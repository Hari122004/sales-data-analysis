import streamlit as st
import pandas as pd
import os

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Login System",
    layout="centered"
)

# ---------------------------
# CREATE USERS FILE
# ---------------------------
if not os.path.exists("users.csv"):

    df = pd.DataFrame(
        columns=["email", "password"]
    )

    df.to_csv("users.csv", index=False)

# ---------------------------
# SESSION STATE
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------
# TITLE
# ---------------------------
st.title("🔐 Login System")

st.write(
    "Sign In or Create New Account"
)

# ---------------------------
# TABS
# ---------------------------
tab1, tab2 = st.tabs(
    ["🔑 Sign In", "📝 Sign Up"]
)

# =================================================
# SIGN IN
# =================================================
with tab1:

    st.subheader("Login to Account")

    email = st.text_input(
        "Enter Gmail",
        key="login_email"
    ).strip()

    password = st.text_input(
        "Enter Password",
        type="password",
        key="login_password"
    ).strip()

    if st.button("Login"):

        users = pd.read_csv("users.csv")

        user = users[
            (users["email"] == email) &
            (users["password"] == password)
        ]

        if not user.empty:

            st.session_state.logged_in = True
            st.session_state.user = email

            st.success("Login Successful")

            st.switch_page(
                "pages/dashboard.py"
            )

        else:
            st.error(
                "Invalid Gmail or Password"
            )

# =================================================
# SIGN UP
# =================================================
with tab2:

    st.subheader("Create New Account")

    new_email = st.text_input(
        "Enter Gmail",
        key="signup_email"
    ).strip()

    new_password = st.text_input(
        "Create Password",
        type="password",
        key="signup_password"
    ).strip()

    if st.button("Create Account"):

        users = pd.read_csv("users.csv")

        # Check existing user
        if new_email in users["email"].values:

            st.warning(
                "Account already exists"
            )

        else:

            new_user = pd.DataFrame({
                "email": [new_email],
                "password": [new_password]
            })

            users = pd.concat(
                [users, new_user],
                ignore_index=True
            )

            users.to_csv(
                "users.csv",
                index=False
            )

            st.success(
                "Account Created Successfully"
            )