import PyPDF2
import docx
from database.db_connection import get_db_connection

def extract_text(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    else:
        return file.read().decode("utf-8")

def search_documents(query):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT content FROM documents WHERE content LIKE %s", ('%' + query + '%',))
    results = cursor.fetchall()
    return results

def save_user_query(username, query, response):
    conn, cursor = get_db_connection()
    cursor.execute("INSERT INTO history (username, query, response) VALUES (%s, %s, %s)", (username, query, response))
    conn.commit()

def get_user_history(username):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT query, response FROM history WHERE username = %s", (username,))
    history = cursor.fetchall()
    return history

def download_history(history):
    with open("chat_history.txt", "w", encoding="utf-8") as file:
        for entry in history:
            file.write(f"Query: {entry[0]}\nResponse: {entry[1]}\n\n")
