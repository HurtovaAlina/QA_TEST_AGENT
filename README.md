libraries

Python 3.11
│
├── LangChain
├── OpenAI / Gemini
├── GoogleGenerativeAIEmbeddings
├── Pinecone
├── python-docx
├── pandas
├── openpyxl
├── pydantic
├── python-docx
└── python-dotenv

from docx import Document - спеціальна бібліотека для читання docx файлів, які мають 
спеціальний формат Word, всередині якого є структура документа: абзаци, таблиці, заголовки,
стилі, списки, форматування, тощо.

from langchain_core.documents import Document - спеціальна бібліотека для створення 
об'єктів документів, які містять текстовий вміст (page_content) та метадані (metadata). 

Document
├── page_content → текст feature
└── metadata
      └── feature → назва feature

from langchain_text_splitters import RecursiveCharacterTextSplitter - спеціальна бібліотека для 
розбиття документу на міні-документи (chunks) з відповідною логікою.

from langchain_google_genai import GoogleGenerativeAIEmbeddings - бібліотека для преведення текстів у 
вектори(набір чисел)

from langchain_pinecone import PineconeVectorStore - бібліотека для збереження chunks та embeddings в Pinecone

from pinecone import Pinecone, ServerlessSpec - Pinecone - створює векторну базу даних, ServerlessSpec - де ця база 
даних буде працювати

from langchain_google_genai import ChatGoogleGenerativeAI - запускає АІ 

import pandas as pd - бібліотека дозволяє працювати з таблицями Excel sheet → pandas DataFrame

========================================================================================================================
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


Structure
│
├── App
│     └── ingestion ├── INGEST DOCUMENT TO DB
│     └── agents ├── TEST GENERATOR (GENERATE TESTS FROM REQUIREMENTS, FIND EXISTING TESTS, GENERATE MISSING TEST)
│     └── model
│     └── rag ├── LOAD DOCUMENT SPLIT INTO FEATURES AND CONTENT
│             ├── SPLIT DOCUMENT TO SMALL PIECES (CHUNKS)
│             ├── EMBEDDINGS (TURNS TEXT TO VECTOR)
│             ├── VECTOR STORE (SAVES EMBEDDINGS)
│             ├── DELETE RECORD 
│
│     
│
│     └── tools ├── SEARCH TOOL
│               ├── SEARCH RECORD IN PINECONE
│               ├── EXCEL LOADER (LOADS .xlx DOCUMENT)
│               ├── TEST CASES LOADER (DATA FRAME -> TO TEST CASE)
│               ├── EXCEL WRITER (ADDS TO EXCEL FILE GENERATED TESTS)
│
│     └── config.py (GETS API KEYS)
│     └── main.py
│
└── data
      └── FDD ├── DOCUMENT WITH REQUIREMENTS
      └── testcases ├── DOCUMENT WITH EXISTING TEST CASES

 FLOW:
FDD
 │
 ▼
RAG / Search
 │
 ▼
Requirements
 │
 ├───────────────┐
 │               │
 ▼               ▼
FDD content    Existing Test Cases
 │               │
 └───────┬───────┘
         ▼
   TEST GENERATOR
         │
         ▼
  Compare by CONTENT
         │
         ▼
Only missing checks
         │
         ▼
New Test Cases 