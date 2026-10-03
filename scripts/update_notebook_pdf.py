import json
import os

nb_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "notebooks", "RAG_Complete_Practical.ipynb"))

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Update cell 6 (Cell 3: Document Loading)
nb['cells'][6]['source'] = [
    "# ✅ Flexible loader: Loads either PDF or TXT seamlessly using LangChain loaders\n",
    "import os\n",
    "from langchain_community.document_loaders import TextLoader, PyPDFLoader\n",
    "\n",
    "PDF_PATH = os.path.join(DATA_DIR, 'as_a_man_thinketh.pdf')\n",
    "\n",
    "if os.path.exists(PDF_PATH):\n",
    "    print(f'📂 Loading PDF document from: {PDF_PATH}')\n",
    "    loader = PyPDFLoader(PDF_PATH)\n",
    "    documents = loader.load()\n",
    "else:\n",
    "    print(f'📂 Loading TXT document from: {BOOK_PATH}')\n",
    "    loader = TextLoader(BOOK_PATH, encoding='utf-8')\n",
    "    documents = loader.load()\n",
    "\n",
    "total_chars = sum(len(d.page_content) for d in documents)\n",
    "print(f'✅ Loaded {len(documents)} page/document(s)')\n",
    "print(f'📝 Total characters: {total_chars:,}')\n",
    "print(f'🏷️  Metadata (Doc 0): {documents[0].metadata}')\n",
    "print('\\n--- First 300 characters of Doc 0 ---')\n",
    "print(documents[0].page_content[:300].strip())\n"
]

# Update cell 8 (Cell 4: Chunking)
nb['cells'][8]['source'] = [
    "# ✅ RecursiveCharacterTextSplitter from langchain_text_splitters (LangChain 1.x)\n",
    "from langchain_text_splitters import RecursiveCharacterTextSplitter\n",
    "\n",
    "text_splitter = RecursiveCharacterTextSplitter(\n",
    "    chunk_size=800,        # Each chunk: at most 800 characters\n",
    "    chunk_overlap=150,     # 150 characters shared between adjacent chunks\n",
    "    length_function=len,\n",
    "    separators=['\\n\\n', '\\n', ' ', '']  # Try these split points in order\n",
    ")\n",
    "\n",
    "chunks = text_splitter.split_documents(documents)\n",
    "\n",
    "total_doc_chars = sum(len(d.page_content) for d in documents)\n",
    "print(f'📊 Chunking Results:')\n",
    "print(f'   Original : {len(documents)} page/document(s), {total_doc_chars:,} characters')\n",
    "print(f'   After    : {len(chunks)} chunks')\n",
    "print(f'   Average  : {sum(len(c.page_content) for c in chunks) // len(chunks)} chars/chunk')\n",
    "print()\n",
    "\n",
    "for i, chunk in enumerate(chunks[5:8], start=5):\n",
    "    print(f'--- CHUNK #{i} ({len(chunk.page_content)} chars) ---')\n",
    "    print(chunk.page_content)\n",
    "    print()\n"
]

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated successfully!")
