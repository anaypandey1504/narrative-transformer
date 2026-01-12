# AI Narrative Transformation System

A modular AI system that systematically transforms public-domain narratives into alternate universes while preserving thematic essence.

## Features

- **6-Stage Pipeline**: Source abstraction → World building → Character transformation → Plot reconstruction → Consistency check → Story generation
- **Interactive CLI**: Select from 7 classic works, define custom target worlds with rules
- **Multiple Outputs**: Markdown story, PDF, visualization diagram, JSON artifacts
- **Checkpointing**: Resume from failures automatically
- **Schema Validation**: Pydantic validation for LLM outputs

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get API Key (FREE)
Get your free Groq API key at: https://console.groq.com/keys

### 3. Set API Key
```powershell
# Windows PowerShell
$env:GROQ_API_KEY = "your-api-key-here"

# Or create a .env file:
echo "GROQ_API_KEY=your-api-key-here" > .env
```

### 4. Run

**Interactive Mode (Recommended):**
```bash
python run.py
```

**Command Line Mode:**
```bash
python run.py --source "Romeo and Juliet" --target "Silicon Valley AI Labs, 2025"
python run.py --source "Hamlet" --target "Cyberpunk Tokyo, 2077"
python run.py --source "The Odyssey" --target "Interstellar Space Mission"
```

**Custom Source Material:**
```bash
python run.py --source-file my_story.txt --target "Post-apocalyptic Earth"
```

**List Available Sources:**
```bash
python run.py --list-sources
```

## Pipeline Stages

| Stage | Module | Description |
|-------|--------|-------------|
| 1 | `source_abstraction.py` | Extract themes, archetypes, conflicts |
| 2 | `world_definition.py` | Define target universe rules |
| 3 | `character_transform.py` | Map characters to new world |
| 4 | `plot_reconstruction.py` | Rebuild narrative structure |
| 5 | `consistency_check.py` | Verify fidelity and quality |
| 6 | `output_generator.py` | Generate story + artifacts |

## Output Files

Generated stories are saved to `output/` directory:

| File | Description |
|------|-------------|
| `story.md` | The reimagined narrative (Markdown) |
| `story.pdf` | PDF version of the story |
| `visualization.md` | Mermaid diagram + transformation tables |
| `artifacts.json` | All intermediate transformation data |
| `transformation_summary.md` | Human-readable process summary |

## Available Source Materials

1. Romeo and Juliet (Shakespeare, 1597)
2. Hamlet (Shakespeare, 1600)
3. The Odyssey (Homer, 8th century BCE)
4. Dracula (Bram Stoker, 1897)
5. Frankenstein (Mary Shelley, 1818)
6. Cinderella (Traditional, 1697)
7. Macbeth (Shakespeare, 1606)

## Example Transformation

**Input:** Romeo and Juliet → COVID Lockdown India, 2020

**Output:** Characters become online gamers/influencers, forbidden love plays out through digital connections during quarantine, family feuds become rival online communities.

## Project Structure

```
narrative-transformer/
├── run.py                 # CLI entry point
├── config.py              # API configuration
├── pipeline/
│   ├── orchestrator.py    # 6-stage coordinator
│   ├── source_abstraction.py
│   ├── world_definition.py
│   ├── character_transform.py
│   ├── plot_reconstruction.py
│   ├── consistency_check.py
│   ├── output_generator.py
│   ├── visualization.py   # Mermaid diagram generator
│   └── schemas.py         # Pydantic validation
├── prompts/
│   └── templates.py       # All prompt templates
├── data/
│   └── source_materials.json
├── docs/
│   └── solution_design.md
└── tests/
    └── test_validators.py
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Tech Stack

- **LLM**: Groq (Llama 3.3 70B) - Free tier
- **CLI**: Rich library
- **PDF**: FPDF2
- **Validation**: Pydantic
