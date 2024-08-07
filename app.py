import streamlit as st
from utils import extract_text, search_documents, get_user_history, download_history, save_user_query
from database.db_connection import get_db_connection
import bcrypt

conn, cursor = get_db_connection()

def authenticate_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        return True
    return False

def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    st.sidebar.write(f"Welcome, {st.session_state['username']}")

    action = st.sidebar.selectbox("Choose an action", ["Upload Document", "Query Documents", "View History", "Download Chat History"])

    if action == "Upload Document":
        uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
        if uploaded_file:
            text = extract_text(uploaded_file)
            cursor.execute("INSERT INTO documents (content) VALUES (%s)", (text,))
            conn.commit()
            st.success("Document uploaded successfully!")

    elif action == "Query Documents":
        query = st.text_input("Enter your query")
        if query:
            if st.button("Search"):
                results = search_documents(query)
                save_user_query(st.session_state['username'], query, str(results))
                st.write("Results:")
                for result in results:
                    st.write(result[0])

    elif action == "View History":
        history = get_user_history(st.session_state['username'])
        st.write("Your Query History:")
        for entry in history:
            st.write(f"Query: {entry[0]}, Response: {entry[1]}")

    elif action == "Download Chat History":
        if st.button("Download"):
            history = get_user_history(st.session_state['username'])
            download_history(history)
            st.success("Chat history downloaded!")
            st.download_button(
                label="Download Chat History",
                data="\n".join([f"Query: {entry[0]}\nResponse: {entry[1]}" for entry in history]),
                file_name="chat_history.txt",
                mime="text/plain",
            )

else:
    choice = st.sidebar.radio("Select an option", ["Login", "Register"])
    
    if choice == "Login":
        st.header("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

    if choice == "Register":
        st.header("Register")
        new_username = st.text_input("New Username", key="register_username")
        new_password = st.text_input("New Password", type="password", key="register_password")
        if st.button("Register"):
            if register_user(new_username, new_password):
                st.success("Registered successfully! You can now log in.")
            else:
                st.error("Registration failed. Please try again.")
