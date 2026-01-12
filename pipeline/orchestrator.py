import json
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from pipeline.source_abstraction import extract_source_elements, load_source_material
from pipeline.world_definition import define_target_world
from pipeline.character_transform import transform_characters, create_character_mapping_table
from pipeline.plot_reconstruction import reconstruct_plot, validate_cause_effect_chain
from pipeline.consistency_check import check_consistency, calculate_overall_score, apply_fixes
from pipeline.output_generator import (
    generate_story, 
    generate_transformation_diff,
    compile_artifacts,
    format_story_markdown,
    generate_pdf
)
from pipeline.visualization import generate_visualization_report
from pipeline.schemas import validate_source_abstraction

console = Console()


class NarrativeTransformer:
    
    CHECKPOINT_FILE = "checkpoint.json"
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.artifacts = {}
        self._checkpoint_path = os.path.join(output_dir, self.CHECKPOINT_FILE)
    
    def _save_checkpoint(self, stage: int, source_name: str, target_setting: str):
        os.makedirs(self.output_dir, exist_ok=True)
        checkpoint = {
            "completed_stage": stage,
            "source_name": source_name,
            "target_setting": target_setting,
            "artifacts": self.artifacts,
            "timestamp": datetime.now().isoformat()
        }
        with open(self._checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2, ensure_ascii=False)
        console.print(f"  [dim]📁 Checkpoint saved (stage {stage})[/dim]")
    
    def _load_checkpoint(self) -> dict:
        if os.path.exists(self._checkpoint_path):
            with open(self._checkpoint_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def _clear_checkpoint(self):
        if os.path.exists(self._checkpoint_path):
            os.remove(self._checkpoint_path)
    
    def can_resume(self) -> bool:
        return os.path.exists(self._checkpoint_path)
    
    def get_checkpoint_info(self) -> dict:
        checkpoint = self._load_checkpoint()
        if checkpoint:
            return {
                "stage": checkpoint.get("completed_stage"),
                "source": checkpoint.get("source_name"),
                "target": checkpoint.get("target_setting"),
                "timestamp": checkpoint.get("timestamp")
            }
        return None
        
    def run_pipeline(self, source_name: str, target_setting: str, source_text: str = None, resume: bool = False) -> dict:
        start_stage = 1
        checkpoint = None
        
        if resume and self.can_resume():
            checkpoint = self._load_checkpoint()
            start_stage = checkpoint['completed_stage'] + 1
            self.artifacts = checkpoint['artifacts']
            source_name = checkpoint['source_name']
            target_setting = checkpoint['target_setting']
            console.print(f"[yellow]Resuming from stage {start_stage} (checkpoint: {checkpoint['timestamp']})[/yellow]")
        console.print(Panel.fit(
            f"[bold cyan]AI Narrative Transformation System[/bold cyan]\n"
            f"Source: {source_name}\n"
            f"Target: {target_setting}",
            title="Starting Pipeline"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            if start_stage <= 1:
                task = progress.add_task("[cyan]Stage 1: Extracting source elements...", total=None)
                
                if source_text:
                    source_material = source_text
                else:
                    source_material = load_source_material(source_name)
                
                source_analysis = extract_source_elements(source_material)
                
                valid, source_analysis, error = validate_source_abstraction(source_analysis)
                if not valid:
                    console.print(f"  [yellow]⚠ Schema validation warning: {error}[/yellow]")
                
                self.artifacts['source_analysis'] = source_analysis
                
                progress.update(task, description="[green]✓ Stage 1: Source abstraction complete")
                console.print(f"  → Extracted {len(source_analysis.get('character_archetypes', []))} characters, "
                             f"{len(source_analysis.get('core_themes', []))} themes")
                self._save_checkpoint(1, source_name, target_setting)
            else:
                source_analysis = self.artifacts.get('source_analysis', {})
                console.print("[dim]Stage 1: Skipped (loaded from checkpoint)[/dim]")
            
            if start_stage <= 2:
                task = progress.add_task("[cyan]Stage 2: Defining target world...", total=None)
                
                world = define_target_world(
                    target_setting,
                    source_analysis.get('core_themes', [])
                )
                self.artifacts['world'] = world
                
                progress.update(task, description="[green]✓ Stage 2: World definition complete")
                console.print(f"  → Created world: {world.get('world_name', 'Target World')}")
                console.print(f"  → {len(world.get('internal_rules', []))} internal rules defined")
                self._save_checkpoint(2, source_name, target_setting)
            else:
                world = self.artifacts.get('world', {})
                console.print("[dim]Stage 2: Skipped (loaded from checkpoint)[/dim]")
            
            if start_stage <= 3:
                task = progress.add_task("[cyan]Stage 3: Transforming characters...", total=None)
                
                characters = transform_characters(
                    source_analysis.get('character_archetypes', []),
                    world
                )
                self.artifacts['characters'] = characters
                
                char_mapping = create_character_mapping_table(
                    source_analysis.get('character_archetypes', []),
                    characters
                )
                
                progress.update(task, description="[green]✓ Stage 3: Character transformation complete")
                console.print(f"  → Transformed {len(characters.get('transformed_characters', []))} characters")
                self._save_checkpoint(3, source_name, target_setting)
            else:
                characters = self.artifacts.get('characters', {})
                console.print("[dim]Stage 3: Skipped (loaded from checkpoint)[/dim]")
            
            if start_stage <= 4:
                task = progress.add_task("[cyan]Stage 4: Reconstructing plot...", total=None)
                
                plot = reconstruct_plot(
                    source_analysis.get('plot_structure', {}),
                    characters,
                    world
                )
                self.artifacts['plot'] = plot
                
                validation = validate_cause_effect_chain(plot)
                
                progress.update(task, description="[green]✓ Stage 4: Plot reconstruction complete")
                console.print(f"  → Plot valid: {validation['valid']}")
                if not validation['valid']:
                    console.print(f"  → Issues: {validation['issues']}")
                self._save_checkpoint(4, source_name, target_setting)
            else:
                plot = self.artifacts.get('plot', {})
                console.print("[dim]Stage 4: Skipped (loaded from checkpoint)[/dim]")
            
            if start_stage <= 5:
                task = progress.add_task("[cyan]Stage 5: Checking consistency...", total=None)
                
                consistency = check_consistency(
                    source_analysis,
                    world,
                    characters,
                    plot
                )
                
                score_info = calculate_overall_score(consistency)
                consistency['overall_score'] = score_info
                
                plot, characters, fixes = apply_fixes(consistency, plot, characters)
                
                self.artifacts['consistency'] = consistency
                
                progress.update(task, description="[green]✓ Stage 5: Consistency check complete")
                console.print(f"  → Overall score: {score_info['overall_score']}/10")
                console.print(f"  → Passed: {score_info['passed']}")
                self._save_checkpoint(5, source_name, target_setting)
            else:
                consistency = self.artifacts.get('consistency', {})
                score_info = consistency.get('overall_score', {})
                console.print("[dim]Stage 5: Skipped (loaded from checkpoint)[/dim]")
            
            task = progress.add_task("[cyan]Stage 6: Generating story...", total=None)
            
            story = generate_story(world, characters, plot)
            
            transformation_diff = generate_transformation_diff(
                source_analysis,
                {
                    'world': world,
                    'characters': characters,
                    'plot': plot
                }
            )
            
            self.artifacts['transformation_diff'] = transformation_diff
            
            progress.update(task, description="[green]✓ Stage 6: Story generation complete")
        
        self._clear_checkpoint()
        
        all_artifacts = compile_artifacts(
            source_analysis,
            world,
            characters,
            plot,
            consistency,
            transformation_diff
        )
        
        metadata = {
            'source_title': source_analysis.get('title', source_name),
            'target_world': world.get('world_name', target_setting)
        }
        formatted_story = format_story_markdown(story, metadata)
        
        self._save_outputs(formatted_story, all_artifacts, source_name, target_setting)
        
        console.print(Panel.fit(
            "[bold green]Pipeline Complete![/bold green]\n"
            f"Story saved to: {self.output_dir}/story.md\n"
            f"PDF saved to: {self.output_dir}/story.pdf\n"
            f"Visualization: {self.output_dir}/visualization.md\n"
            f"Artifacts saved to: {self.output_dir}/artifacts.json",
            title="Success"
        ))
        
        return {
            'story': formatted_story,
            'artifacts': all_artifacts
        }
    
    def _save_outputs(self, story: str, artifacts: dict, source: str, target: str):
        os.makedirs(self.output_dir, exist_ok=True)
        
        story_path = os.path.join(self.output_dir, "story.md")
        with open(story_path, 'w', encoding='utf-8') as f:
            f.write(story)
        
        artifacts_path = os.path.join(self.output_dir, "artifacts.json")
        with open(artifacts_path, 'w', encoding='utf-8') as f:
            json.dump(artifacts, f, indent=2, ensure_ascii=False)
        
        viz_report = generate_visualization_report(artifacts)
        viz_path = os.path.join(self.output_dir, "visualization.md")
        with open(viz_path, 'w', encoding='utf-8') as f:
            f.write(viz_report)
        
        summary = self._create_summary(artifacts, source, target)
        summary_path = os.path.join(self.output_dir, "transformation_summary.md")
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        metadata = artifacts.get('metadata', {})
        if not metadata:
            metadata = {'source_title': source, 'target_world': target}
        pdf_path = os.path.join(self.output_dir, "story.pdf")
        story_text = story.split('---\n\n', 1)[-1] if '---' in story else story
        generate_pdf(story_text, metadata, pdf_path)
    
    def _create_summary(self, artifacts: dict, source: str, target: str) -> str:
        stages = artifacts.get('stages', {})
        
        summary = f"""# Transformation Summary

## Source → Target
- **Original**: {source}
- **New World**: {target}

## Character Mapping

| Original | Transformed | Preservation |
|----------|-------------|--------------|
"""
        chars = stages.get('3_character_transformation', {}).get('transformed_characters', [])
        for char in chars[:5]:
            summary += f"| {char.get('original_name', 'N/A')} | {char.get('new_name', 'N/A')} | {char.get('preserved_motivation', 'N/A')[:30]}... |\n"
        
        summary += f"""
## Theme Mapping

"""
        themes = stages.get('2_world_definition', {}).get('theme_mapping', [])
        for theme in themes:
            summary += f"- **{theme.get('original_theme', 'N/A')}** → {theme.get('world_expression', 'N/A')}\n"
        
        summary += f"""
## Quality Scores

"""
        consistency = stages.get('5_consistency_check', {})
        for key in ['thematic_fidelity', 'internal_consistency', 'originality_check', 'cultural_sensitivity']:
            cat = consistency.get(key, {})
            score = cat.get('score', 'N/A')
            summary += f"- {key.replace('_', ' ').title()}: {score}/10\n"
        
        overall = consistency.get('overall_score', {})
        summary += f"\n**Overall Score**: {overall.get('overall_score', 'N/A')}/10\n"
        
        diff = stages.get('6_transformation_diff', {})
        diff_summary = diff.get('transformation_summary', '')
        if diff_summary:
            summary += f"""
## Transformation Approach

{diff_summary}
"""
        
        return summary
