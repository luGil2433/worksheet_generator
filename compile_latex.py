import subprocess
import os

def compile_latex_to_pdf(tex_filename):
    try:
        subprocess.run(
            ["pdflatex", "-output-directory=outputs", "-interaction=nonstopmode", tex_filename],
            check=True
        )
        print(f"PDF created successfully for {tex_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling LaTeX: {e}")
