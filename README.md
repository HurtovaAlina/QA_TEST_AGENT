# 🤖 QA Test Agent

AI-powered QA assistant that analyzes requirements from FDD documents, searches existing test cases, compares them by meaning/content, and generates only the missing test cases.

---

## 🎯 Project Goal

The main goal of the project is to automate part of the QA test case creation process.

The agent:

1. Reads requirements from an FDD document.
2. Splits the document into features and smaller chunks.
3. Converts chunks into vector embeddings.
4. Stores embeddings in Pinecone Vector DB.
5. Searches for relevant requirements.
6. Loads existing test cases from Excel.
7. Compares existing test cases with the requirements by **content/meaning**, not only by exact wording.
8. Identifies missing test coverage.
9. Generates new test cases using Gemini.
10. Allows generated test cases to be added back to the Excel file.

---

# 🛠️ Libraries & Technologies

```text
Python 3.11
│
├── LangChain
├── Google Gemini
├── GoogleGenerativeAIEmbeddings
├── Pinecone
├── python-docx
├── pandas
├── openpyxl
├── pydantic
├── python-dotenv
└── Streamlit
```

---

## 📚 Main Libraries

### `python-docx`

```python
from docx import Document
```

Used for reading `.docx` Word documents.

A Word document has an internal structure containing:

- paragraphs
- tables
- headings
- styles
- lists
- formatting

In this project it is used to read the FDD document containing requirements.

---

### `LangChain Document`

```python
from langchain_core.documents import Document
```

Used to create document objects containing text content and metadata.

The project uses:

```text
Document
├── page_content → text of the feature/chunk
└── metadata
      └── feature → feature name
```

Example:

```python
Document(
    page_content="User must enter a valid phone number...",
    metadata={
        "feature": "User Registration"
    }
)
```

The metadata allows the project to keep information about which feature the text belongs to.

---

### `RecursiveCharacterTextSplitter`

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

Used to split large documents into smaller pieces called **chunks**.

```text
Large FDD document
        │
        ▼
   Feature content
        │
        ▼
 RecursiveCharacterTextSplitter
        │
        ├── Chunk 1
        ├── Chunk 2
        ├── Chunk 3
        └── Chunk 4
```

Chunks make the documents easier to search and process using embeddings.

---

### `GoogleGenerativeAIEmbeddings`

```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings
```

Used to convert text into numerical vectors called **embeddings**.

```text
Text
 │
 ▼
GoogleGenerativeAIEmbeddings
 │
 ▼
Vector
[0.012, -0.245, 0.731, ...]
```

These vectors represent the semantic meaning of the text and allow similar requirements to be found.

---

### `PineconeVectorStore`

```python
from langchain_pinecone import PineconeVectorStore
```

Used to store:

- document chunks
- embeddings
- metadata

inside Pinecone Vector Database.

```text
Chunk
  │
  ▼
Embedding
  │
  ▼
Pinecone
  │
  ├── Vector
  ├── Text
  └── Metadata
```

---

### `Pinecone`

```python
from pinecone import Pinecone, ServerlessSpec
```

`Pinecone` is used to create and connect to the vector database.

`ServerlessSpec` defines where the Pinecone index runs.

Example:

```python
ServerlessSpec(
    cloud="aws",
    region="us-east-1"
)
```

---

### `ChatGoogleGenerativeAI`

```python
from langchain_google_genai import ChatGoogleGenerativeAI
```

Used to communicate with the Gemini AI model.

The model is responsible for tasks such as:

- analyzing requirements
- checking test coverage
- comparing test cases
- generating missing test cases

---

### `pandas`

```python
import pandas as pd
```

Used for working with Excel data.

An Excel sheet can be loaded into a pandas `DataFrame`.

```text
Excel Sheet
     │
     ▼
pandas
     │
     ▼
DataFrame
```

The project uses pandas to process existing test cases.

---

### `openpyxl`

Used for reading and writing Excel `.xlsx` files.

It is especially useful when the project needs to preserve the Excel workbook structure and add generated test cases.

---

### `python-dotenv`

Used for loading environment variables from `.env`.

Example:

```text
GEMINI_API_KEY=...
PINECONE_API_KEY=...
```

The keys are loaded in:

```text
app/config.py
```

---

### `Streamlit`

```python
import streamlit as st
```

Used to create the graphical user interface for the project.

Instead of interacting only through the terminal, the user can enter requirements and view the analysis through a web interface.

---

# 🗄️ Vector Database

The project uses **Pinecone** as a Vector Database.

The database contains requirements from different features.

```text
Vector DB
│
├── Browse Prices
│     └── requirements...
│
├── Browse Inventory
│     └── requirements...
│
├── Deals
│     └── requirements...
│
└── Categories
      └── requirements...
```

