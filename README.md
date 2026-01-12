# AI Narrative Transformation System

A modular system for systematically transforming public-domain narratives into alternate universes.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get your FREE Groq API key at: https://console.groq.com/keys

3. Set your API key:
```powershell
# Windows PowerShell
$env:GROQ_API_KEY = "your-api-key-here"

# Or create a .env file with:
# GROQ_API_KEY=your-api-key-here
```

## Usage

### Interactive Mode
```bash
python run.py
```

### Command Line Mode
```bash
python run.py --source "Romeo and Juliet" --target "Silicon Valley AI Labs, 2025"
```

### Custom Source Material
```bash
python run.py --source-file "my_story.txt" --target "Cyberpunk Tokyo, 2077"
```

## Pipeline Stages

1. **Source Abstraction** - Extract themes, archetypes, conflicts
2. **World Definition** - Define target universe rules
3. **Character Transform** - Map characters to new world
4. **Plot Reconstruction** - Rebuild narrative structure
5. **Consistency Check** - Verify fidelity and safety
6. **Output Generation** - Produce final story + artifacts

## Output

Generated stories are saved to `output/` directory with:
- `story.md` - The reimagined narrative
- `artifacts.json` - Intermediate transformation data
- `transformation_summary.md` - Human-readable process log

## Powered By

- **Groq** - Ultra-fast inference with Llama 3.3 70B (FREE tier available)
