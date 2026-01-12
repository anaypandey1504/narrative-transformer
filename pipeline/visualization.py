from typing import Optional


def generate_transformation_diagram(artifacts: dict) -> str:
    stages = artifacts.get('stages', {})
    metadata = artifacts.get('metadata', {})
    
    source_title = metadata.get('source_title', 'Source')
    target_world = metadata.get('target_world', 'Target')
    
    source_analysis = stages.get('1_source_abstraction', {})
    world_def = stages.get('2_world_definition', {})
    char_transform = stages.get('3_character_transformation', {})
    plot_recon = stages.get('4_plot_reconstruction', {})
    consistency = stages.get('5_consistency_check', {})
    
    themes = source_analysis.get('core_themes', [])
    theme_names = [t.get('theme', 'Theme')[:20] for t in themes[:3]]
    
    characters = source_analysis.get('character_archetypes', [])
    orig_chars = [c.get('name', 'Char')[:15] for c in characters[:4]]
    
    transformed = char_transform.get('transformed_characters', [])
    new_chars = [c.get('new_name', 'New')[:15] for c in transformed[:4]]
    
    theme_mapping = world_def.get('theme_mapping', [])
    
    overall = consistency.get('overall_score', {})
    score = overall.get('overall_score', 'N/A')
    passed = overall.get('passed', False)
    
    diagram = f"""```mermaid
flowchart TB
    subgraph SOURCE["{source_title}"]
        S1["Themes: {', '.join(theme_names)}"]
        S2["Characters: {', '.join(orig_chars[:2])}..."]
        S3["Plot Structure"]
    end
    
    subgraph STAGE1["Stage 1: Abstraction"]
        A1[Extract Archetypes]
        A2[Identify Conflicts]
        A3[Map Emotional Arc]
    end
    
    subgraph STAGE2["Stage 2: World Building"]
        W1["{target_world}"]
        W2["Rules: {len(world_def.get('internal_rules', []))} defined"]
        W3["Constraints: {len(world_def.get('forbidden_actions', []))} set"]
    end
    
    subgraph STAGE3["Stage 3: Character Transform"]
        C1["{orig_chars[0] if orig_chars else 'Char'} → {new_chars[0] if new_chars else 'New'}"]
        C2["Preserve motivations"]
        C3["Adapt to world"]
    end
    
    subgraph STAGE4["Stage 4: Plot Rebuild"]
        P1[Cause-Effect Chain]
        P2[New Conflicts]
        P3[Resolution]
    end
    
    subgraph STAGE5["Stage 5: Validation"]
        V1["Score: {score}/10"]
        V2["Pass: {'✓' if passed else '✗'}"]
    end
    
    subgraph OUTPUT["Final Output"]
        O1[story.md]
        O2[story.pdf]
        O3[artifacts.json]
    end
    
    SOURCE --> STAGE1
    STAGE1 --> STAGE2
    STAGE2 --> STAGE3
    STAGE3 --> STAGE4
    STAGE4 --> STAGE5
    STAGE5 --> OUTPUT
    
    style SOURCE fill:#e1f5fe
    style OUTPUT fill:#c8e6c9
    style STAGE5 fill:#{'c8e6c9' if passed else 'ffcdd2'}
```"""
    
    return diagram


def generate_character_mapping_table(artifacts: dict) -> str:
    stages = artifacts.get('stages', {})
    source = stages.get('1_source_abstraction', {})
    transformed = stages.get('3_character_transformation', {})
    
    orig_chars = {c.get('name', ''): c for c in source.get('character_archetypes', [])}
    new_chars = transformed.get('transformed_characters', [])
    
    table = "| Original | Archetype | → | Transformed | Role | Preserved |\n"
    table += "|----------|-----------|---|-------------|------|----------|\n"
    
    for nc in new_chars:
        orig_name = nc.get('original_name', '')
        orig = orig_chars.get(orig_name, {})
        
        archetype = orig.get('archetype', 'N/A')[:20]
        new_name = nc.get('new_name', 'N/A')
        new_role = nc.get('occupation_or_role', 'N/A')[:25]
        preserved = "✓" if nc.get('preserved_motivation') and nc.get('preserved_flaw') else "◐"
        
        table += f"| {orig_name} | {archetype} | → | {new_name} | {new_role} | {preserved} |\n"
    
    return table


def generate_theme_flow(artifacts: dict) -> str:
    stages = artifacts.get('stages', {})
    world = stages.get('2_world_definition', {})
    
    mappings = world.get('theme_mapping', [])
    
    if not mappings:
        return "No theme mappings found."
    
    lines = ["| Original Theme | → | World Expression |", "|----------------|---|------------------|"]
    
    for m in mappings:
        orig = m.get('original_theme', 'N/A')[:25]
        expr = m.get('world_expression', 'N/A')[:40]
        lines.append(f"| {orig} | → | {expr}... |")
    
    return "\n".join(lines)


def generate_visualization_report(artifacts: dict) -> str:
    metadata = artifacts.get('metadata', {})
    
    report = f"""# Transformation Visualization

## Pipeline Flow

{generate_transformation_diagram(artifacts)}

## Character Mapping

{generate_character_mapping_table(artifacts)}

## Theme Flow

{generate_theme_flow(artifacts)}

## Quality Breakdown

"""
    
    stages = artifacts.get('stages', {})
    consistency = stages.get('5_consistency_check', {})
    
    categories = ['thematic_fidelity', 'internal_consistency', 'originality_check', 'cultural_sensitivity']
    
    for cat in categories:
        data = consistency.get(cat, {})
        score = data.get('score', 'N/A')
        bar = '█' * int(score) + '░' * (10 - int(score)) if isinstance(score, int) else '░' * 10
        report += f"- **{cat.replace('_', ' ').title()}**: [{bar}] {score}/10\n"
    
    overall = consistency.get('overall_score', {})
    report += f"\n**Overall**: {overall.get('overall_score', 'N/A')}/10 | {'PASSED ✓' if overall.get('passed') else 'FAILED ✗'}\n"
    
    return report
