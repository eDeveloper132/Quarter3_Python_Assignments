import streamlit as st
import json
from streamlit_javascript import st_javascript

def load_library():
    """Load the library from local storage."""
    try:
        library_json = st_javascript("return localStorage.getItem('library');")
        if library_json and library_json != "null":
            return json.loads(library_json)
        return []
    except Exception as e:
        st.error(f"Error loading library: {e}")
        return []

def save_library(library):
    """Save the library to local storage."""
    try:
        library_json = json.dumps(library)
        st_javascript(f"localStorage.setItem('library', `{library_json}`);")
    except Exception as e:
        st.error(f"Error saving library: {e}")

st.title("📚 Personal Library Manager")
st.write("Manage your book collection with data stored in your browser's local storage.")

if 'library' not in st.session_state:
    st.session_state.library = load_library()

action = st.sidebar.selectbox("Choose an action", ["Add a book", "Remove a book", "Search for a book", "Display all books", "Display statistics"])

if action == "Add a book":
    st.header("Add a Book")
    title = st.text_input("Enter the book title")
    author = st.text_input("Enter the author")
    year = st.number_input("Enter the publication year", min_value=0, step=1)
    genre = st.text_input("Enter the genre")
    read = st.checkbox("Have you read this book?")
    
    if st.button("Add Book"):
        if title and author and genre:
            book = {
                "title": title,
                "author": author,
                "year": int(year),
                "genre": genre,
                "read": read
            }
            st.session_state.library.append(book)
            save_library(st.session_state.library)
            st.success("Book added successfully!")
        else:
            st.error("Please fill in all required fields (title, author, genre).")

elif action == "Remove a book":
    st.header("Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        if title:
            for book in st.session_state.library:
                if book["title"].lower() == title.lower():
                    st.session_state.library.remove(book)
                    save_library(st.session_state.library)
                    st.success("Book removed successfully!")
                    break
            else:
                st.error("Book not found.")
        else:
            st.error("Please enter a title.")

elif action == "Search for a book":
    st.header("Search for a Book")
    search_by = st.selectbox("Search by", ["Title", "Author"])
    search_term = st.text_input("Enter the search term")
    if st.button("Search"):
        if search_term:
            matches = []
            if search_by == "Title":
                matches = [book for book in st.session_state.library if search_term.lower() in book["title"].lower()]
            elif search_by == "Author":
                matches = [book for book in st.session_state.library if search_term.lower() in book["author"].lower()]
            if matches:
                st.write("**Matching Books:**")
                for book in matches:
                    read_status = "Read" if book["read"] else "Unread"
                    st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
            else:
                st.warning("No matching books found.")
        else:
            st.error("Please enter a search term.")

elif action == "Display all books":
    st.header("Your Library")
    if st.session_state.library:
        st.write("**All Books:**")
        for book in st.session_state.library:
            read_status = "Read" if book["read"] else "Unread"
            st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
    else:
        st.info("Your library is empty.")

elif action == "Display statistics":
    st.header("Library Statistics")
    total_books = len(st.session_state.library)
    if total_books > 0:
        read_books = sum(1 for book in st.session_state.library if book["read"])
        percentage_read = (read_books / total_books) * 100
        st.write(f"**Total books:** {total_books}")
        st.write(f"**Percentage read:** {percentage_read:.1f}%")
    else:
        st.info("Your library is empty.")