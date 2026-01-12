SOURCE_ABSTRACTION_PROMPT = '''You are a narrative analyst. Analyze the following source material and extract its core narrative elements.

SOURCE MATERIAL:
{source_material}

Analyze this story and provide a structured breakdown. Do NOT copy any original text verbatim.

Respond in the following JSON format ONLY (no markdown, no explanation):
{{
    "title": "Name of the source work",
    "core_themes": [
        {{
            "theme": "Theme name",
            "description": "How this theme manifests in the story"
        }}
    ],
    "character_archetypes": [
        {{
            "name": "Original character name",
            "archetype": "The universal archetype (e.g., Star-crossed lover, Tragic hero)",
            "motivation": "What drives this character",
            "flaw": "Their fatal weakness or limitation",
            "role_in_plot": "Their function in the narrative"
        }}
    ],
    "central_conflict": {{
        "type": "Internal/External/Both",
        "description": "The core struggle",
        "opposing_forces": ["Force 1", "Force 2"]
    }},
    "emotional_arc": {{
        "opening_state": "Emotional tone at start",
        "peak_emotion": "Most intense emotional moment",
        "closing_state": "Emotional resolution"
    }},
    "plot_structure": {{
        "setup": "Initial situation and world",
        "inciting_incident": "What disrupts the status quo",
        "rising_action": ["Key escalation point 1", "Key escalation point 2"],
        "climax": "The turning point of highest tension",
        "falling_action": "Consequences of the climax",
        "resolution": "How the story concludes"
    }}
}}'''

WORLD_DEFINITION_PROMPT = '''You are a world-builder. Create a coherent alternate universe based on the user's target setting.

TARGET SETTING: {target_setting}

ORIGINAL STORY THEMES TO PRESERVE:
{themes}

Design a world that can support these themes while being internally consistent.

Respond in the following JSON format ONLY (no markdown, no explanation):
{{
    "world_name": "Name or description of this world",
    "era": "Time period",
    "domain": "Primary domain (technology, magic, dystopia, etc.)",
    "setting_details": {{
        "geography": "Where this takes place",
        "society": "Social structure and norms",
        "technology_or_power": "What enables or limits characters",
        "culture": "Cultural values and practices"
    }},
    "internal_rules": [
        {{
            "rule": "A fundamental rule of this world",
            "implication": "How this affects the narrative"
        }}
    ],
    "conflict_drivers": [
        "What creates tension in this world"
    ],
    "forbidden_actions": [
        "What characters cannot do (constraints that add tension)"
    ],
    "theme_mapping": [
        {{
            "original_theme": "Theme from original",
            "world_expression": "How it manifests in this new world"
        }}
    ]
}}'''

CHARACTER_TRANSFORM_PROMPT = '''You are a character designer. Transform the original characters to fit the new world while preserving their essence.

ORIGINAL CHARACTERS:
{characters}

TARGET WORLD:
{world}

Transform each character. Preserve their core archetype, motivation, and flaw.
Create new names, roles, and identities appropriate to the new world.
Do NOT use any original dialogue or specific descriptions.

Respond in the following JSON format ONLY (no markdown, no explanation):
{{
    "transformed_characters": [
        {{
            "original_name": "Name from source",
            "new_name": "Name in new world",
            "new_identity": "Who they are in this world",
            "occupation_or_role": "Their position in this society",
            "preserved_motivation": "Same core drive, recontextualized",
            "preserved_flaw": "Same weakness, recontextualized",
            "world_specific_traits": ["Trait fitting the new world"],
            "key_relationships": ["Relationship to other transformed characters"],
            "visual_description": "Brief appearance in new world context"
        }}
    ],
    "group_dynamics": {{
        "alliances": ["Who works together"],
        "conflicts": ["Who opposes whom"],
        "key_relationship_transformation": "How the central relationship changes in context"
    }}
}}'''

