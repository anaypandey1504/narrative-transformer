import json
from groq import Groq
from prompts.templates import WORLD_DEFINITION_PROMPT
from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE
from pipeline.utils import parse_llm_json, make_llm_call


def define_target_world(target_setting: str, source_themes: list) -> dict:
    client = Groq(api_key=GROQ_API_KEY)
    
    themes_text = "\n".join([
        f"- {t['theme']}: {t['description']}" 
        for t in source_themes
    ])
    
    prompt = WORLD_DEFINITION_PROMPT.format(
        target_setting=target_setting,
        themes=themes_text
    )
    
    response_content = make_llm_call(
        client=client,
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a world-builder. Always respond with valid JSON only, no markdown."},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE,
        response_format={"type": "json_object"}
    )
    
    return parse_llm_json(response_content)


WORLD_TEMPLATES = {
    "silicon_valley_ai": {
        "description": "Silicon Valley AI Research Labs, 2025",
        "era": "Near future (2025)",
        "domain": "Technology / AI",
        "suggested_conflicts": [
            "Rival tech companies competing for AI supremacy",
            "Ethics vs. profit in AI development",
            "Human connection in a digital age"
        ]
    },
    "cyberpunk": {
        "description": "Cyberpunk Megacity, 2077",
        "era": "Far future",
        "domain": "Dystopian technology",
        "suggested_conflicts": [
            "Corporate control vs. individual freedom",
            "Human vs. machine identity",
            "Underground resistance movements"
        ]
    },
    "space_opera": {
        "description": "Interstellar Federation, 3000 CE",
        "era": "Deep future",
        "domain": "Space exploration",
        "suggested_conflicts": [
            "Rival planetary factions",
            "First contact scenarios",
            "Resource scarcity across star systems"
        ]
    },
    "ancient_mythology": {
        "description": "Ancient mythological realm",
        "era": "Mythic past",
        "domain": "Mythology / Magic",
        "suggested_conflicts": [
            "Gods interfering in mortal affairs",
            "Fate vs. free will",
            "Heroic quests and trials"
        ]
    },
    "post_apocalyptic": {
        "description": "Post-apocalyptic Earth, 2150",
        "era": "Post-collapse",
        "domain": "Survival / Dystopia",
        "suggested_conflicts": [
            "Scarcity and survival",
            "Rebuilding civilization",
            "Trust in a lawless world"
        ]
    }
}


def get_template_suggestions() -> list:
    return [
        {"key": k, "description": v["description"]}
        for k, v in WORLD_TEMPLATES.items()
    ]
