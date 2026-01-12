import pytest
import sys
sys.path.insert(0, '.')

from pipeline.plot_reconstruction import validate_cause_effect_chain
from pipeline.consistency_check import calculate_overall_score
from pipeline.character_transform import calculate_preservation_score
from pipeline.schemas import validate_world_definition, validate_character_transformation


class TestValidateCauseEffectChain:
    
    def test_valid_complete_plot(self):
        plot = {
            'reconstructed_plot': {
                'setup': {'scene': 'Opening'},
                'inciting_incident': {'event': 'Disruption', 'cause': 'Character choice'},
                'rising_action': [
                    {'event': 'Escalation', 'effect': 'Tension increases'}
                ],
                'climax': {'event': 'Confrontation', 'stakes': 'Everything at risk'},
                'resolution': {'final_state': 'Conclusion'}
            },
            'cause_effect_chain': ['A leads to B']
        }
        result = validate_cause_effect_chain(plot)
        assert result['valid'] is True
        assert len(result['issues']) == 0
    
    def test_missing_inciting_cause(self):
        plot = {
            'reconstructed_plot': {
                'setup': {'scene': 'Opening'},
                'inciting_incident': {'event': 'Disruption'},
                'rising_action': [],
                'climax': {'event': 'Peak', 'stakes': 'High'},
                'resolution': {'final_state': 'End'}
            }
        }
        result = validate_cause_effect_chain(plot)
        assert result['valid'] is False
        assert 'Inciting incident missing causal explanation' in result['issues']
    
    def test_missing_climax_stakes(self):
        plot = {
            'reconstructed_plot': {
                'setup': {'scene': 'Opening'},
                'inciting_incident': {'event': 'Start', 'cause': 'Reason'},
                'rising_action': [],
                'climax': {'event': 'Peak'},
                'resolution': {'final_state': 'End'}
            }
        }
        result = validate_cause_effect_chain(plot)
        assert result['valid'] is False
        assert 'Climax missing stakes' in result['issues']
    
    def test_rising_action_missing_effect(self):
        plot = {
            'reconstructed_plot': {
                'setup': {'scene': 'Opening'},
                'inciting_incident': {'event': 'Start', 'cause': 'Reason'},
                'rising_action': [
                    {'event': 'Event 1'},
                    {'event': 'Event 2', 'effect': 'Result'}
                ],
                'climax': {'event': 'Peak', 'stakes': 'High'},
                'resolution': {'final_state': 'End'}
            }
        }
        result = validate_cause_effect_chain(plot)
        assert result['valid'] is False
        assert 'Rising action event 1 missing effect' in result['issues']
    
    def test_empty_plot_structure(self):
        plot = {'reconstructed_plot': {}}
        result = validate_cause_effect_chain(plot)
        assert result['valid'] is False
        assert len(result['issues']) >= 2


class TestCalculateOverallScore:
    
    def test_all_perfect_scores(self):
        check_result = {
            'thematic_fidelity': {'score': 10},
            'internal_consistency': {'score': 10},
            'originality_check': {'score': 10},
            'cultural_sensitivity': {'score': 10}
        }
        result = calculate_overall_score(check_result)
        assert result['overall_score'] == 10.0
        assert result['passed'] is True
    
    def test_threshold_boundary(self):
        check_result = {
            'thematic_fidelity': {'score': 6},
            'internal_consistency': {'score': 6},
            'originality_check': {'score': 6},
            'cultural_sensitivity': {'score': 6}
        }
        result = calculate_overall_score(check_result)
        assert result['overall_score'] == 6.0
        assert result['passed'] is True
    
    def test_below_threshold(self):
        check_result = {
            'thematic_fidelity': {'score': 5},
            'internal_consistency': {'score': 5},
            'originality_check': {'score': 5},
            'cultural_sensitivity': {'score': 5}
        }
        result = calculate_overall_score(check_result)
        assert result['overall_score'] == 5.0
        assert result['passed'] is False
    
    def test_missing_category_uses_default(self):
        check_result = {
            'thematic_fidelity': {'score': 10}
        }
        result = calculate_overall_score(check_result)
        assert result['overall_score'] == 6.5
        assert result['passed'] is True


class TestCalculatePreservationScore:
    
    def test_high_preservation(self):
        original = {'motivation': 'X', 'flaw': 'Y'}
        transformed = {
            'preserved_motivation': 'To achieve X in new context',
            'preserved_flaw': 'Still has Y weakness'
        }
        result = calculate_preservation_score(original, transformed)
        assert result == 'High'
    
    def test_medium_preservation_motivation_only(self):
        original = {'motivation': 'X', 'flaw': 'Y'}
        transformed = {
            'preserved_motivation': 'To achieve X',
            'preserved_flaw': None
        }
        result = calculate_preservation_score(original, transformed)
        assert result == 'Medium'
    
    def test_medium_preservation_flaw_only(self):
        original = {'motivation': 'X', 'flaw': 'Y'}
        transformed = {
            'preserved_motivation': None,
            'preserved_flaw': 'Still has Y'
        }
        result = calculate_preservation_score(original, transformed)
        assert result == 'Medium'
    
    def test_low_preservation(self):
        original = {'motivation': 'X', 'flaw': 'Y'}
        transformed = {}
        result = calculate_preservation_score(original, transformed)
        assert result == 'Low'


