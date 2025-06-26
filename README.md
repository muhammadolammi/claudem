# 🤖 CLAUDEM – AI Agent Powered by Google Gemini API

**Claudem** is a lightweight AI agent that leverages Google’s Gemini API to generate intelligent responses from user input. It’s designed for modularity, simplicity, and ease of integration into larger systems — making it an excellent foundation for real-world AI assistant projects.

---

## 🚀 Features

- 🔑 Secure API handling via `.env` and `python-dotenv`
- ✍️ Text content generation using Gemini's powerful language model
- 🔧 Clean, modular structure for maintainability and scalability
- 🧪 Includes test file for validating core logic
- ✅ CLI support with optional verbose mode

---

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/claudem.git
cd claudem
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory and add your Google Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## 🧠 Usage

You can run the AI agent from the command line:

```bash
python main.py "What is the capital of France?"
```

To run in verbose mode:

```bash
python main.py "Explain how photosynthesis works" --verbose
```

---

## 🧪 Run Tests

Basic functionality tests can be run using:

```bash
python tests.py
```

---

## 📁 Project Structure

```
claudem/
├── main.py                 # Entry point for CLI interaction
├── generate_content.py     # Core logic to call Gemini API
├── functions/              # Utility modules (expandable)
├── tests.py                # Simple test suite
├── .env                    # API key (not committed)
├── .gitignore              # Standard ignores
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

---

## 💼 Why This Project?

This project demonstrates:
- API integration and secure credential management
- CLI tooling for real-world developer workflows
- Clean code organization and modular architecture
- Practical application of AI in software systems

**Perfect for backend roles, AI tooling, or full-stack developer positions.**

---

## 👨‍💻 Author

**Muhammad Olamide**  
Passionate about building robust AI and backend systems with Python and Go.