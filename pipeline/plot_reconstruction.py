import json
from groq import Groq
from prompts.templates import PLOT_RECONSTRUCTION_PROMPT
from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE
from pipeline.utils import parse_llm_json, make_llm_call


def reconstruct_plot(
    original_plot: dict,
    transformed_characters: dict,
    world_rules: dict
) -> dict:
    client = Groq(api_key=GROQ_API_KEY)
    
    plot_text = json.dumps(original_plot, indent=2)
    characters_text = json.dumps(
        transformed_characters.get('transformed_characters', []), 
        indent=2
    )
    rules_text = json.dumps(world_rules.get('internal_rules', []), indent=2)
    
    prompt = PLOT_RECONSTRUCTION_PROMPT.format(
        plot_structure=plot_text,
        characters=characters_text,
        world_rules=rules_text
    )
    
    response_content = make_llm_call(
        client=client,
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a story architect. Always respond with valid JSON only, no markdown."},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE,
        response_format={"type": "json_object"}
    )
    
    return parse_llm_json(response_content)


def validate_cause_effect_chain(plot: dict) -> dict:
    issues = []
    reconstructed = plot.get('reconstructed_plot', {})
    
    if not reconstructed.get('setup'):
        issues.append("Missing setup section")
    
    inciting = reconstructed.get('inciting_incident', {})
    if not inciting.get('cause'):
        issues.append("Inciting incident missing causal explanation")
    
    rising = reconstructed.get('rising_action', [])
    for i, event in enumerate(rising):
        if not event.get('effect'):
            issues.append(f"Rising action event {i+1} missing effect")
    
    climax = reconstructed.get('climax', {})
    if not climax.get('stakes'):
        issues.append("Climax missing stakes")
    
    if not reconstructed.get('resolution'):
        issues.append("Missing resolution")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "cause_effect_chain": plot.get('cause_effect_chain', [])
    }