class TestValidateWorldDefinition:
    """Tests for Stage 2 Pydantic validation."""
    
    def test_valid_world_definition(self):
        world = {
            'world_name': 'Test World',
            'era': '2025',
            'domain': 'Technology',
            'setting_details': {
                'geography': 'Urban city',
                'society': 'Democratic',
                'technology_or_power': 'AI systems',
                'culture': 'Innovation-focused'
            },
            'internal_rules': [
                {'rule': 'Rule 1', 'implication': 'Effect 1'},
                {'rule': 'Rule 2', 'implication': 'Effect 2'}
            ],
            'conflict_drivers': ['Competition'],
            'forbidden_actions': [],
            'theme_mapping': [
                {'original_theme': 'Love', 'world_expression': 'Digital connection'}
            ]
        }
        valid, result, error = validate_world_definition(world)
        assert valid is True
        assert error is None
    
    def test_missing_required_field(self):
        world = {
            'world_name': 'Test World',
            'era': '2025',
            # Missing 'domain' and other required fields
        }
        valid, result, error = validate_world_definition(world)
        assert valid is False
        assert error is not None
    
    def test_insufficient_internal_rules(self):
        world = {
            'world_name': 'Test World',
            'era': '2025',
            'domain': 'Tech',
            'setting_details': {
                'geography': 'City',
                'society': 'Modern',
                'technology_or_power': 'Computers',
                'culture': 'Digital'
            },
            'internal_rules': [{'rule': 'Only one', 'implication': 'Not enough'}],
            'conflict_drivers': ['Conflict'],
            'theme_mapping': [{'original_theme': 'Theme', 'world_expression': 'Expression'}]
        }
        valid, result, error = validate_world_definition(world)
        assert valid is False
        assert 'At least 2 internal rules' in error


class TestValidateCharacterTransformation:
    """Tests for Stage 3 Pydantic validation."""
    
    def test_valid_character_transformation(self):
        chars = {
            'transformed_characters': [
                {
                    'original_name': 'Romeo',
                    'new_name': 'Rohan',
                    'new_identity': 'Tech entrepreneur',
                    'occupation_or_role': 'Startup founder',
                    'preserved_motivation': 'Love conquers all',
                    'preserved_flaw': 'Impulsive decisions',
                    'world_specific_traits': ['Tech-savvy'],
                    'key_relationships': ['Partner']
                },
                {
                    'original_name': 'Juliet',
                    'new_name': 'Jaya',
                    'new_identity': 'Rival company heir',
                    'occupation_or_role': 'Product manager',
                    'preserved_motivation': 'True love',
                    'preserved_flaw': 'Family loyalty conflict',
                    'world_specific_traits': ['Ambitious'],
                    'key_relationships': ['Family']
                }
            ],
            'group_dynamics': {
                'alliances': ['Romeo-Juliet'],
                'conflicts': ['Families'],
                'key_relationship_transformation': 'Corporate rivalry instead of family feud'
            }
        }
        valid, result, error = validate_character_transformation(chars)
        assert valid is True
        assert error is None
    
    def test_missing_preserved_motivation(self):
        chars = {
            'transformed_characters': [
                {
                    'original_name': 'Romeo',
                    'new_name': 'Rohan',
                    'new_identity': 'Engineer',
                    'occupation_or_role': 'Dev',
                    # Missing 'preserved_motivation'
                    'preserved_flaw': 'Impulsive',
                    'world_specific_traits': ['Smart']
                },
                {
                    'original_name': 'Juliet',
                    'new_name': 'Jaya',
                    'new_identity': 'Manager',
                    'occupation_or_role': 'PM',
                    'preserved_motivation': 'Love',
                    'preserved_flaw': 'Conflict',
                    'world_specific_traits': ['Driven']
                }
            ],
            'group_dynamics': {
                'key_relationship_transformation': 'Test'
            }
        }
        valid, result, error = validate_character_transformation(chars)
        assert valid is False
        assert error is not None
    
    def test_insufficient_characters(self):
        chars = {
            'transformed_characters': [
                {
                    'original_name': 'Solo',
                    'new_name': 'Only One',
                    'new_identity': 'Lonely',
                    'occupation_or_role': 'Hermit',
                    'preserved_motivation': 'Solitude',
                    'preserved_flaw': 'Isolation',
                    'world_specific_traits': ['Alone']
                }
            ],
            'group_dynamics': {
                'key_relationship_transformation': 'None'
            }
        }
        valid, result, error = validate_character_transformation(chars)
        assert valid is False
        assert 'At least 2 characters' in error
