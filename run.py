#!/usr/bin/env python3
import argparse
import sys
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

sys.path.insert(0, '.')

from config import validate_config
from pipeline.orchestrator import NarrativeTransformer
from pipeline.world_definition import get_template_suggestions

console = Console()


def load_source_materials() -> list:
    with open('data/source_materials.json', 'r', encoding='utf-8') as f:
        materials = json.load(f)
    return list(materials.items())


def display_numbered_sources(sources: list) -> None:
    console.print("\n[bold cyan]Available Source Materials:[/bold cyan]\n")
    for i, (key, material) in enumerate(sources, 1):
        console.print(f"  [{i}] {material['title']} ({material['author']}, {material['year']})")
    console.print()


def prompt_source_selection(sources: list) -> tuple:
    while True:
        choice = Prompt.ask("[cyan]Select source material (enter number)[/cyan]")
        
        try:
            index = int(choice)
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")
            continue
        
        if index < 1 or index > len(sources):
            console.print(f"[red]Please enter a number between 1 and {len(sources)}.[/red]")
            continue
        
        return sources[index - 1]


def prompt_world_definition() -> str:
    console.print("\n[bold cyan]Define Your Target World:[/bold cyan]\n")
    
    era = Prompt.ask(
        "  [cyan]Era/Time Period[/cyan]",
        default="Near Future (2050)"
    )
    
    domain = Prompt.ask(
        "  [cyan]Domain/Genre[/cyan]",
        default="Technology"
    )
    
    console.print("\n  [dim]Enter 2-4 world rules or constraints (empty line to finish):[/dim]")
    rules = []
    for i in range(4):
        prompt_text = f"  [cyan]Rule {i + 1}[/cyan]"
        if i >= 2:
            prompt_text += " [dim](optional, press Enter to skip)[/dim]"
        
        rule = Prompt.ask(prompt_text, default="")
        if not rule.strip():
            if i < 2:
                console.print("  [red]Please enter at least 2 rules.[/red]")
                continue
            else:
                break
        rules.append(rule.strip())
    
    rules_text = "; ".join(rules) if rules else "standard genre conventions"
    target = f"{domain} setting, {era}. Rules: {rules_text}"
    
    return target


def show_world_templates() -> None:
    templates = get_template_suggestions()
    
    console.print("\n[bold cyan]Suggested Target Worlds (for inspiration):[/bold cyan]")
    for t in templates:
        console.print(f"  • {t['key']}: {t['description']}")
    console.print()


def interactive_mode() -> None:
    console.print(Panel.fit(
        "[bold cyan]AI Narrative Transformation System[/bold cyan]\n"
        "Transform public-domain stories into alternate universes",
        title="Welcome"
    ))
    
    sources = load_source_materials()
    display_numbered_sources(sources)
    
    source_key, source_material = prompt_source_selection(sources)
    source_title = source_material['title']
    
    console.print(f"\n[green]Selected:[/green] {source_title}")
    
    show_world_templates()
    
    target = prompt_world_definition()
    
    console.print(f"\n[yellow]═══ Transformation Summary ═══[/yellow]")
    console.print(f"  [bold]Source:[/bold] {source_title}")
    console.print(f"  [bold]Target:[/bold] {target}")
    console.print()
    
    confirm = Prompt.ask("Proceed with transformation?", choices=["y", "n"], default="y")
    
    if confirm.lower() != 'y':
        console.print("[red]Cancelled.[/red]")
        return
    
    transformer = NarrativeTransformer()
    try:
        result = transformer.run_pipeline(source_title, target)
        
        console.print("\n[bold green]Story Preview (first 500 chars):[/bold green]")
        console.print(Panel(result['story'][:500] + "...", title="Preview"))
        
        console.print("\n[bold]Full output saved to 'output/' directory[/bold]")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise


def cli_mode(args):
    transformer = NarrativeTransformer(output_dir=args.output)
    
    if args.resume:
        if not transformer.can_resume():
            console.print("[bold red]No checkpoint found to resume from.[/bold red]")
            return
        
        info = transformer.get_checkpoint_info()
        console.print(f"[yellow]Resuming transformation:[/yellow]")
        console.print(f"  Source: {info['source']}")
        console.print(f"  Target: {info['target']}")
        console.print(f"  Last stage: {info['stage']}")
        console.print(f"  Checkpoint: {info['timestamp']}\n")
        
        try:
            result = transformer.run_pipeline(
                source_name=info['source'],
                target_setting=info['target'],
                resume=True
            )
            
            if args.print_story:
                console.print("\n[bold cyan]Generated Story:[/bold cyan]\n")
                console.print(result['story'])
            
            return result
            
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            raise
    
    source = args.source
    target = args.target
    
    source_text = None
    if args.source_file:
        with open(args.source_file, 'r', encoding='utf-8') as f:
            source_text = f.read()
        source = args.source_file
    
    console.print(f"[yellow]Transforming:[/yellow] {source}")
    console.print(f"[yellow]Into:[/yellow] {target}\n")
    
    transformer = NarrativeTransformer(output_dir=args.output)
    
    try:
        result = transformer.run_pipeline(source, target, source_text)
        
        if args.print_story:
            console.print("\n[bold cyan]Generated Story:[/bold cyan]\n")
            console.print(result['story'])
        
        return result
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="AI Narrative Transformation System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--source', '-s',
        help='Name of the source story (e.g., "Romeo and Juliet")'
    )
    
    parser.add_argument(
        '--target', '-t',
        help='Target world/setting (e.g., "Silicon Valley AI Labs, 2025")'
    )
    
    parser.add_argument(
        '--source-file', '-f',
        help='Path to a custom source material text file'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--print-story', '-p',
        action='store_true',
        help='Print the generated story to console'
    )
    
    parser.add_argument(
        '--list-sources',
        action='store_true',
        help='List available source materials and exit'
    )
    
    parser.add_argument(
        '--resume', '-r',
        action='store_true',
        help='Resume from the last checkpoint'
    )
    
    args = parser.parse_args()
    
    # Validate configuration
    try:
        validate_config()
    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        sys.exit(1)
    
    # Handle list sources
    if args.list_sources:
        sources = load_source_materials()
        display_numbered_sources(sources)
        show_world_templates()
        return
    
    # Handle resume mode
    if args.resume:
        cli_mode(args)
        return
    
    # Determine mode
    if args.source and args.target:
        cli_mode(args)
    elif args.source_file and args.target:
        cli_mode(args)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
