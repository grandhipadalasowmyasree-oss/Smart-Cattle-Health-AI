# ============================================================
# chatbot.py
# SMART CATTLE HEALTH AI ASSISTANT
# Existing RAG pipeline + Professional UI
# ============================================================

import os
import re
import html as html_module
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai

from rag.retriever import retrieve_relevant_chunks


# ============================================================
# PATH / ENVIRONMENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")


# ============================================================
# GEMINI CLIENT
# ============================================================

client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception:
        client = None


# ============================================================
# CLEAN AI RESPONSE
# ============================================================

def clean_ai_response(text):
    """
    Removes unwanted HTML / code formatting from Gemini output.

    Example unwanted output:
        <h1 style="color:#166534;">Hello</h1>
        <p>Some text</p>

    Becomes:
        Hello
        Some text
    """

    if text is None:
        return ""

    text = str(text)

    # --------------------------------------------------------
    # Decode HTML entities
    # --------------------------------------------------------

    text = html_module.unescape(text)

    # --------------------------------------------------------
    # Remove fenced code blocks
    # --------------------------------------------------------

    text = re.sub(
        r"```(?:html|HTML|markdown|Markdown)?",
        "",
        text
    )

    text = text.replace(
        "```",
        ""
    )

    # --------------------------------------------------------
    # Remove HTML comments
    # --------------------------------------------------------

    text = re.sub(
        r"<!--.*?-->",
        "",
        text,
        flags=re.DOTALL
    )

    # --------------------------------------------------------
    # Remove script/style blocks
    # --------------------------------------------------------

    text = re.sub(
        r"<(script|style).*?>.*?</\1>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    # --------------------------------------------------------
    # Convert common HTML block tags to line breaks
    # --------------------------------------------------------

    text = re.sub(
        r"</(p|div|h1|h2|h3|h4|h5|h6|li|section|article|header|footer|br)\s*>",
        "\n",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # Replace list opening tags
    # --------------------------------------------------------

    text = re.sub(
        r"<li\b[^>]*>",
        "• ",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # Remove all remaining HTML tags
    # --------------------------------------------------------

    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    # --------------------------------------------------------
    # Remove leftover style/code fragments
    # --------------------------------------------------------

    text = re.sub(
        r'\s+style\s*=\s*["\'][^"\']*["\']',
        "",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # Clean excessive blank lines
    # --------------------------------------------------------

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    # --------------------------------------------------------
    # Clean excessive spaces
    # --------------------------------------------------------

    text = re.sub(
        r"[ \t]{2,}",
        " ",
        text
    )

    return text.strip()


# ============================================================
# RAG RESPONSE FUNCTION
# ============================================================

def get_chatbot_response(user_question):
    """
    Connects the website chatbot to the existing RAG pipeline.

    Flow:
    User Question
        ↓
    Retriever
        ↓
    Existing Knowledge Base
        ↓
    Relevant Context
        ↓
    Gemini
        ↓
    Clean Answer
    """

    question = str(
        user_question
    ).strip()

    if not question:

        return (
            "Please enter a question about cattle health."
        )


    # --------------------------------------------------------
    # Check Gemini
    # --------------------------------------------------------

    if client is None:

        return (
            "AI Assistant is not configured because the Gemini API key "
            "was not found."
        )


    # --------------------------------------------------------
    # Retrieve knowledge from EXISTING RAG
    # --------------------------------------------------------

    try:

        retrieved_chunks = retrieve_relevant_chunks(
            question,
            top_k=3
        )

    except Exception:

        return (
            "I could not access the cattle-health knowledge base "
            "right now."
        )


    # --------------------------------------------------------
    # No information found
    # --------------------------------------------------------

    if not retrieved_chunks:

        return (
            "Sorry, this information is not available in the "
            "provided cattle-health knowledge base."
        )


    # --------------------------------------------------------
    # Build context
    # --------------------------------------------------------

    context_parts = []


    for chunk in retrieved_chunks:

        if isinstance(
            chunk,
            dict
        ):

            text = (
                chunk.get("text")
                or chunk.get("content")
                or chunk.get("page_content")
                or ""
            )

        else:

            text = str(chunk)


        if text.strip():

            context_parts.append(
                text.strip()
            )


    context = "\n\n".join(
        context_parts
    )


    if not context.strip():

        return (
            "Sorry, relevant information was not found in the "
            "provided cattle-health knowledge base."
        )


    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    prompt = f"""
You are AICW - AI Cattle Wellness Assistant.

You answer questions about cattle health using ONLY the
provided knowledge-base context.

IMPORTANT RULES:

1. Use only the information present in the context.
2. Do not invent medical information.
3. Do not hallucinate.
4. If the answer is not present in the context, clearly say:
   "This information is not available in the provided knowledge base."
5. Do not prescribe medicines.
6. Do not recommend antibiotics.
7. Do not recommend injections.
8. Do not provide medicine dosage.
9. Do not provide dangerous veterinary treatment instructions.
10. For suspected disease, recommend veterinary confirmation.
11. Explain answers clearly for farmers/students.
12. You may answer in simple English and Telugu when appropriate.
13. Do not mention RAG, retriever, vector database, prompt,
    model or internal system details.
14. DO NOT generate HTML.
15. DO NOT generate CSS.
16. DO NOT generate JavaScript.
17. DO NOT use <h1>, <h2>, <p>, <div>, <span>, <style>,
    or any other HTML tags.
18. Return only normal readable text.
19. You may use simple Markdown bullets if needed.

KNOWLEDGE BASE CONTEXT:
-----------------------
{context}
-----------------------

USER QUESTION:
{question}

Answer clearly and professionally using plain text only.
"""


    # --------------------------------------------------------
    # Gemini
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )


        answer = getattr(
            response,
            "text",
            None
        )


        if answer:

            # IMPORTANT:
            # Clean any HTML generated by Gemini
            answer = clean_ai_response(
                answer
            )

            if answer:

                return answer


        return (
            "Sorry, I could not generate an answer at this moment."
        )


    except Exception as e:

        error_text = str(e)


        if (
            "503" in error_text
            or "UNAVAILABLE" in error_text
        ):

            return (
                "Gemini is temporarily busy. "
                "Please try again after a few seconds."
            )


        if "429" in error_text:

            return (
                "AI service usage limit has been reached temporarily. "
                "Please try again later."
            )


        if "404" in error_text:

            return (
                "The configured Gemini model is currently unavailable."
            )


        return (
            "The AI Assistant is temporarily unavailable. "
            "Please try again."
        )


# ============================================================
# CHATBOT UI
# ============================================================

def render_chatbot():

    # --------------------------------------------------------
    # Session state
    # --------------------------------------------------------

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []


    if "chat_pending_question" not in st.session_state:

        st.session_state.chat_pending_question = None


    # --------------------------------------------------------
    # Professional page CSS
    # --------------------------------------------------------

    st.markdown(
        """
        <style>

        .aicw-chat-wrapper {
            max-width: 1050px;
            margin: 0 auto;
        }

        .aicw-chat-header {
            text-align: center;
            padding: 20px 20px 10px 20px;
        }

        .aicw-chat-label {
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 2px;
            color: #557a61;
            text-transform: uppercase;
        }

        .aicw-chat-title {
            font-size: 42px;
            font-weight: 800;
            color: #16251c;
            margin-top: 5px;
        }

        .aicw-chat-subtitle {
            color: #68766d;
            font-size: 16px;
            max-width: 650px;
            margin: auto;
        }

        .aicw-empty {
            background: #ffffff;
            border: 1px solid #e4ebe5;
            border-radius: 20px;
            padding: 35px;
            margin-top: 25px;
            text-align: center;
            box-shadow: 0 8px 30px rgba(0,0,0,0.04);
        }

        .aicw-empty-icon {
            font-size: 50px;
        }

        .aicw-empty-title {
            font-size: 22px;
            font-weight: 700;
            color: #1c2b22;
            margin-top: 10px;
        }

        .aicw-empty-text {
            color: #718078;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="aicw-chat-wrapper">

            <div class="aicw-chat-header">

                <div class="aicw-chat-label">
                    AICW • AI CATTLE WELLNESS
                </div>

                <div class="aicw-chat-title">
                    AI Assistant
                </div>

                <div class="aicw-chat-subtitle">
                    Ask anything about cattle health, diseases,
                    symptoms, precautions and care.
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Sidebar
    # --------------------------------------------------------

    with st.sidebar:

        st.markdown(
            "### 🐄 AICW Assistant"
        )


        if st.button(
            "＋ New Conversation",
            use_container_width=True
        ):

            st.session_state.chat_history = []

            st.session_state.chat_pending_question = None


            try:

                st.rerun()

            except Exception:

                try:

                    st.experimental_rerun()

                except Exception:

                    pass


        st.markdown("---")


        st.markdown(
            "#### Recent Questions"
        )


        questions = [

            item["question"]

            for item
            in st.session_state.chat_history

            if item.get("role") == "user"

        ]


        for question_item in questions[-5:]:

            st.caption(
                "• "
                + question_item[:60]
            )


    # --------------------------------------------------------
    # Empty state
    # --------------------------------------------------------

    if not st.session_state.chat_history:

        st.markdown(
            """
            <div class="aicw-empty">

                <div class="aicw-empty-icon">
                    🐄
                </div>

                <div class="aicw-empty-title">
                    How can I help with cattle health?
                </div>

                <div class="aicw-empty-text">
                    Ask about cattle diseases, symptoms,
                    prevention, nutrition and general care.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            "###"
        )


        st.markdown(
            "**Try asking:**"
        )


        q1, q2, q3 = st.columns(3)


        if q1.button(
            "What is Lumpy Skin Disease?",
            use_container_width=True
        ):

            st.session_state.chat_pending_question = (
                "What is Lumpy Skin Disease?"
            )


        if q2.button(
            "What are the symptoms?",
            use_container_width=True
        ):

            st.session_state.chat_pending_question = (
                "What are the symptoms of cattle diseases?"
            )


        if q3.button(
            "How can cattle be protected?",
            use_container_width=True
        ):

            st.session_state.chat_pending_question = (
                "How can cattle be protected from diseases?"
            )


    # --------------------------------------------------------
    # Existing conversation
    # --------------------------------------------------------

    for message in st.session_state.chat_history:

        role = message.get(
            "role"
        )


        content = message.get(
            "content",
            ""
        )


        if role == "user":

            with st.chat_message(
                "user"
            ):

                st.markdown(
                    content
                )


        else:

            with st.chat_message(
                "assistant",
                avatar="🐄"
            ):

                # Also clean old answers that may already be
                # stored in session state.
                safe_content = clean_ai_response(
                    content
                )

                st.markdown(
                    safe_content
                )


    # --------------------------------------------------------
    # Input
    # --------------------------------------------------------

    question = st.chat_input(
        "Ask about cattle health..."
    )


    # --------------------------------------------------------
    # Button question
    # --------------------------------------------------------

    if st.session_state.chat_pending_question:

        question = (
            st.session_state.chat_pending_question
        )

        st.session_state.chat_pending_question = None


    # --------------------------------------------------------
    # Process question
    # --------------------------------------------------------

    if question:

        question = question.strip()


        if question:

            # ------------------------------------------------
            # User message
            # ------------------------------------------------

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "question": question,
                    "content": question
                }
            )


            with st.chat_message(
                "user"
            ):

                st.markdown(
                    question
                )


            # ------------------------------------------------
            # Assistant
            # ------------------------------------------------

            with st.chat_message(
                "assistant",
                avatar="🐄"
            ):

                with st.spinner(
                    "Checking cattle-health information..."
                ):

                    answer = get_chatbot_response(
                        question
                    )


                # Final safety cleaning
                answer = clean_ai_response(
                    answer
                )


                st.markdown(
                    answer
                )


            # ------------------------------------------------
            # Save answer
            # ------------------------------------------------

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


            # ------------------------------------------------
            # Rerun
            # ------------------------------------------------

            try:

                st.rerun()

            except Exception:

                try:

                    st.experimental_rerun()

                except Exception:

                    pass