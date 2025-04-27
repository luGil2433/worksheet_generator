import subprocess
import shutil


# Check if Ollama is installed
if not shutil.which("ollama"):
    raise EnvironmentError("Ollama is not installed. Please install from https://ollama.com")

# Generate questions safely for LaTeX
def generate_questions_with_llm(subject, grade, num_questions, difficulty, graphs,topic_focus=None):
    # Define difficulty-specific instructions depending on the subject
    general_easy = """
Focus on basic recall, simple definitions, or basic problem-solving.
Avoid multi-step logic, and keep questions straightforward.
Real graphs, plots, tables or diagrams drawn using LaTeX should be simple and easy to interpret.
"""
    general_medium = """
Focus on applying concepts, basic reasoning, and short questions.
Include simple multi-step problems or minor critical thinking. 
Real graphs, plots, tables or diagrams drawn using LaTeX should contain some interpretation 
and some level of complexity.
"""
    general_hard = """
Focus on complex reasoning, multi-step problems, proofs, or advanced questions.
Encourage critical thinking, analysis, and synthesis of ideas.
Real graphs, plots, tables or diagrams drawn using LaTeX should be complex and required reasoning 
and deep understanding of the topic in question.
"""

    subject_instructions = {
        "Mathematics": {
            "easy": """
Focus on simple math problems:
- Solving for x
- Basic addition, subtraction, multiplication
- Simplify basic expressions
""",
            "medium": """
Focus on intermediate problems:
- Derivatives of polynomials
- Basic definite integrals
- Evaluate simple limits
""",
            "hard": """
Focus on advanced math problems:
- Chain rule, product rule
- Complex definite integrals
- Optimization or related rates problems
"""
        },
        "Physics": {
            "easy": """
Focus on basic concepts:
- Definitions (force, energy, velocity)
- Unit conversions
- Simple formulas (F=ma)
""",
            "medium": """
Focus on applying formulas:
- Calculating forces, work, energy
- Simple motion problems
- Conceptual questions about Newton's Laws
""",
            "hard": """
Focus on complex reasoning:
- Multi-body systems
- Advanced energy conservation problems
- Circuit analysis
"""
        },
        "Chemistry": {
            "easy": """
Focus on basic recall:
- Naming elements
- Simple chemical equations
- Basic periodic table questions
""",
            "medium": """
Focus on application:
- Balance chemical reactions
- Stoichiometry problems
- Identify types of chemical bonds
""",
            "hard": """
Focus on advanced concepts:
- Thermodynamics calculations
- Reaction mechanisms
- Acid-base titration problems
"""
        },
        "Biology": {
            "easy": """
Focus on definitions:
- Parts of a cell
- Major organ systems
- Basic food chains
""",
            "medium": """
Focus on basic understanding:
- Function of cell organelles
- Systems interactions (e.g., respiratory/circulatory)
- Simple genetics (Punnett squares)
""",
            "hard": """
Focus on deep understanding:
- Molecular biology processes (transcription, translation)
- Evolutionary theory application
- Detailed ecosystem dynamics
"""
        },
        "History": {
            "easy": """
Focus on simple recall:
- Names, dates, events
- Important figures
""",
            "medium": """
Focus on cause and effect:
- Short paragraph explanations
- Matching events to outcomes in a tables format

""",
            "hard": """
Focus on analysis:
- Comparing movements across periods
- Essay prompts about historical significance
"""
        },
        "English": {
            "easy": """
Focus on simple exercises:
- Vocabulary matching utilizing a table format
- Fill-in-the-blank grammar
- Short sentence correction
""",
            "medium": """
Focus on short passages:
- Reading comprehension questions
- Identifying parts of speech
""",
            "hard": """
Focus on analysis:
- Short essay questions
- Literary devices identification
- Argument evaluation
"""
        }
    }

    # Set default difficulty instructions if subject is not predefined
    subject_block = subject_instructions.get(subject, {
        "easy": general_easy,
        "medium": general_medium,
        "hard": general_hard
    })

    difficulty_key = difficulty.lower()

    difficulty_instructions = subject_block.get(difficulty_key, general_medium)  # Default to medium if typo

    # Now build the full flexible prompt
    prompt = f"""
You are an educational worksheet generator.

Create {num_questions} questions about {subject} about this topic {topic_focus} for grade {grade} students at {difficulty} difficulty level.

{difficulty_instructions}
If possible, include a maximum of {graphs} questions that show real graphs, plots, tables or diagrams drawn using LaTeX pgfplots.


RULES:
- ONLY output clean \\item entries in LaTeX enumerate format.
- Every math/science/technical expression must be wrapped inside inline math mode using \\( ... \\) if applicable.
- Avoid Unicode symbols like √, ∫, etc. Always use LaTeX syntax (\\sqrt{{}}, \\int, etc.).
- Never nest \\( \\( ... \\) \\).
- If writing fractions, always use \\frac{{numerator}}{{denominator}} format, not (numerator)/(denominator).
- Do NOT include introductions, summaries, or extra explanations.
- ONLY output the list of \\item entries.

EXAMPLES:

\\item Solve for \\( x \\) in \\( \\frac{{x^2 - 4}}{{x - 2}} = 2 \\).

\\item Find the derivative of \\( f(x) = 3x^2 + 5x - 7 \\).

\\item Sketch the graph of \\( y = \\sin(x) \\) from \\( 0 \\) to \\( 2\\pi \\).

\\item Given the table below, determine the median value:

\\[
\\begin{{array}}{{|c|c|c|}}
\\hline
Value & Frequency \\\\
\\hline
2 & 3 \\\\
4 & 5 \\\\
6 & 2 \\\\
8 & 1 \\\\
\\hline
\\end{{array}}
\\]

\\item Read the following excerpt and identify two literary devices used.

\\item Compare the causes of the American Revolution and the French Revolution in a short paragraph.

\\item Plot the scatter diagram of the following points and find the line of best fit:

\\[
(1,2), (2,3), (3,5), (4,7)
\\]

\item Plot the scatter plot of the points: (1,2), (2,3), (3,5), (4,7).

\item Balance the chemical reaction: \( \text{{C}}_3\text{{H}}_8 + \text{{O}}_2 \rightarrow \text{{CO}}_2 + \text{{H}}_2\text{{O}} \).

\item Given a bar graph showing monthly sales of Products A, B, C, identify the month with the highest sales for Product B.

\item Read the following passage and identify the tone used by the author.

\item Write a short essay discussing the influence of the Enlightenment on modern political systems.

\item Sketch the graph of \( y = \sqrt{{x}} \) between \( 0 \) and \( 4 \).

\item Using the timeline, order the events of the American Revolution.

\item A car starts from rest and accelerates uniformly at \( 2 \, \text{{m/s}}^2 \). Find its velocity after \( 5 \) seconds.

\item Analyze the following graph of \( y = e^{{-x^2}} \) and determine at which points the function changes concavity.

\item Given the table of GDP growth rates by country, calculate the average growth rate.

ONLY output the list of \\item entries.
"""
    return prompt

    



