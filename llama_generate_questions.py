import subprocess
import shutil

# Check if Ollama is installed
if not shutil.which("ollama"):
    raise EnvironmentError("Ollama is not installed. Please install from https://ollama.com")

# Generate questions safely for LaTeX
def generate_questions_with_llm(subject, grade, num_questions, difficulty, topic_focus=None):
    # Define difficulty-specific instructions depending on the subject
    general_easy = """
Focus on basic recall, simple definitions, or basic problem-solving.
Avoid multi-step logic, and keep questions straightforward.
"""
    general_medium = """
Focus on applying concepts, basic reasoning, and short questions.
Include simple multi-step problems or minor critical thinking.
"""
    general_hard = """
Focus on complex reasoning, multi-step problems, proofs, or advanced questions.
Encourage critical thinking, analysis, and synthesis of ideas.
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
- Matching events to outcomes
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
- Vocabulary matching
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

RULES:
- ONLY output clean \\item entries in LaTeX enumerate format.
- Every math/science/technical expression must be wrapped inside inline math mode using \\( ... \\) if applicable.
- Avoid Unicode symbols like √, ∫, etc. Always use LaTeX syntax (\\sqrt{{}}, \\int, etc.).
- Never nest \\( \\( ... \\) \\).
- If writing fractions, always use \\frac{{numerator}}{{denominator}} format, not (numerator)/(denominator).
- Do NOT write explanations or extra sentences outside the questions.

Example output format:

\\item Solve for \\( x \\) in \\( \\frac{{x^2 - 4}}{{x - 2}} = 2 \\)
\\item Find the derivative of \\( f(x) = 3x^2 + 5x - 7 \\)
\\item Name two causes of the American Revolution.

ONLY output the list of \\item entries.

"""
    return prompt

    



