import json
from groq import Groq
from prompts.templates import CONSISTENCY_CHECK_PROMPT
from config import GROQ_API_KEY, MODEL_NAME
from pipeline.utils import parse_llm_json, make_llm_call


def check_consistency(
    original_analysis: dict,
    world: dict,
    characters: dict,
    plot: dict
) -> dict:
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = CONSISTENCY_CHECK_PROMPT.format(
        original_analysis=json.dumps(original_analysis, indent=2),
        world=json.dumps(world, indent=2),
        characters=json.dumps(characters, indent=2),
        plot=json.dumps(plot, indent=2)
    )
    
    response_content = make_llm_call(
        client=client,
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a narrative quality reviewer. Always respond with valid JSON only, no markdown."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    
    return parse_llm_json(response_content)


def calculate_overall_score(check_result: dict) -> dict:
    weights = {
        "thematic_fidelity": 0.3,
        "internal_consistency": 0.25,
        "originality_check": 0.25,
        "cultural_sensitivity": 0.2
    }
    
    scores = {}
    weighted_sum = 0
    
    for key, weight in weights.items():
        category = check_result.get(key, {})
        score = category.get('score', 5)
        scores[key] = score
        weighted_sum += score * weight
    
    return {
        "overall_score": round(weighted_sum, 1),
        "category_scores": scores,
        "pass_threshold": 6.0,
        "passed": weighted_sum >= 6.0
    }


FIX_PROMPT = '''You are a narrative editor. The following transformation has issues that need fixing.

CURRENT ARTIFACTS:
- Plot: {plot}
- Characters: {characters}

ISSUES TO FIX:
{issues}

Provide corrected versions of the affected elements. Focus only on the specific issues mentioned.
Respond in JSON format with keys "fixed_plot" and "fixed_characters" (include only fields that changed).'''


def apply_fixes(
    check_result: dict,
    plot: dict,
    characters: dict,
    original_analysis: dict = None,
    world: dict = None,
    max_retries: int = 1
) -> tuple:
    required_fixes = check_result.get('required_fixes', [])
    applied_fixes = []
    
    if not required_fixes:
        return plot, characters, []
    
    client = Groq(api_key=GROQ_API_KEY)
    
    issues_text = "\n".join(f"- {fix}" for fix in required_fixes)
    
    prompt = FIX_PROMPT.format(
        plot=json.dumps(plot, indent=2),
        characters=json.dumps(characters, indent=2),
        issues=issues_text
    )
    
    try:
        response_content = make_llm_call(
            client=client,
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a narrative editor. Return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        
        fixes = parse_llm_json(response_content)
        
        if 'fixed_plot' in fixes and fixes['fixed_plot']:
            plot = _deep_merge(plot, fixes['fixed_plot'])
            applied_fixes.append({
                "type": "plot",
                "status": "applied",
                "issues_addressed": required_fixes
            })
        
        if 'fixed_characters' in fixes and fixes['fixed_characters']:
            characters = _deep_merge(characters, fixes['fixed_characters'])
            applied_fixes.append({
                "type": "characters", 
                "status": "applied",
                "issues_addressed": required_fixes
            })
        
        if not applied_fixes:
            applied_fixes.append({
                "type": "manual_review",
                "status": "flagged",
                "issues": required_fixes,
                "reason": "LLM did not return specific fixes"
            })
            
    except Exception as e:
        applied_fixes.append({
            "type": "manual_review",
            "status": "flagged",
            "issues": required_fixes,
            "reason": f"Fix generation failed: {str(e)}"
        })
    
    return plot, characters, applied_fixes


def _deep_merge(base: dict, updates: dict) -> dict:
    result = base.copy()
    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result