Each requirement is stored together with its embedding and metadata.

This allows semantic search.

---

# 📁 Project Structure

```text
QA_TEST_AGENT/
│
├── app/
│   │
│   ├── ingestion/
│   │   └── ingest_fdd.py
│   │       └── INGEST DOCUMENT TO DB
│   │
│   ├── agents/
│   │   └── test_generator.py
│   │       └── TEST GENERATOR
│   │           ├── Generate tests from requirements
│   │           ├── Find existing tests
│   │           └── Generate missing tests
│   │
│   ├── rag/
│   │   ├── document_loader.py
│   │   │   └── LOAD DOCUMENT
│   │   │       SPLIT INTO FEATURES AND CONTENT
│   │   │
│   │   ├── splitter.py
│   │   │   └── SPLIT DOCUMENT TO SMALL PIECES
│   │   │       (CHUNKS)
│   │   │
│   │   ├── embeddings.py
│   │   │   └── TURNS TEXT INTO VECTOR
│   │   │
│   │   ├── vector_store.py
│   │   │   └── SAVES EMBEDDINGS TO PINECONE
│   │   │
│   │   └── delete_record.py
│   │       └── DELETE RECORD FROM VECTOR DB
│   │
│   ├── prompts/
│   │   ├── prompt files
│   │   │   └── TEXT FILES WITH PROMPTS
│   │   │
│   │   └── prompt_loader.py
│   │       └── LOADS PROMPTS
│   │
│   ├── tools/
│   │   ├── search.py
│   │   │   └── SEARCH TOOL
│   │   │
│   │   ├── search_tool.py
│   │   │   └── SEARCH RECORD IN PINECONE
│   │   │
│   │   ├── excel_loader.py
│   │   │   └── LOADS .XLSX DOCUMENT
│   │   │
│   │   ├── test_cases_loader.py
│   │   │   └── DATAFRAME → TEST CASES
│   │   │
│   │   └── excel_writer.py
│   │       └── ADDS GENERATED TEST CASES
│   │           TO EXCEL FILE
│   │
│   ├── config.py
│   │   └── GETS API KEYS
│   │
│   ├── main.py
│   │   └── MAIN APPLICATION
│   │
│   └── streamlit_app.py
│       └── STREAMLIT UI
│
├── data/
│   │
│   ├── fdd/
│   │   └── BEES_Customer.docx
│   │       └── DOCUMENT WITH REQUIREMENTS
│   │
│   └── testcases/
│       └── Testcases.xlsx
│           └── EXISTING TEST CASES
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🔄 Application Flow

```text
                         FDD
                          │
                          ▼
                    Document Loader
                          │
                          ▼
                     Split Features
                          │
                          ▼
                     Split into Chunks
                          │
                          ▼
                      Embeddings
                          │
                          ▼
                    Pinecone Vector DB
                          │
                          │
                          ▼
                    RAG / Semantic Search
                          │
                          ▼
                     Requirements
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
        FDD Content             Existing Test Cases
              │                       │
              │                       │
              └───────────┬───────────┘
                          ▼
                    TEST GENERATOR
                          │
                          ▼
                  Compare by Content
                          │
                          ▼
                 Check Test Coverage
                          │
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼
              Covered           Missing
                 │                 │
                 │                 ▼
                 │          Generate New Tests
                 │                 │
                 └────────┬────────┘
                          ▼
                    Test Cases
                          │
                          ▼
                    Excel Writer
                          │
                          ▼
                   Testcases.xlsx
```

---

# 🧠 How Test Coverage Works

The project does not simply compare test case titles.

It compares the **meaning and content** of the test cases.

### Requirement

```text
User must be able to log in using a phone number.
```

### Existing Test Case

```text
Verify that the user can authenticate using a registered phone number.
```

Although the wording is different, the test covers the same requirement.

Therefore:

```text
Requirement
     │
     ▼
Semantic comparison
     │
     ▼
Existing test covers requirement
     │
     ▼
No new test required
```

If the existing tests do not cover a requirement:

```text
Requirement
     │
     ▼
Search existing test cases
     │
     ▼
No sufficient coverage
     │
     ▼
Gemini generates missing test case
```

---

# 🤖 Test Generator

The Test Generator is responsible for:

### 1. Requirement Analysis

The agent receives a requirement retrieved from the FDD.

### 2. Existing Test Search

Existing test cases are loaded from Excel and provided to the agent for comparison.

### 3. Coverage Check

The agent determines whether the requirement is already covered.

```text
Requirement
     │
     ▼
Existing Test Cases
     │
     ▼
Coverage Analysis
     │
     ├── Covered
     │
     └── Not Covered
