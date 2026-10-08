# ============================================================
# CATTLE VISION AI - LOGIN & REGISTER
# ============================================================

import streamlit as st
import hashlib
import json
from pathlib import Path


# ============================================================
# USERS FILE
# ============================================================

USERS_FILE = Path(__file__).parent / "users.json"


# ============================================================
# PASSWORD HASH
# ============================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# LOAD USERS
# ============================================================

def load_users():

    if USERS_FILE.exists():

        try:

            with open(
                USERS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return {}

    return {}


# ============================================================
# SAVE USERS
# ============================================================

def save_users(users):

    with open(
        USERS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            users,
            f,
            indent=4
        )


# ============================================================
# MAIN LOGIN PAGE
# ============================================================

def render_login():

    # ========================================================
    # PAGE DESIGN
    # ========================================================

    st.markdown(
        """
        <style>

        /* ==================================================
           SKY BLUE BACKGROUND
           ================================================== */

        .stApp {

            background: #dff3ff;

        }


        /* ==================================================
           PAGE WIDTH
           ================================================== */

        .block-container {

            max-width: 600px;

            padding-top: 65px;

            padding-bottom: 40px;

        }


        /* ==================================================
           CATTLE VISION AI
           ================================================== */

        .cattle-title {

            text-align: center;

            color: #123b68;

            font-size: 42px;

            font-weight: 800;

            margin-bottom: 3px;

        }


        .cattle-subtitle {

            text-align: center;

            color: #123b68;

            font-size: 15px;

            margin-bottom: 35px;

        }


        /* ==================================================
           EMAIL / PASSWORD LABEL
           ================================================== */

        .stTextInput label {

            color: #123b68 !important;

            font-weight: 700 !important;

        }


        /* ==================================================
           EMAIL / PASSWORD BOX
           ================================================== */

        .stTextInput input {

            background-color: #123b68 !important;

            color: white !important;

            border: 2px solid #123b68 !important;

            border-radius: 10px !important;

            height: 44px !important;

        }


        /* PLACEHOLDER */

        .stTextInput input::placeholder {

            color: #dce8f2 !important;

            opacity: 1 !important;

        }


        /* ==================================================
           LOGIN / REGISTER BUTTON
           ================================================== */

        .stButton > button {

            width: 100%;

            height: 44px;

            background-color: #123b68 !important;

            color: white !important;

            border: 2px solid #123b68 !important;

            border-radius: 10px;

            font-size: 16px;

            font-weight: 700;

        }


        .stButton > button:hover {

            background-color: #0d2e52 !important;

            border-color: #0d2e52 !important;

            color: white !important;

        }


        /* ==================================================
           NEW USER / ALREADY ACCOUNT TEXT
           ================================================== */

        .register-link {

            text-align: center;

            margin-top: 18px;

            margin-bottom: 8px;

            color: #123b68 !important;

            font-size: 15px;

            font-weight: 700;

        }


        /* ==================================================
           ERROR / WARNING / INFO TEXT
           ================================================== */

        div[data-testid="stAlert"] {

            color: #123b68 !important;

            background-color: #eaf4fb !important;

            border-radius: 10px !important;

        }


        div[data-testid="stAlert"] p {

            color: #123b68 !important;

            font-weight: 600 !important;

        }


        /* ==================================================
           SUCCESS MESSAGE
           ================================================== */

        div[data-testid="stAlert"] p {

            font-weight: 600 !important;

        }


        /* ==================================================
           HIDE STREAMLIT MENU
           ================================================== */

        #MainMenu {

            visibility: hidden;

        }


        footer {

            visibility: hidden;

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CATTLE VISION AI TITLE
    # ========================================================

    st.markdown(
        '<div class="cattle-title">CattleVisionAI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="cattle-subtitle">'
        'Smart Cattle Health AI'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # REGISTER STATE
    # ========================================================

    if "show_register" not in st.session_state:

        st.session_state.show_register = False


    # ========================================================
    # REGISTER PAGE
    # ========================================================

    if st.session_state.show_register:

        # ----------------------------------------------------
        # EMAIL
        # ----------------------------------------------------

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="register_email"
        )


        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create your password",
            key="register_password"
        )


        # ----------------------------------------------------
        # CONFIRM PASSWORD
        # ----------------------------------------------------

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="register_confirm"
        )


        st.write("")


        # ----------------------------------------------------
        # CREATE ACCOUNT
        # ----------------------------------------------------

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            users = load_users()

            email = email.strip().lower()


            if not email:

                st.markdown(
                    """
                    <p style="
                        color:#123b68;
                        font-weight:600;
                        text-align:center;
                    ">
                        Please enter your email.
                    </p>
                    """,
                    unsafe_allow_html=True
                )


            elif not password:

                st.markdown(
                    """
                    <p style="
                        color:#123b68;
                        font-weight:600;
                        text-align:center;
                    ">
                        Please enter your password.
                    </p>
                    """,
                    unsafe_allow_html=True
                )


            elif password != confirm_password:

                st.markdown(
                    """
                    <p style="
                        color:#123b68;
                        font-weight:600;
                        text-align:center;
                    ">
                        Passwords do not match.
                    </p>
                    """,
                    unsafe_allow_html=True
                )


            elif email in users:

                st.markdown(
                    """
                    <p style="
                        color:#123b68;
                        font-weight:700;
                        text-align:center;
                    ">
                        Account already exists. Please login.
                    </p>
                    """,
                    unsafe_allow_html=True
                )


            else:

                users[email] = hash_password(
                    password
                )

                save_users(users)

                st.success(
                    "Account created successfully!"
                )

                st.session_state.show_register = False

                st.experimental_rerun()


        # ----------------------------------------------------
        # BACK TO LOGIN
        # ----------------------------------------------------

        st.markdown(
            '<div class="register-link">'
            'Already have an account?'
            '</div>',
            unsafe_allow_html=True
        )


        if st.button(
            "Login",
            use_container_width=True
        ):

            st.session_state.show_register = False

            st.experimental_rerun()


        return


    # ========================================================
    # LOGIN PAGE
    # ========================================================

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    email = st.text_input(
        "Email",
        placeholder="Enter your email",
        key="login_email"
    )


    # --------------------------------------------------------
    # PASSWORD
    # --------------------------------------------------------

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        key="login_password"
    )


    st.write("")


    # ========================================================
    # LOGIN BUTTON
    # ========================================================

    if st.button(
        "Login",
        use_container_width=True
    ):

        users = load_users()

        email = email.strip().lower()


        if not email or not password:

            st.markdown(
                """
                <p style="
                    color:#123b68;
                    font-weight:600;
                    text-align:center;
                ">
                    Please enter email and password.
                </p>
                """,
                unsafe_allow_html=True
            )


        elif email not in users:

            st.markdown(
                """
                <p style="
                    color:#123b68;
                    font-weight:600;
                    text-align:center;
                ">
                    Account not found. Please register first.
                </p>
                """,
                unsafe_allow_html=True
            )


        elif users[email] != hash_password(password):

            st.markdown(
                """
                <p style="
                    color:#123b68;
                    font-weight:600;
                    text-align:center;
                ">
                    Incorrect password.
                </p>
                """,
                unsafe_allow_html=True
            )


        else:

            st.session_state.logged_in = True

            st.session_state.user_email = email

            st.success(
                "Login successful!"
            )

            st.experimental_rerun()


    # ========================================================
    # REGISTER
    # ========================================================

    st.markdown(
        '<div class="register-link">'
        'New user?'
        '</div>',
        unsafe_allow_html=True
    )


    if st.button(
        "Register",
        use_container_width=True
    ):

        st.session_state.show_register = True

        st.experimental_rerun()