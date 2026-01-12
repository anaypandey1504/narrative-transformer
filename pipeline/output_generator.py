import json
from groq import Groq
from prompts.templates import STORY_GENERATION_PROMPT, TRANSFORMATION_DIFF_PROMPT
from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE, MAX_OUTPUT_TOKENS
from pipeline.utils import parse_llm_json, make_llm_call


def generate_story(world: dict, characters: dict, plot: dict) -> str:
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = STORY_GENERATION_PROMPT.format(
        world=json.dumps(world, indent=2),
        characters=json.dumps(characters.get('transformed_characters', []), indent=2),
        plot=json.dumps(plot.get('reconstructed_plot', {}), indent=2)
    )
    
    return make_llm_call(
        client=client,
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a master storyteller. Write engaging, vivid prose."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=MAX_OUTPUT_TOKENS
    )


def generate_transformation_diff(original_analysis: dict, transformation: dict) -> dict:
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = TRANSFORMATION_DIFF_PROMPT.format(
        original=json.dumps(original_analysis, indent=2),
        transformed=json.dumps(transformation, indent=2)
    )
    
    try:
        response_content = make_llm_call(
            client=client,
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a narrative analyst. Always respond with valid JSON only, no markdown."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return parse_llm_json(response_content)
    except Exception:
        return {"transformation_diff": [], "transformation_summary": "Unable to generate diff"}


def compile_artifacts(
    source_analysis: dict,
    world: dict,
    characters: dict,
    plot: dict,
    consistency: dict,
    transformation_diff: dict
) -> dict:
    return {
        "pipeline_version": "1.0.0",
        "stages": {
            "1_source_abstraction": source_analysis,
            "2_world_definition": world,
            "3_character_transformation": characters,
            "4_plot_reconstruction": plot,
            "5_consistency_check": consistency,
            "6_transformation_diff": transformation_diff
        },
        "metadata": {
            "source_title": source_analysis.get('title', 'Unknown'),
            "target_world": world.get('world_name', 'Unknown'),
            "overall_score": consistency.get('overall_score', {})
        }
    }


def format_story_markdown(story: str, metadata: dict) -> str:
    header = f"""# {metadata.get('target_world', 'Reimagined Story')}

*A transformation of "{metadata.get('source_title', 'Unknown')}"*

---

"""
    return header + story


def generate_pdf(story: str, metadata: dict, output_path: str) -> str:
    from fpdf import FPDF
    
    class StoryPDF(FPDF):
        def header(self):
            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 10, 'AI Narrative Transformation System', 0, 1, 'C')
            self.ln(5)
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    pdf = StoryPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.set_font('Helvetica', 'B', 20)
    title = metadata.get('target_world', 'Reimagined Story')
    pdf.multi_cell(0, 12, title, 0, 'C')
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'I', 12)
    subtitle = f"A transformation of \"{metadata.get('source_title', 'Unknown')}\""
    pdf.cell(0, 10, subtitle, 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_draw_color(100, 100, 100)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(10)
    
    pdf.set_font('Helvetica', '', 11)
    
    def sanitize_text(text):
        replacements = {
            '\u2013': '-',
            '\u2014': '--',
            '\u2018': "'",
            '\u2019': "'",
            '\u201c': '"',
            '\u201d': '"',
            '\u2026': '...',
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        return text.encode('latin-1', 'replace').decode('latin-1')

    paragraphs = story.split('\n\n')
    for para in paragraphs:
        para = para.strip()
        if para:
            para = para.replace('**', '').replace('*', '').replace('#', '')
            para = sanitize_text(para)
            pdf.multi_cell(0, 7, para)
            pdf.ln(5)
    
    pdf.output(output_path)
    return output_path
