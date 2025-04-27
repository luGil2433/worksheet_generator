from llama_generate_questions import generate_questions_with_llm
from compile_latex import compile_latex_to_pdf
from validate_latex import contains_unicode_math, super_fix_latex, clean_llm_output
import os

def load_template():
    with open('templates/base_template.tex', 'r') as f:
        return f.read()

def fill_template(template, title, instructions, questions_latex):
    template = template.replace('{{title}}', title)
    template = template.replace('{{instructions}}', instructions)
    template = template.replace('{{questions}}', questions_latex)
    return template

def main():
    print("Starting the script...")

    # ==== User Inputs ====
    subject = "AP English Literature"
    grade = "9"
    num_questions = 5
    difficulty = "hard"
    worksheet_title = "math worksheet"
    instructions_text = "Answer the following questions carefully."
    topic_focus = "Great Expectations; Jane Eyre"  
    graphs = 0  # Number of questions with graphs or diagrams

    # ==== Generate Questions ====
    print("Generating questions...")
    prompt = generate_questions_with_llm(subject, grade, num_questions, difficulty,graphs, topic_focus=topic_focus,)

    # Run the LLM
    import subprocess
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
        return

    if not questions_latex:
        print("No questions generated. Exiting.")
        return

    # ==== Fix Output ====
    # Step 1: Fix Unicode / Math problems
    questions_latex = super_fix_latex(questions_latex)

    # Step 2: Remove any intro sentences before the first \item
    questions_latex = clean_llm_output(questions_latex)

    # ==== Check for Unicode Problems ====
    if contains_unicode_math(questions_latex):
        print("⚠️ Warning: Unicode math detected after fixing.")
        print(questions_latex)
        return

    # ==== Fill Template ====
    print("Loading template...")
    template = load_template()
    print("Filling template...")
    final_latex = fill_template(template, worksheet_title, instructions_text, questions_latex)

    # ==== Save and Compile ====
    os.makedirs('outputs', exist_ok=True)
    tex_filename = os.path.join('outputs', 'worksheet_generated.tex')

    print("Saving .tex file...")
    with open(tex_filename, 'w') as f:
        f.write(final_latex)

    print("Compiling to PDF...")
    compile_latex_to_pdf(tex_filename)
    print("Done!")

if __name__ == "__main__":
    main()
