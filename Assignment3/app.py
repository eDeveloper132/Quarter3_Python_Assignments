import streamlit as st
import re
import random
import string

def check_password_strength(password, common_passwords=None):
    score = 0
    feedback = []
    
    # Check against common passwords
    if common_passwords and password.lower() in common_passwords:
        feedback.append("Do not use common passwords like this.")
        return 0, feedback
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")
    
    # Uppercase and Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")
    
    return score, feedback

def generate_strong_password(length=12):
    if length < 8:
        length = 8
    
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = "!@#$%^&*"
    
    # Ensure at least one of each required character type
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Fill the remaining length with random characters
    all_chars = uppercase + lowercase + digits + special
    password += [random.choice(all_chars) for _ in range(length - 4)]
    
    # Shuffle to randomize character positions
    random.shuffle(password)
    
    return ''.join(password)

# Streamlit App
st.title("🔐 Password Strength Meter")
st.write("Enter a password to check its strength or generate a strong password.")

# List of common weak passwords
common_passwords = ["password", "123456", "qwerty", "letmein", "admin", "welcome"]

# Section 1: Check Password Strength
st.subheader("Check Password Strength")
password = st.text_input("Enter your password", type="password")

if st.button("Check Strength"):
    score, feedback = check_password_strength(password, common_passwords)
    
    if score == 4:
        st.success("✅ Strong Password!")
    elif score == 3:
        st.warning("⚠️ Moderate Password - Consider adding more security features.")
    else:
        st.error("❌ Weak Password - Improve it using the suggestions below.")
    
    if feedback:
        st.write("**Suggestions:**")
        for msg in feedback:
            st.write(f"- {msg}")

# Section 2: Generate Strong Password
st.subheader("Generate Strong Password")
length = st.number_input("Password length (min 8)", min_value=8, value=12, step=1)

if st.button("Generate Password"):
    generated_password = generate_strong_password(length)
    st.write(f"**Generated Password:** {generated_password}")
    st.info("Remember to store your password securely.")

# Additional Information
st.write("""
### Why Strong Passwords Matter
- **Protect your data**: Prevent unauthorized access.
- **Enhance security**: Reduce the risk of hacking and identity theft.
- **Safeguard accounts**: Keep your online presence secure.
""")