```

### 4. Missing Test Generation

If the requirement is not sufficiently covered, Gemini generates a new test case.

---

# 📄 Input Data

## FDD

Requirements are stored in:

```text
data/fdd/
```

Example:

```text
data/fdd/BEES_Customer.docx
```

The FDD is processed using `python-docx`.

---

## Existing Test Cases

Existing test cases are stored in:

```text
data/testcases/
```

Example:

```text
data/testcases/Testcases.xlsx
```

Excel sheets contain existing QA test cases.

The workbook is loaded with pandas and openpyxl.

---

# 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

The `.env` file should **not** be committed to Git.

Make sure it is included in `.gitignore`:

```text
.env
.venv/
__pycache__/
```

---

# 🚀 Installation

Clone the repository and create a virtual environment:

```bash
python3.11 -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 📥 FDD Ingestion

FDD ingestion is a separate process.

The document is processed as follows:

```text
DOCX
 │
 ▼
Load document
 │
 ▼
Identify features
 │
 ▼
Split into chunks
 │
 ▼
Generate embeddings
 │
 ▼
Store in Pinecone
```

Run the ingestion process before using semantic search if the FDD has not yet been added to the database.

---

# ▶️ Running the Application

## Terminal Version

Run:

```bash
python -m app.main
```

---

## Streamlit Version

Run:

```bash
streamlit run app/streamlit_app.py
```

The Streamlit application provides a graphical interface for working with the QA Test Agent.

---

# 🖥️ Streamlit Interface

The Streamlit UI allows the user to:

- enter a requirement
- search relevant FDD content
- identify the feature
- find existing test cases
- check test coverage
- generate missing test cases
- add generated test cases to Excel

```text
User
 │
 ▼
Streamlit UI
 │
 ▼
Requirement
 │
 ▼
RAG Search
 │
 ▼
Existing Test Cases
 │
 ▼
Coverage Check
 │
 ├── Covered → Show existing coverage
 │
 └── Missing → Generate test
                    │
                    ▼
              Add to Excel
```

---

# 📦 Main Components

| Component | Responsibility |
|---|---|
| `ingestion` | Loads FDD documents into Vector DB |
| `agents` | AI logic and test generation |
| `rag` | Document processing and embeddings |
| `prompts` | Stores and loads AI prompts |
| `tools` | Search, Excel loading and writing |
| `config.py` | API configuration |
| `main.py` | Main application flow |
| `streamlit_app.py` | Web UI |
| `data/fdd` | FDD requirements |
| `data/testcases` | Existing test cases |

---

# 🔍 RAG Architecture

The project uses a Retrieval-Augmented Generation approach.

```text
                 FDD DOCUMENT
                      │
                      ▼
              Document Loader
                      │
                      ▼
                   Chunks
                      │
                      ▼
                 Embeddings
                      │
                      ▼
                Pinecone DB
                      │
                      │
                      ▼
                User Requirement
                      │
                      ▼
                 Semantic Search
                      │
                      ▼
             Relevant FDD Content
                      │
                      ▼
                  Gemini LLM
                      │
                      ▼
               Generated Result
```

RAG allows the AI model to use the actual project requirements instead of relying only on its general knowledge.

---

# 📌 Why Vector Database?

Traditional keyword search might fail when two texts use different words but have the same meaning.

For example:

```text
Requirement:
"Customer can authenticate with a phone number."

Test Case:
"Verify that the user can log in using a registered mobile number."
```

Keyword matching may not consider these texts identical.

Vector search can identify that they are semantically similar.

This is important for checking duplicate or missing test coverage.

---

# 🧩 Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Main programming language |
| LangChain | LLM / RAG framework |
| Gemini | LLM and embeddings |
| Pinecone | Vector database |
| python-docx | DOCX processing |
| pandas | Excel / DataFrame processing |
| openpyxl | Excel file manipulation |
| python-dotenv | Environment variables |
| Streamlit | User interface |

---

# 🔮 Future Improvements

Possible future improvements:

- Better semantic test case comparison
- Test case similarity scoring
- Automatic duplicate detection
- More advanced FDD parsing
- Support for multiple FDD documents
- Support for multiple countries
- Automatic feature detection
- Test case prioritization
- Integration with Jira
- Integration with TestRail
- Automatic regression test selection
- Better reporting and coverage statistics

---

# 👩‍💻 Project Purpose

This project is a learning and practical QA automation project that combines:

```text
QA
+
Python
+
LLMs
+
RAG
+
Vector Databases
+
Test Case Generation
+
Test Automation
```

The final goal is to create an AI assistant that can help QA engineers understand requirements, identify existing test coverage, and generate missing test cases without creating unnecessary duplicates.
