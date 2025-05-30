from llama_generate_questions import generate_questions_with_llm
from compile_latex import compile_latex_to_pdf
from validate_latex import contains_unicode_math, super_fix_latex, clean_llm_output
import os
import subprocess

def load_template():
    with open('templates/base_template.tex', 'r') as f:
        return f.read()

def fill_template(template, title, instructions, questions_latex):
    template = template.replace('{{title}}', title)
    template = template.replace('{{instructions}}', instructions)
    template = template.replace('{{questions}}', questions_latex)
    return template

def generate_worksheet(subject, grade, difficulty, num_questions, topic_focus, graphs):
    print("Generating worksheet...")

    worksheet_title = f"{subject} Worksheet"
    instructions_text = "Answer the following questions carefully."

    # Generate prompt
    prompt = generate_questions_with_llm(subject, grade, num_questions, difficulty, graphs, topic_focus=topic_focus)

    # Run LLM
    try:
        result = subprocess.run(
            ['ollama', 'run', 'llama3'],
            input=prompt,
            capture_output=True,
            text=True,
            check=True
        )
        questions_latex = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running LLM: {e}")
        return None

    if not questions_latex:
        print("No questions generated. Exiting.")
        return None

    # Fix LaTeX
    questions_latex = super_fix_latex(questions_latex)
    questions_latex = clean_llm_output(questions_latex)

    if contains_unicode_math(questions_latex):
        print("Unicode math detected after fixing.")
        print(questions_latex)
        return None

    # Fill template
    template = load_template()
    final_latex = fill_template(template, worksheet_title, instructions_text, questions_latex)

    # Save and compile
    os.makedirs('outputs', exist_ok=True)
    tex_filename = os.path.join('outputs', 'worksheet_generated.tex')
    pdf_filename = os.path.join('outputs', 'worksheet_generated.pdf')

    with open(tex_filename, 'w') as f:
        f.write(final_latex)

    compile_latex_to_pdf(tex_filename)

    return pdf_filename
