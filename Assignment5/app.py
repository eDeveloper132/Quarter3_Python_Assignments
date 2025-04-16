import streamlit as st
import hashlib
from cryptography.fernet import Fernet

if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}
if 'next_id' not in st.session_state:
    st.session_state.next_id = 1
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'locked_out' not in st.session_state:
    st.session_state.locked_out = False

if 'fernet_key' not in st.session_state:
    st.session_state.fernet_key = Fernet.generate_key()
cipher = Fernet(st.session_state.fernet_key)

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

MASTER_PASSWORD_HASH = hash_passkey("admin123")

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text):
    try:
        return cipher.decrypt(encrypted_text.encode()).decode()
    except Exception as e:
        st.error(f"Decryption failed: {e}")
        return None

st.title("🔒 Secure Data Encryption System")

menu = ["Home", "Store Data", "Retrieve Data", "Delete Data", "Login"]

if st.session_state.locked_out:
    choice = "Login"
else:
    choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")
    st.write("- Navigate to 'Store Data' to encrypt and save your data.")
    st.write("- Use 'Retrieve Data' to decrypt your stored data with the correct passkey.")
    st.write("- Use 'Delete Data' to remove stored data.")
    
    if st.session_state.stored_data:
        st.write("**Stored Data Labels:**")
        for data_id, entry in st.session_state.stored_data.items():
            st.write(f"- {data_id}: {entry['label']}")
    else:
        st.write("No data stored yet.")

elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")
    st.write("**Note:** Remember your passkey, as it will be required to retrieve the data.")
    label = st.text_input("Enter a label for this data")
    user_data = st.text_area("Enter Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if label and user_data and passkey:
            data_id = str(st.session_state.next_id)
            st.session_state.next_id += 1
            encrypted_text = encrypt_data(user_data)
            hashed_passkey = hash_passkey(passkey)
            st.session_state.stored_data[data_id] = {
                "label": label,
                "encrypted_text": encrypted_text,
                "passkey": hashed_passkey
            }
            st.success(f"✅ Data stored securely with ID: {data_id} and label: {label}")
        else:
            st.error("⚠️ All fields are required!")

elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    st.write("**Instructions:** Select the data you want to retrieve and enter the correct passkey to decrypt it.")
    if st.session_state.stored_data:
        options = [f"{data_id}: {st.session_state.stored_data[data_id]['label']}" for data_id in st.session_state.stored_data]
        selected_option = st.selectbox("Select Data", options)
        data_id = selected_option.split(":")[0]
        passkey = st.text_input("Enter Passkey:", type="password")

        if st.button("Decrypt"):
            if passkey:
                hashed_passkey = hash_passkey(passkey)
                stored_entry = st.session_state.stored_data[data_id]
                if stored_entry["passkey"] == hashed_passkey:
                    decrypted_text = decrypt_data(stored_entry["encrypted_text"])
                    if decrypted_text:
                        st.session_state.failed_attempts = 0
                        st.success(f"✅ Decrypted Data: {decrypted_text}")
                else:
                    st.session_state.failed_attempts += 1
                    attempts_left = 3 - st.session_state.failed_attempts
                    st.error(f"❌ Incorrect passkey! Attempts remaining: {attempts_left}")
                    if st.session_state.failed_attempts >= 3:
                        st.session_state.locked_out = True
                        st.warning("🔒 Too many failed attempts! Please log in to continue.")
            else:
                st.error("⚠️ Please enter a passkey.")
    else:
        st.write("No data stored yet.")

elif choice == "Delete Data":
    st.subheader("🗑️ Delete Stored Data")
    if st.session_state.stored_data:
        options = [f"{data_id}: {st.session_state.stored_data[data_id]['label']}" for data_id in st.session_state.stored_data]
        selected_option = st.selectbox("Select Data to Delete", options)
        data_id = selected_option.split(":")[0]
        
        if st.checkbox("Are you sure you want to delete this data?"):
            if st.button("Delete"):
                if data_id in st.session_state.stored_data:
                    del st.session_state.stored_data[data_id]
                    st.success(f"✅ Data with ID {data_id} deleted successfully!")
                else:
                    st.error("❌ Data not found.")
        else:
            st.info("Deletion cancelled.")
    else:
        st.write("No data stored yet.")

elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    login_pass = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if hash_passkey(login_pass) == MASTER_PASSWORD_HASH:
            st.session_state.locked_out = False
            st.session_state.failed_attempts = 0
            st.success("✅ Reauthorized successfully! You can now retrieve data.")
        else:
            st.error("❌ Incorrect password!")