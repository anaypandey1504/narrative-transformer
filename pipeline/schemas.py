from pydantic import BaseModel, Field, validator
from typing import List, Optional


class ThemeSchema(BaseModel):
    theme: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class CharacterArchetypeSchema(BaseModel):
    name: str = Field(..., min_length=1)
    archetype: str = Field(..., min_length=1)
    motivation: str = Field(..., min_length=1)
    flaw: str = Field(..., min_length=1)
    role_in_plot: str = Field(..., min_length=1)


class CentralConflictSchema(BaseModel):
    type: str = Field(..., pattern=r'^(Internal|External|Both)$')
    description: str = Field(..., min_length=1)
    opposing_forces: List[str] = Field(..., min_items=2)


class EmotionalArcSchema(BaseModel):
    opening_state: str = Field(..., min_length=1)
    peak_emotion: str = Field(..., min_length=1)
    closing_state: str = Field(..., min_length=1)


class PlotStructureSchema(BaseModel):
    setup: str = Field(..., min_length=1)
    inciting_incident: str = Field(..., min_length=1)
    rising_action: List[str] = Field(..., min_items=1)
    climax: str = Field(..., min_length=1)
    falling_action: str = Field(..., min_length=1)
    resolution: str = Field(..., min_length=1)


class SourceAbstractionSchema(BaseModel):
    title: str = Field(..., min_length=1)
    core_themes: List[ThemeSchema] = Field(..., min_items=1)
    character_archetypes: List[CharacterArchetypeSchema] = Field(..., min_items=1)
    central_conflict: CentralConflictSchema
    emotional_arc: EmotionalArcSchema
    plot_structure: PlotStructureSchema
    
    @validator('core_themes')
    def validate_themes_count(cls, v):
        if len(v) < 2:
            raise ValueError('At least 2 themes required for meaningful transformation')
        return v
    
    @validator('character_archetypes')
    def validate_characters_count(cls, v):
        if len(v) < 2:
            raise ValueError('At least 2 characters required')
        return v


def validate_source_abstraction(data: dict) -> tuple:
    try:
        validated = SourceAbstractionSchema(**data)
        return True, validated.dict(), None
    except Exception as e:
        return False, data, str(e)
