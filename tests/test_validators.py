import pytest
import sys
sys.path.insert(0, '.')

from pipeline.plot_reconstruction import validate_cause_effect_chain
from pipeline.consistency_check import calculate_overall_score
from pipeline.character_transform import calculate_preservation_score


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
