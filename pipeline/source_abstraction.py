import json
from groq import Groq
from prompts.templates import SOURCE_ABSTRACTION_PROMPT
from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE
from pipeline.utils import parse_llm_json, make_llm_call


def extract_source_elements(source_material: str) -> dict:
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = SOURCE_ABSTRACTION_PROMPT.format(source_material=source_material)
    
    response_content = make_llm_call(
        client=client,
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a narrative analyst. Always respond with valid JSON only, no markdown."},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE,
        response_format={"type": "json_object"}
    )
    
    return parse_llm_json(response_content)


def load_source_material(source_name: str, database_path: str = "data/source_materials.json") -> str:
    with open(database_path, 'r', encoding='utf-8') as f:
        database = json.load(f)
    
    source_key = source_name.lower().replace(" ", "_").replace("and", "&").replace("&", "and")
    
    possible_keys = [
        source_key,
        source_name.lower().replace(" ", "_"),
        source_name.lower().replace(" and ", "_and_"),
    ]
    
    source = None
    for key in database:
        if key.lower() in [k.lower() for k in possible_keys]:
            source = database[key]
            break
        if database[key].get("title", "").lower() == source_name.lower():
            source = database[key]
            break
    
    if not source:
        return source_name
    
    formatted = f"""
Title: {source['title']}
Author: {source['author']} ({source['year']})
Type: {source['type']}

Summary: {source['summary']}

Main Characters: {', '.join(source['characters'])}

Key Themes: {', '.join(source['themes'])}

Setting: {source['setting']}
"""
    return formatted
