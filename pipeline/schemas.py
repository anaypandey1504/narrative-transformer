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


# ============================================================================
# Stage 2: World Definition Schema
# ============================================================================

class SettingDetailsSchema(BaseModel):
    geography: str = Field(..., min_length=1)
    society: str = Field(..., min_length=1)
    technology_or_power: str = Field(..., min_length=1)
    culture: str = Field(..., min_length=1)


class InternalRuleSchema(BaseModel):
    rule: str = Field(..., min_length=1)
    implication: str = Field(..., min_length=1)


class ThemeMappingSchema(BaseModel):
    original_theme: str = Field(..., min_length=1)
    world_expression: str = Field(..., min_length=1)


class WorldDefinitionSchema(BaseModel):
    world_name: str = Field(..., min_length=1)
    era: str = Field(..., min_length=1)
    domain: str = Field(..., min_length=1)
    setting_details: SettingDetailsSchema
    internal_rules: List[InternalRuleSchema] = Field(..., min_items=1)
    conflict_drivers: List[str] = Field(..., min_items=1)
    forbidden_actions: List[str] = Field(default_factory=list)
    theme_mapping: List[ThemeMappingSchema] = Field(..., min_items=1)
    
    @validator('internal_rules')
    def validate_rules_count(cls, v):
        if len(v) < 2:
            raise ValueError('At least 2 internal rules required for coherent world')
        return v


def validate_world_definition(data: dict) -> tuple:
    """Validate Stage 2 output against WorldDefinitionSchema."""
    try:
        validated = WorldDefinitionSchema(**data)
        return True, validated.dict(), None
    except Exception as e:
        return False, data, str(e)


# ============================================================================
# Stage 3: Character Transformation Schema
# ============================================================================

class TransformedCharacterSchema(BaseModel):
    original_name: str = Field(..., min_length=1)
    new_name: str = Field(..., min_length=1)
    new_identity: str = Field(..., min_length=1)
    occupation_or_role: str = Field(..., min_length=1)
    preserved_motivation: str = Field(..., min_length=1)
    preserved_flaw: str = Field(..., min_length=1)
    world_specific_traits: List[str] = Field(..., min_items=1)
    key_relationships: List[str] = Field(default_factory=list)
    visual_description: Optional[str] = None


class GroupDynamicsSchema(BaseModel):
    alliances: List[str] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)
    key_relationship_transformation: str = Field(..., min_length=1)


class CharacterTransformationSchema(BaseModel):
    transformed_characters: List[TransformedCharacterSchema] = Field(..., min_items=1)
    group_dynamics: GroupDynamicsSchema
    
    @validator('transformed_characters')
    def validate_characters_count(cls, v):
        if len(v) < 2:
            raise ValueError('At least 2 characters required for narrative')
        return v


def validate_character_transformation(data: dict) -> tuple:
    """Validate Stage 3 output against CharacterTransformationSchema."""
    try:
        validated = CharacterTransformationSchema(**data)
        return True, validated.dict(), None
    except Exception as e:
        return False, data, str(e)