PLOT_RECONSTRUCTION_PROMPT = '''You are a story architect. Reconstruct the narrative for the new world.

ORIGINAL PLOT STRUCTURE:
{plot_structure}

TRANSFORMED CHARACTERS:
{characters}

TARGET WORLD RULES:
{world_rules}

Rebuild the story maintaining cause-and-effect logic. No deus ex machina.
Every event must follow logically from the world's rules and character motivations.

Respond in the following JSON format ONLY (no markdown, no explanation):
{{
    "reconstructed_plot": {{
        "setup": {{
            "scene": "Opening scene description",
            "world_establishment": "How we show the world",
            "character_introductions": ["How each main character is introduced"],
            "status_quo": "The initial state before disruption"
        }},
        "inciting_incident": {{
            "event": "What disrupts everything",
            "cause": "Why this happens (rooted in world/character logic)",
            "immediate_effect": "First consequences"
        }},
        "rising_action": [
            {{
                "event": "Key scene or turning point",
                "cause": "What leads to this",
                "effect": "What results from this",
                "character_development": "How characters change"
            }}
        ],
        "climax": {{
            "event": "The peak confrontation",
            "choices_made": "Critical decisions by main characters",
            "stakes": "What's at risk",
            "twist_or_revelation": "Any surprising element (optional)"
        }},
        "falling_action": {{
            "immediate_aftermath": "Direct consequences of climax",
            "character_reactions": "How characters respond"
        }},
        "resolution": {{
            "final_state": "How things end",
            "thematic_closure": "What message or feeling concludes the story",
            "open_threads": "Any intentional ambiguity (optional)"
        }}
    }},
    "cause_effect_chain": [
        "Event A leads to Event B because..."
    ]
}}'''

CONSISTENCY_CHECK_PROMPT = '''You are a narrative quality reviewer. Check the transformation for consistency and safety.

ORIGINAL STORY ANALYSIS:
{original_analysis}

TRANSFORMATION DETAILS:
- World: {world}
- Characters: {characters}
- Plot: {plot}

Verify the transformation meets all requirements. Be strict but fair.

Respond in the following JSON format ONLY (no markdown, no explanation):
{{
    "thematic_fidelity": {{
        "score": 1-10,
        "preserved_themes": ["Themes successfully carried over"],
        "lost_themes": ["Themes that were not preserved (if any)"],
        "assessment": "Overall evaluation"
    }},
    "internal_consistency": {{
        "score": 1-10,
        "logical_issues": ["Any plot holes or contradictions"],
        "world_rule_violations": ["Any breaks in world logic"],
        "assessment": "Overall evaluation"
    }},
    "originality_check": {{
        "score": 1-10,
        "copied_elements": ["Any elements too close to original (should be empty)"],
        "successfully_transformed": ["Elements well-adapted"],
        "assessment": "Overall evaluation"
    }},
    "cultural_sensitivity": {{
        "score": 1-10,
        "concerns": ["Any potentially problematic elements"],
        "positive_representation": ["Respectful elements"],
        "assessment": "Overall evaluation"
    }},
    "overall_pass": true,
    "required_fixes": ["List of mandatory changes before output (if any)"],
    "suggestions": ["Optional improvements"]
}}'''

STORY_GENERATION_PROMPT = '''You are a master storyteller. Write the final reimagined story.

WORLD:
{world}

CHARACTERS:
{characters}

PLOT:
{plot}

Write a compelling 2-3 page narrative that brings this transformed story to life.

Requirements:
- Write in engaging prose, not bullet points
- Include dialogue that feels natural to the new world
- Show, don't tell - demonstrate themes through action
- Create vivid scenes with sensory details
- Maintain consistent tone throughout
- End with emotional resonance

The story should be readable as a standalone piece while clearly echoing the original's spirit.

Write the story now:'''

TRANSFORMATION_DIFF_PROMPT = '''You are a narrative analyst. Create a transformation comparison.

ORIGINAL:
{original}

TRANSFORMED:
{transformed}

Create a side-by-side comparison showing how each major element was transformed.

Respond in the following JSON format ONLY (no markdown, no explanation):
{{
    "transformation_diff": [
        {{
            "element_type": "Character/Theme/Plot Point/Symbol",
            "original": "What it was",
            "transformed": "What it became",
            "preservation_note": "What essence was kept"
        }}
    ],
    "transformation_summary": "Overall description of the transformation approach"
}}'''
