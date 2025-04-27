# 📚 Worksheet Generator Web App

An interactive Flask-based website to **generate customizable academic worksheets** (Math, Physics, English, History, etc.) using **LaTeX** and **Ollama (local LLM)**.  
Supports generation of **questions, graphs, tables,** and **automatic PDF** output – *no manual command line needed!*

---

## ✨ Features
- 🖥️ Beautiful Web Interface (responsive design)
- 📝 Create worksheets for any **subject** and **grade level**
- 📈 Auto-generate **graphs**, **plots**, **tables**, and **equations** in LaTeX
- ✏️ Select number of **questions** and **difficulty** (easy, medium, hard)
- 📚 Option to specify a **topic focus**
- ⚡ Automatic LaTeX → PDF compilation
- 🖨️ Download both the **PDF** and **.tex source**
- 🛡️ Resilient to small LaTeX errors (no blocking or manual intervention)
- 🐍 100% Python + Flask backend

---

## 🛠 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/worksheet-generator.git
cd worksheet-generator
```

### 2. Set up a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
```

### 3. Install required Python packages
```bash
pip install flask
```

### 4. Install LaTeX
Make sure `pdflatex` is installed and available in your PATH:
- On macOS: 
  ```bash
  brew install mactex
  ```
- On Ubuntu:
  ```bash
  sudo apt install texlive-full
  ```
- On Windows: Install [MiKTeX](https://miktex.org/)

### 5. Install and run Ollama
- Install from: https://ollama.com
- Example to pull a model:
  ```bash
  ollama pull llama3
  ```

---

## 🚀 Usage

### To start the app
```bash
python app.py
```

Then open your browser and go to:
```
http://127.0.0.1:5000
```

✅ Fill out the form with:
- Subject
- Grade
- Difficulty
- Number of questions
- Topic focus
- Number of graphs

Generate your worksheet, preview it, and download the PDF and LaTeX file!

---

## 📂 Project Structure

```
worksheet_generator/
├── app.py               
├── main.py               
├── compile_latex.py      
├── llama_generate_questions.py  
├── validate_latex.py     
├── templates/
│   ├── form.html         
│   └── base_template.tex 
├── outputs/              
└── README.md
```

---

## ⚙️ Configuration Notes

- **Automatic LaTeX error handling:**  
  The LaTeX compilation uses `-interaction=nonstopmode` so minor errors won't stop generation.

- **LaTeX packages already included:**  
  ```latex
  \usepackage{amsmath, amssymb, graphicx, tikz, pgfplots, geometry, array, booktabs}
  ```

- **PDF generation time:**  
  Depends on LLM response but usually ~2–5 seconds.

---

# 🚀 Thank you for using Worksheet Generator!

