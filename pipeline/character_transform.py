import json
from groq import Groq
from prompts.templates import CHARACTER_TRANSFORM_PROMPT
from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE
from pipeline.utils import parse_llm_json, make_llm_call


def transform_characters(source_characters: list, target_world: dict) -> dict:
    client = Groq(api_key=GROQ_API_KEY)
    
    characters_text = json.dumps(source_characters, indent=2)
    
    world_text = f"""
World: {target_world.get('world_name', 'Target World')}
Era: {target_world.get('era', 'Unknown')}
Domain: {target_world.get('domain', 'Unknown')}
Setting: {json.dumps(target_world.get('setting_details', {}), indent=2)}
Rules: {json.dumps(target_world.get('internal_rules', []), indent=2)}
"""
    
    prompt = CHARACTER_TRANSFORM_PROMPT.format(
        characters=characters_text,
        world=world_text
    )
    
    response_content = make_llm_call(
        client=client,
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a character designer. Always respond with valid JSON only, no markdown."},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE,
        response_format={"type": "json_object"}
    )
    
    return parse_llm_json(response_content)


def create_character_mapping_table(original: list, transformed: dict) -> list:
    mappings = []
    transformed_chars = transformed.get('transformed_characters', [])
    
    for orig in original:
        match = None
        for trans in transformed_chars:
            if trans.get('original_name', '').lower() == orig.get('name', '').lower():
                match = trans
                break
        
        if match:
            mappings.append({
                "original": {
                    "name": orig.get('name'),
                    "archetype": orig.get('archetype'),
                    "motivation": orig.get('motivation'),
                    "flaw": orig.get('flaw')
                },
                "transformed": {
                    "name": match.get('new_name'),
                    "identity": match.get('new_identity'),
                    "motivation": match.get('preserved_motivation'),
                    "flaw": match.get('preserved_flaw')
                },
                "preservation_score": calculate_preservation_score(orig, match)
            })
    
    return mappings


def calculate_preservation_score(original: dict, transformed: dict) -> str:
    if transformed.get('preserved_motivation') and transformed.get('preserved_flaw'):
        return "High"
    elif transformed.get('preserved_motivation') or transformed.get('preserved_flaw'):
        return "Medium"
    return "Low"
