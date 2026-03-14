# MemoAI 🧠

**MemoAI** is a premium note-taking application that replaces traditional keyword search with **AI-powered semantic retrieval**. It understands the meaning behind your words, allowing you to find notes based on context rather than exact matches.

## 🚀 Key Concepts

### Semantic Search
Instead of basic text matching, this app uses **Vector Embeddings**. 
- Every note is converted into a 384-dimensional mathematical vector.
- When you search, the app calculates the "closeness" between your query and your notes using **Cosine Similarity**.
- This means searching for "Healthy Eating" can successfully find a note titled "Salad Recipes."

### Storage Architecture
The backend is designed to be modular. While the default uses **PostgreSQL**, the logic can be adapted to any storage preference.

1. **Relational Data**: Titles and text are stored in a standard table.
2. **Vector Data**: The AI-generated embeddings are stored as searchable numerical data linked to each note ID.
3. **Custom Implementation**: Developers are encouraged to use the included PostgreSQL logic or swap it for **SQLite** (local file) or **ChromaDB** (vector database).

## 🛠️ Setup & Usage

### Installation
Requires Python 3.9+. Install the core dependencies via pip:
`pip install customtkinter psycopg2 numpy sentence-transformers`

### Configuration
1. **Database**: Provide your credentials in the `Memo` class initialization.
2. **Tables**: Ensure your database has a table for text content and a linked table for vector embeddings.
3. **Execution**: Run `python app.py` to launch the graphical interface.

## 📂 Project Structure
- **`app.py`**: The UI Controller. Manages the modern CustomTkinter interface, live card updates, and user interactions.
- **`MemoAI.py`**: The Logic Engine. Manages the Sentence-Transformer model, database operations, and similarity calculations.

---
*Private. Offline. Intelligent.*
