import streamlit as st
import re

# Page configuration
st.set_page_config(page_title="Password Strength Checker",
                   page_icon=":lock:", layout="wide")

# Title
st.title("🤔 Do you think you have a strong password?")
st.subheader("🔒 Check your password strength and generate a strong password here!")

# Function to generate a strong password


def generate_strong_password():
    import random
    import string
    length = 12
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = "".join(random.choice(characters) for _ in range(length))
    return password

# Function to copy text to clipboard


def safe_copy(text):
    """Safe clipboard copy with fallback"""
    try:
        import pyperclip
        pyperclip.copy(text)
        st.toast("Copied to clipboard!", icon="✅")
    except Exception as e:
        st.code(text)


# Sidebar for additional info
with st.sidebar:
    st.header("💡 Tips for a Strong Password")
    st.write("Follow these guidelines to create a secure password:")
    st.markdown("✅ Use at least **8 characters**.")
    st.markdown("✅ Include **uppercase & lowercase** letters.")
    st.markdown("✅ Add at least **one number** (0-9).")
    st.markdown("✅ Use at least **one special character** (!@#$%^&*).")

    st.divider()

    # Generate Strong Password Button
    if st.button("🎲 Generate Strong Password"):
        strong_password = generate_strong_password()
        st.success(f"🔑 **Generated Password:** `{strong_password}`")

        st.divider()


# Common weak passwords blacklist
COMMON_PASSWORDS = {"123456", "password", "12345678", "qwerty", "123456789", "12345",
                    "1234", "111111", "123123", "abc123", "password1", "123qwe", "admin", "qwertyuiop", "admin123", "admin@123", "admin@1234"}


# Function to check password strength
def check_password_strength(password):
    score: int = 0
    feedback: list = []

    # Blacklist Check
    if password in COMMON_PASSWORDS:
        st.error(
            "❌ This password is too common and easily guessable. Choose a stronger one.")
        return

    # Length Check
    if len(password) >= 8:
        score += 1
        feedback.append("✅ Password is at least 8 characters long.")
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
        feedback.append(
            "✅ Password contains both uppercase and lowercase letters.")
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
        feedback.append("✅ Password contains at least one number.")
    else:
        feedback.append("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
        feedback.append("✅ Password contains at least one special character.")
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    # Strength Rating
    strength_levels = ["Very Weak", "Weak",
                       "Moderate", "Strong", "Very Strong"]
    strength = strength_levels[score]

    # Display Feedback in Columns
    st.subheader("🔍 Feedback")
    col1, col2 = st.columns(2)
    for item in feedback[:2]:
        col1.write(item)
    for item in feedback[2:]:
        col2.write(item)

    # Display Strength Rating
    st.subheader("📊 Strength Rating")
    if strength == "Very Strong":
        st.success(f"🎉 Your password is **{strength}**!")
        st.balloons()
    elif strength == "Strong":
        st.success(f"👍 Your password is **{strength}**.")
    elif strength == "Moderate":
        st.warning(
            f"⚠️ Your password is **{strength}**. Consider adding more security features.")
    else:
        st.error(f"❌ Your password is **{strength}**. Please improve it.")


# Main App
password = st.text_input("Enter your password:",
                         type="password", key="password_input")

# Copy to Clipboard Button
if st.button("📋 Copy Password to Clipboard"):
    safe_copy(password)


# Check password strength
if st.button("🛡️ Check Strength"):
    if password:
        check_password_strength(password)
    else:
        st.warning("Please enter a password to check its strength.")


# Footer
st.markdown("---")
st.markdown('© 2025 Rafay Nadeem. Built with 🤍. \n All rights Reserved')
