# ============================================================
# SMART CATTLE AI ASSISTANT
# FINAL RAG + GEMINI + TELUGU/ENGLISH VERSION
# ============================================================

import os
import re
import html
import time
import json
import textwrap

import streamlit as st
from dotenv import load_dotenv
from google import genai
import streamlit.components.v1 as components

from deep_translator import GoogleTranslator

from rag.retriever import retrieve_relevant_chunks


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# LOAD ENV
# ============================================================

load_dotenv()

API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


# ============================================================
# GEMINI MODELS
# ============================================================

GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash"
]


# ============================================================
# GEMINI CLIENT
# ============================================================

client = None

if API_KEY:

    try:

        client = genai.Client(
            api_key=API_KEY
        )

    except Exception as error:

        print(
            "Gemini client error:",
            error
        )

        client = None


# ============================================================
# CONSTANT RESPONSES
# ============================================================

NO_KNOWLEDGE_RESPONSE = (
    "Sorry, I don't have that information "
    "in my cattle health knowledge base."
)

RAG_ERROR_RESPONSE = (
    "Sorry, I couldn't access the cattle health "
    "knowledge base right now."
)


# ============================================================
# SAFE RERUN
# ============================================================

def safe_rerun():

    if hasattr(st, "rerun"):

        st.rerun()

        return

    if hasattr(
        st,
        "experimental_rerun"
    ):

        st.experimental_rerun()


# ============================================================
# INITIALIZE CHAT STATE
# ============================================================

def initialize_chat_state():

    if "chat_sessions" not in st.session_state:

        st.session_state.chat_sessions = []


    if "active_chat_id" not in st.session_state:

        st.session_state.active_chat_id = None


    if not st.session_state.chat_sessions:

        chat_id = str(
            int(
                time.time() * 1000
            )
        )

        st.session_state.chat_sessions = [

            {
                "id": chat_id,
                "title": "New Chat",
                "messages": []
            }

        ]

        st.session_state.active_chat_id = (
            chat_id
        )


    valid_ids = [

        chat["id"]

        for chat
        in st.session_state.chat_sessions

    ]


    if (
        st.session_state.active_chat_id
        not in valid_ids
    ):

        st.session_state.active_chat_id = (

            st.session_state.chat_sessions[0]["id"]

        )


# ============================================================
# GET ACTIVE CHAT
# ============================================================

def get_active_chat():

    initialize_chat_state()


    for chat in st.session_state.chat_sessions:

        if (
            chat["id"]
            ==
            st.session_state.active_chat_id
        ):

            return chat


    return st.session_state.chat_sessions[0]


# ============================================================
# CREATE NEW CHAT
# ============================================================

def create_new_chat():

    chat_id = str(
        int(
            time.time() * 1000
        )
    )


    new_chat = {

        "id": chat_id,

        "title": "New Chat",

        "messages": []

    }


    st.session_state.chat_sessions.insert(
        0,
        new_chat
    )


    st.session_state.active_chat_id = (
        chat_id
    )


# ============================================================
# DELETE CHAT
# ============================================================

def delete_chat(chat_id):

    st.session_state.chat_sessions = [

        chat

        for chat
        in st.session_state.chat_sessions

        if chat["id"] != chat_id

    ]


    if not st.session_state.chat_sessions:

        create_new_chat()

        return


    if (
        st.session_state.active_chat_id
        == chat_id
    ):

        st.session_state.active_chat_id = (

            st.session_state.chat_sessions[0]["id"]

        )


# ============================================================
# CHAT TITLE
# ============================================================

def make_chat_title(question):

    title = str(
        question
    ).strip()


    title = re.sub(
        r"\s+",
        " ",
        title
    )


    if not title:

        return "New Chat"


    if len(title) > 35:

        title = (
            title[:35].rstrip()
            + "..."
        )


    return title


# ============================================================
# CLEAN RESPONSE
# ============================================================

def clean_response(response):

    if response is None:

        return ""


    text = str(
        response
    )


    # --------------------------------------------------------
    # HTML ENTITIES
    # --------------------------------------------------------

    text = html.unescape(
        text
    )


    # --------------------------------------------------------
    # REMOVE CODE FENCES
    # --------------------------------------------------------

    text = re.sub(
        r"```(?:html|svg|css|javascript|js|xml|python|text)?",
        "",
        text,
        flags=re.IGNORECASE
    )


    text = text.replace(
        "```",
        ""
    )


    # --------------------------------------------------------
    # REMOVE SVG
    # --------------------------------------------------------

    text = re.sub(
        r"<svg\b.*?</svg>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )


    # --------------------------------------------------------
    # REMOVE SCRIPT
    # --------------------------------------------------------

    text = re.sub(
        r"<script\b.*?</script>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )


    # --------------------------------------------------------
    # REMOVE STYLE
    # --------------------------------------------------------

    text = re.sub(
        r"<style\b.*?</style>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )


    # --------------------------------------------------------
    # REMOVE HTML TAGS
    # --------------------------------------------------------

    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )


    # --------------------------------------------------------
    # REMOVE PAGE MARKERS
    # --------------------------------------------------------

    text = re.sub(
        r"---\s*PAGE\s*\d+\s*---",
        "",
        text,
        flags=re.IGNORECASE
    )


    # --------------------------------------------------------
    # REMOVE DOCUMENT HEADER
    # --------------------------------------------------------

    text = re.sub(
        r"Smart Cattle Health Detection System\s*\|\s*Detailed RAG Knowledge Base",
        "",
        text,
        flags=re.IGNORECASE
    )


    # --------------------------------------------------------
    # REMOVE EXCESSIVE SPACES
    # --------------------------------------------------------

    text = textwrap.dedent(
        text
    )


    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )


    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )


    return text.strip()


# ============================================================
# TELUGU DETECTION
# ============================================================

def is_telugu_text(text):

    text = str(
        text or ""
    )


    for character in text:

        if (
            "\u0C00"
            <= character
            <= "\u0C7F"
        ):

            return True


    return False


# ============================================================
# TRANSLATE TO TELUGU
# ============================================================

def translate_to_telugu(text):

    text = clean_response(
        text
    )


    if not text:

        return text


    try:

        translated = GoogleTranslator(

            source="auto",

            target="te"

        ).translate(
            text
        )


        if translated:

            return clean_response(
                translated
            )


    except Exception as error:

        print(
            "TELUGU TRANSLATION ERROR:",
            error
        )


    return text


# ============================================================
# ANSWER IN USER LANGUAGE
# ============================================================

def answer_in_user_language(
    answer,
    question
):

    answer = clean_response(
        answer
    )


    if not answer:

        return answer


    # Telugu question
    if is_telugu_text(
        question
    ):

        # Already Telugu
        if is_telugu_text(
            answer
        ):

            return answer


        return translate_to_telugu(
            answer
        )


    # English question
    return answer


# ============================================================
# DOCUMENT TO TEXT
# ============================================================

def document_to_text(document):

    if document is None:

        return ""


    if isinstance(
        document,
        str
    ):

        return document.strip()


    if isinstance(
        document,
        dict
    ):

        for key in [

            "text",
            "content",
            "document",
            "chunk"

        ]:

            if key in document:

                value = document[key]


                if value:

                    return str(
                        value
                    ).strip()


        return ""


    for attribute in [

        "text",
        "content",
        "document"

    ]:

        if hasattr(
            document,
            attribute
        ):

            try:

                value = getattr(
                    document,
                    attribute
                )


                if value:

                    return str(
                        value
                    ).strip()


            except Exception:

                pass


    return ""


# ============================================================
# GET RAG DOCUMENTS
# ============================================================

def get_rag_documents(
    question
):

    try:

        documents = retrieve_relevant_chunks(

            question,

            top_k=5

        )

    except Exception as error:

        print(
            "RAG ERROR:",
            error
        )

        return None


    if not documents:

        return []


    cleaned = []


    for document in documents:

        text = document_to_text(
            document
        )


        text = clean_response(
            text
        )


        if text:

            cleaned.append(
                text
            )


    return cleaned


# ============================================================
# GET RAG CONTEXT
# ============================================================

def get_rag_context(
    question
):

    documents = get_rag_documents(
        question
    )


    if documents is None:

        return None


    if not documents:

        return ""


    context = "\n\n".join(
        documents
    )


    return clean_response(
        context
    )


# ============================================================
# REMOVE DOCUMENT NOISE
# ============================================================

def remove_document_noise(
    text
):

    text = clean_response(
        text
    )


    if not text:

        return ""


    # --------------------------------------------------------
    # Remove metadata / glossary sections
    # --------------------------------------------------------

    patterns = [

        r"Disease Knowledge Matrix.*",

        r"Key Telugu Terms for Bilingual Chatbot.*",

        r"English\s+Simple Telugu.*",

        r"Recommended metadata fields:.*"

    ]


    for pattern in patterns:

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )


    # --------------------------------------------------------
    # Remove page markers
    # --------------------------------------------------------

    text = re.sub(
        r"---\s*PAGE\s*\d+\s*---",
        "",
        text,
        flags=re.IGNORECASE
    )


    # --------------------------------------------------------
    # Remove broken null characters
    # --------------------------------------------------------

    text = text.replace(
        "\x00",
        ""
    )


    # --------------------------------------------------------
    # Normalize spaces
    # --------------------------------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    )


    return text.strip()


# ============================================================
# DETECT QUESTION TOPIC
# ============================================================

def detect_question_topic(
    question
):

    q = str(
        question or ""
    ).lower()


    # --------------------------------------------------------
    # PRECAUTIONS / PREVENTION
    # --------------------------------------------------------

    prevention_words = [

        "precaution",
        "precautions",
        "prevent",
        "prevention",
        "preventive",
        "protection",
        "protect",
        "biosecurity",
        "control",
        "avoid",
        "safety",
        "how to prevent"

    ]


    if any(
        word in q
        for word in prevention_words
    ):

        return "prevention"


    # --------------------------------------------------------
    # SYMPTOMS
    # --------------------------------------------------------

    symptom_words = [

        "symptom",
        "symptoms",
        "sign",
        "signs",
        "clinical signs",
        "indication",
        "fever",
        "nodules",
        "swelling",
        "lesion",
        "lesions"

    ]


    if any(
        word in q
        for word in symptom_words
    ):

        return "symptoms"


    # --------------------------------------------------------
    # CAUSE
    # --------------------------------------------------------

    cause_words = [

        "cause",
        "causes",
        "caused by",
        "causative",
        "virus",
        "bacteria",
        "agent",
        "organism"

    ]


    if any(
        word in q
        for word in cause_words
    ):

        return "cause"


    # --------------------------------------------------------
    # TRANSMISSION / SPREAD
    # --------------------------------------------------------

    transmission_words = [

        "transmission",
        "transmit",
        "spread",
        "spreads",
        "spreading",
        "vector",
        "vectors",
        "infected",
        "infection"

    ]


    if any(
        word in q
        for word in transmission_words
    ):

        return "transmission"


    # --------------------------------------------------------
    # CARE / MANAGEMENT
    # --------------------------------------------------------

    care_words = [

        "care",
        "management",
        "manage",
        "monitor",
        "monitoring",
        "feeding",
        "nutrition",
        "hygiene",
        "milk"

    ]


    if any(
        word in q
        for word in care_words
    ):

        return "care"


    # --------------------------------------------------------
    # DEFINITION
    # --------------------------------------------------------

    definition_words = [

        "what is",
        "what are",
        "define",
        "definition",
        "meaning",
        "tell me about",
        "explain"

    ]


    if any(
        word in q
        for word in definition_words
    ):

        return "definition"


    return "general"


# ============================================================
# TOPIC KEYWORDS
# ============================================================

TOPIC_TERMS = {

    "prevention": [

        "prevent",
        "prevention",
        "precaution",
        "precautions",
        "biosecurity",
        "control",
        "protect",
        "isolation",
        "isolate",
        "veterinary assessment",
        "spread"

    ],

    "symptoms": [

        "symptom",
        "symptoms",
        "sign",
        "signs",
        "fever",
        "nodules",
        "skin",
        "swelling",
        "lesions",
        "salivation",
        "lameness",
        "udder",
        "milk"

    ],

    "cause": [

        "cause",
        "caused",
        "causative",
        "virus",
        "bacteria",
        "agent",
        "lsdv",
        "capripoxvirus"

    ],

    "transmission": [

        "transmission",
        "spread",
        "spreads",
        "vector",
        "vectors",
        "infected",
        "infection"

    ],

    "care": [

        "care",
        "management",
        "monitor",
        "monitoring",
        "appetite",
        "feeding",
        "nutrition",
        "hygiene",
        "milk"

    ],

    "definition": [

        "what is",
        "definition",
        "viral disease",
        "disease is",
        "primarily affecting"

    ],

    "general": []

}


# ============================================================
# DISEASE KEYWORDS
# ============================================================

DISEASE_TERMS = {

    "lumpy": [

        "lumpy skin",
        "lumpy",
        "lsd",
        "lsdv"

    ],

    "mastitis": [

        "mastitis",
        "udder",
        "teat"

    ],

    "fmd": [

        "foot and mouth",
        "foot-mouth",
        "fmd",
        "mouth lesions"

    ],

    "healthy": [

        "healthy cow",
        "healthy buffalo",
        "healthy cattle",
        "healthy"

    ]

}


# ============================================================
# FIND SENTENCES BY TOPIC
# ============================================================

def find_topic_sentences(
    context,
    question
):

    topic = detect_question_topic(
        question
    )

    q_lower = question.lower()


    # --------------------------------------------------------
    # Find disease
    # --------------------------------------------------------

    disease = None

    for disease_name, keywords in DISEASE_TERMS.items():

        if any(
            keyword in q_lower
            for keyword in keywords
        ):

            disease = disease_name

            break


    # --------------------------------------------------------
    # Split source into sentences
    # --------------------------------------------------------

    sentences = re.split(
        r"(?<=[.!?])\s+",
        context
    )


    candidates = []


    # --------------------------------------------------------
    # Topic scoring
    # --------------------------------------------------------

    topic_words = TOPIC_TERMS.get(
        topic,
        []
    )


    disease_words = []

    if disease:

        disease_words = DISEASE_TERMS[
            disease
        ]


    for sentence in sentences:

        sentence = sentence.strip()


        if not sentence:

            continue


        sentence_lower = (
            sentence.lower()
        )


        score = 0


        # Disease match
        for word in disease_words:

            if word in sentence_lower:

                score += 5


        # Topic match
        for word in topic_words:

            if word in sentence_lower:

                score += 4


        # Exact question words
        question_words = [

            word

            for word
            in re.findall(
                r"[a-zA-Z]+",
                q_lower
            )

            if len(word) > 3

        ]


        for word in question_words:

            if word in sentence_lower:

                score += 1


        if score > 0:

            candidates.append(
                (
                    score,
                    sentence
                )
            )


    candidates.sort(
        key=lambda item: item[0],
        reverse=True
    )


    return [
        sentence
        for _, sentence
        in candidates
    ]


# ============================================================
# RAG FALLBACK ANSWER
# ============================================================

def rag_fallback_answer(
    context,
    question
):

    context = remove_document_noise(
        context
    )


    if not context:

        return answer_in_user_language(
            NO_KNOWLEDGE_RESPONSE,
            question
        )


    topic = detect_question_topic(
        question
    )


    q_lower = question.lower()


    # ========================================================
    # LUMPY SKIN DISEASE
    # ========================================================

    if (
        "lumpy skin" in q_lower
        or "lumpy" in q_lower
        or "lsd" in q_lower
    ):

        sentences = find_topic_sentences(
            context,
            question
        )


        # ----------------------------------------------------
        # PRECAUTIONS
        # ----------------------------------------------------

        if topic == "prevention":

            selected = []


            for sentence in sentences:

                low = sentence.lower()


                if any(
                    word in low

                    for word in [

                        "isolate",
                        "isolation",
                        "biosecurity",
                        "prevention",
                        "prevent",
                        "control",
                        "spread",
                        "veterinary"

                    ]
                ):

                    selected.append(
                        sentence
                    )


                if len(selected) >= 4:

                    break


            if selected:

                answer = " ".join(
                    selected[:4]
                )

            else:

                answer = (
                    "The knowledge base recommends "
                    "isolation as practical, veterinary "
                    "assessment, biosecurity and prevention "
                    "measures for Lumpy Skin Disease."
                )


            return answer_in_user_language(
                answer,
                question
            )


        # ----------------------------------------------------
        # SYMPTOMS
        # ----------------------------------------------------

        if topic == "symptoms":

            selected = []


            for sentence in sentences:

                low = sentence.lower()


                if any(
                    word in low

                    for word in [

                        "fever",
                        "nodule",
                        "nodules",
                        "skin",
                        "lesion",
                        "swelling",
                        "clinical"

                    ]
                ):

                    selected.append(
                        sentence
                    )


                if len(selected) >= 4:

                    break


            answer = " ".join(
                selected[:4]
            )


            if not answer:

                answer = (
                    "The knowledge base contains "
                    "information about fever and skin "
                    "nodules among the clinical information "
                    "associated with Lumpy Skin Disease."
                )


            return answer_in_user_language(
                answer,
                question
            )


        # ----------------------------------------------------
        # CAUSE
        # ----------------------------------------------------

        if topic == "cause":

            selected = []


            for sentence in sentences:

                low = sentence.lower()


                if any(
                    word in low

                    for word in [

                        "caused",
                        "causative",
                        "virus",
                        "lsdv",
                        "capripoxvirus"

                    ]
                ):

                    selected.append(
                        sentence
                    )


                if len(selected) >= 3:

                    break


            answer = " ".join(
                selected[:3]
            )


            if not answer:

                answer = (
                    "Lumpy Skin Disease is caused by "
                    "Lumpy Skin Disease Virus (LSDV)."
                )


            return answer_in_user_language(
                answer,
                question
            )


        # ----------------------------------------------------
        # TRANSMISSION
        # ----------------------------------------------------

        if topic == "transmission":

            selected = []


            for sentence in sentences:

                low = sentence.lower()


                if any(
                    word in low

                    for word in [

                        "transmission",
                        "spread",
                        "vector",
                        "vectors",
                        "infected"

                    ]
                ):

                    selected.append(
                        sentence
                    )


                if len(selected) >= 4:

                    break


            answer = " ".join(
                selected[:4]
            )


            if not answer:

                answer = (
                    "The knowledge base includes "
                    "information about spread, vectors "
                    "and control of Lumpy Skin Disease."
                )


            return answer_in_user_language(
                answer,
                question
            )


        # ----------------------------------------------------
        # DEFINITION
        # ----------------------------------------------------

        if topic == "definition":

            selected = []


            for sentence in sentences:

                low = sentence.lower()


                if (
                    "lumpy skin disease"
                    in low
                    or "lsdv"
                    in low
                    or "capripoxvirus"
                    in low
                ):

                    selected.append(
                        sentence
                    )


                if len(selected) >= 3:

                    break


            answer = " ".join(
                selected[:3]
            )


            if not answer:

                answer = (
                    "Lumpy Skin Disease (LSD) is a "
                    "viral disease primarily affecting cattle."
                )


            return answer_in_user_language(
                answer,
                question
            )


    # ========================================================
    # MASTITIS
    # ========================================================

    if "mastitis" in q_lower:

        sentences = find_topic_sentences(
            context,
            question
        )


        selected = sentences[:4]


        if selected:

            answer = " ".join(
                selected
            )

        else:

            answer = (
                "The knowledge base contains information "
                "about Mastitis, including udder and milk "
                "observations."
            )


        return answer_in_user_language(
            answer,
            question
        )


    # ========================================================
    # FMD
    # ========================================================

    if (
        "foot and mouth" in q_lower
        or "foot-mouth" in q_lower
        or "fmd" in q_lower
    ):

        sentences = find_topic_sentences(
            context,
            question
        )


        selected = sentences[:4]


        if selected:

            answer = " ".join(
                selected
            )

        else:

            answer = (
                "The knowledge base contains information "
                "about Foot-and-Mouth Disease and its "
                "clinical and control information."
            )


        return answer_in_user_language(
            answer,
            question
        )


    # ========================================================
    # HEALTHY COW
    # ========================================================

    if (
        "healthy cow" in q_lower
        or "healthy buffalo" in q_lower
        or "healthy cattle" in q_lower
    ):

        sentences = find_topic_sentences(
            context,
            question
        )


        selected = sentences[:4]


        if selected:

            answer = " ".join(
                selected
            )

        else:

            answer = (
                "A healthy cow is generally alert, "
                "responsive, and able to stand and walk normally."
            )


        return answer_in_user_language(
            answer,
            question
        )


    # ========================================================
    # GENERAL FALLBACK
    # ========================================================

    sentences = find_topic_sentences(
        context,
        question
    )


    selected = sentences[:4]


    if not selected:

        sentences = re.split(
            r"(?<=[.!?])\s+",
            context
        )

        selected = [
            sentence.strip()
            for sentence in sentences[:3]
            if sentence.strip()
        ]


    answer = " ".join(
        selected
    )


    # Keep answer concise
    if len(answer) > 1000:

        answer = (
            answer[:1000]
            .rsplit(
                " ",
                1
            )[0]
            + "..."
        )


    return answer_in_user_language(
        answer,
        question
    )


# ============================================================
# ASK RAG
# ============================================================

def ask_rag(
    question,
    previous_messages=None
):

    question = str(
        question
    ).strip()


    if not question:

        return "Please enter a question."


    # ========================================================
    # STEP 1
    # RETRIEVE RELEVANT RAG CONTENT
    # ========================================================

    context = get_rag_context(
        question
    )


    # ========================================================
    # RAG ERROR
    # ========================================================

    if context is None:

        return answer_in_user_language(
            RAG_ERROR_RESPONSE,
            question
        )


    # ========================================================
    # NO RELEVANT RAG DATA
    #
    # IMPORTANT:
    # GEMINI IS NOT CALLED
    # ========================================================

    if not context:

        return answer_in_user_language(
            NO_KNOWLEDGE_RESPONSE,
            question
        )


    # ========================================================
    # PREVIOUS CHAT
    # ========================================================

    conversation_text = ""


    if previous_messages:

        recent_messages = (
            previous_messages[-6:]
        )


        conversation_lines = []


        for message in recent_messages:

            role = (

                "Farmer"

                if message.get(
                    "role"
                ) == "user"

                else "Assistant"

            )


            content = clean_response(

                message.get(
                    "content",
                    ""
                )

            )


            if content:

                conversation_lines.append(

                    f"{role}: {content}"

                )


        conversation_text = "\n".join(
            conversation_lines
        )


    # ========================================================
    # GEMINI NOT AVAILABLE
    # ========================================================

    if client is None:

        return rag_fallback_answer(
            context,
            question
        )


    # ========================================================
    # LANGUAGE
    # ========================================================

    if is_telugu_text(question):

        language_instruction = """
The farmer asked in Telugu.

Answer in simple Telugu.
Use Telugu script.

A common technical English term such as
Lumpy Skin Disease (LSD), Mastitis or FMD can
remain in English when useful, but the explanation
must be in Telugu.

Do NOT give the answer fully in English.
"""

    else:

        language_instruction = """
The farmer asked in English.

Answer in simple English.
"""


    # ========================================================
    # TOPIC
    # ========================================================

    topic = detect_question_topic(
        question
    )


    # ========================================================
    # STRICT RAG PROMPT
    # ========================================================

    prompt = f"""
You are Smart Cattle AI Assistant.

You are a STRICT RAG DOCUMENT-BASED assistant.

Your ONLY factual source is the retrieved knowledge.

{language_instruction}

The farmer's detected question topic is:
{topic}

============================================================
STRICT RULES
============================================================

1. Use ONLY the retrieved knowledge.

2. Do NOT use outside knowledge.

3. Do NOT use general model knowledge.

4. Do NOT guess.

5. Do NOT invent facts.

6. Do NOT invent symptoms.

7. Do NOT invent causes.

8. Do NOT invent treatments.

9. Do NOT invent medicines.

10. Do NOT invent dosages.

11. Do NOT provide a definitive diagnosis.

12. Answer ONLY the current question.

13. Pay close attention to what the farmer is asking:
    definition, symptoms, cause, transmission,
    precautions, prevention, care, monitoring, etc.

14. If the farmer asks about precautions or prevention,
    give prevention/biosecurity information from the
    retrieved knowledge, NOT only the disease definition.

15. If the farmer asks about symptoms,
    give symptom information from the retrieved knowledge,
    NOT only the definition.

16. If the farmer asks about the cause,
    give cause information from the retrieved knowledge.

17. If the farmer asks about transmission,
    give transmission/spread information from the
    retrieved knowledge.

18. Do NOT reproduce the whole document.

19. Do NOT reproduce tables.

20. Do NOT reproduce metadata.

21. Do NOT reproduce page numbers.

22. Do NOT reproduce document headings unnecessarily.

23. Do NOT reproduce the Disease Knowledge Matrix.

24. Do NOT reproduce the Telugu glossary.

25. Give a concise answer, normally 2 to 5 sentences.

26. Do NOT generate HTML.

27. Do NOT generate CSS.

28. Do NOT generate JavaScript.

29. Do NOT generate code.

30. If the retrieved knowledge does not contain enough
    information, reply exactly:

Sorry, I don't have that information in my cattle
health knowledge base.

============================================================
RETRIEVED KNOWLEDGE
============================================================

{context}

============================================================
PREVIOUS CONVERSATION
============================================================

{conversation_text}

============================================================
CURRENT FARMER QUESTION
============================================================

{question}

============================================================

Answer only the current question.
"""

    # ========================================================
    # GEMINI REQUEST
    # ========================================================

    for model_name in GEMINI_MODELS:

        try:

            response = client.models.generate_content(

                model=model_name,

                contents=prompt

            )


            answer = getattr(
                response,
                "text",
                ""
            )


            answer = clean_response(
                answer
            )


            # ------------------------------------------------
            # Remove document dumps
            # ------------------------------------------------

            answer = re.sub(
                r"Disease Knowledge Matrix.*",
                "",
                answer,
                flags=re.IGNORECASE | re.DOTALL
            )


            answer = re.sub(
                r"Key Telugu Terms.*",
                "",
                answer,
                flags=re.IGNORECASE | re.DOTALL
            )


            answer = re.sub(
                r"---\s*PAGE\s*\d+\s*---",
                "",
                answer,
                flags=re.IGNORECASE
            )


            answer = clean_response(
                answer
            )


            # ------------------------------------------------
            # Max length
            # ------------------------------------------------

            if len(answer) > 1200:

                answer = (
                    answer[:1200]
                    .rsplit(
                        " ",
                        1
                    )[0]
                    + "..."
                )


            if answer:

                return answer_in_user_language(
                    answer,
                    question
                )


        except Exception as error:

            error_text = str(
                error
            )


            upper_error = (
                error_text.upper()
            )


            print(
                "GEMINI ERROR:",
                error_text
            )


            # =================================================
            # QUOTA
            # =================================================

            if (
                "429" in error_text
                or
                "RESOURCE_EXHAUSTED"
                in upper_error
                or
                "QUOTA"
                in upper_error
                or
                "RATE LIMIT"
                in upper_error
                or
                "USAGE LIMIT"
                in upper_error
            ):

                return rag_fallback_answer(
                    context,
                    question
                )


            # =================================================
            # API KEY
            # =================================================

            if (
                "401" in error_text
                or
                "403" in error_text
                or
                "API KEY"
                in upper_error
            ):

                return rag_fallback_answer(
                    context,
                    question
                )


            # =================================================
            # MODEL NOT FOUND
            # =================================================

            if (
                "404" in error_text
                or
                "NOT_FOUND"
                in upper_error
            ):

                continue


            # =================================================
            # SERVER ERROR
            # =================================================

            if (
                "500" in error_text
                or
                "503" in error_text
                or
                "UNAVAILABLE"
                in upper_error
            ):

                continue


            # =================================================
            # OTHER ERROR
            # =================================================

            return rag_fallback_answer(
                context,
                question
            )


    # ========================================================
    # ALL MODELS FAILED
    # ========================================================

    return rag_fallback_answer(
        context,
        question
    )


# ============================================================
# SHOW USER MESSAGE
# ============================================================

def show_user_message(
    message
):

    st.markdown(
        "### 🧑 You"
    )


    st.write(
        clean_response(
            message
        )
    )


# ============================================================
# SHOW ASSISTANT MESSAGE
# ============================================================

def show_assistant_message(
    message
):

    st.markdown(
        "### 🐄 Smart Cattle AI"
    )


    st.write(
        clean_response(
            message
        )
    )


# ============================================================
# VOICE ASSISTANT
# ============================================================

def render_voice_assistant(
    answer
):

    safe_answer = json.dumps(
        clean_response(
            answer
        )
    )


    components.html(

        f"""
        <script>

        const answerText = {safe_answer};

        function speakAnswer() {{

            if (
                !("speechSynthesis" in window)
            ) {{

                alert(
                    "Voice is not supported "
                    + "in this browser."
                );

                return;

            }}


            window.speechSynthesis.cancel();


            const utterance =
                new SpeechSynthesisUtterance(
                    answerText
                );


            utterance.rate = 0.95;

            utterance.pitch = 1.0;

            utterance.volume = 1.0;


            const teluguRange =
                /[\\u0C00-\\u0C7F]/;


            if (
                teluguRange.test(answerText)
            ) {{

                utterance.lang = "te-IN";

            }} else {{

                utterance.lang = "en-IN";

            }}


            window.speechSynthesis.speak(
                utterance
            );

        }}

        </script>


        <button
            onclick="speakAnswer()"
            style="
                padding:8px 16px;
                border-radius:20px;
                border:1px solid #9FD5E8;
                background:#F1FAFE;
                color:#124B70;
                font-size:13px;
                font-weight:700;
                cursor:pointer;
            "
        >
            🔊 Voice Assistant
        </button>
        """,

        height=48,

        scrolling=False

    )


# ============================================================
# CHAT SIDEBAR
# ============================================================

def render_chat_sidebar():

    with st.sidebar:

        st.markdown(
            "## 🐄 Smart Cattle AI"
        )


        st.caption(
            "AI HEALTH ASSISTANT"
        )


        st.write("")


        # ====================================================
        # NEW CHAT
        # ====================================================

        if st.button(

            "＋ New Chat",

            key="new_chat_button",

            use_container_width=True

        ):

            create_new_chat()

            safe_rerun()


        st.markdown(
            "---"
        )


        # ====================================================
        # CHAT HISTORY
        # ====================================================

        st.markdown(
            "### Chat History"
        )


        for chat in st.session_state.chat_sessions:

            chat_id = chat["id"]

            title = chat["title"]


            col1, col2 = st.columns(
                [5, 1]
            )


            # =================================================
            # OPEN CHAT
            # =================================================

            with col1:

                active = (

                    chat_id
                    ==
                    st.session_state.active_chat_id

                )


                label = (

                    ("● " if active else "")
                    +
                    title

                )


                if st.button(

                    label,

                    key=f"history_{chat_id}",

                    use_container_width=True

                ):

                    st.session_state.active_chat_id = (
                        chat_id
                    )

                    safe_rerun()


            # =================================================
            # DELETE
            # =================================================

            with col2:

                if st.button(

                    "🗑",

                    key=f"delete_{chat_id}",

                    use_container_width=True

                ):

                    delete_chat(
                        chat_id
                    )

                    safe_rerun()


# ============================================================
# MAIN CHATBOT
# ============================================================
# ============================================================
# MAIN CHATBOT
# ============================================================

def render_chatbot():

    initialize_chat_state()

    # ========================================================
    # SIDEBAR
    # ========================================================

    render_chat_sidebar()

    # ========================================================
    # ACTIVE CHAT
    # ========================================================

    active_chat = get_active_chat()

    # ========================================================
    # HEADER
    # ========================================================

    st.title(
        "💬 Smart Cattle AI Assistant"
    )

    st.caption(
        "Ask questions about cattle health, diseases, "
        "nutrition and care."
    )

    st.markdown(
        "---"
    )

    # ========================================================
    # MESSAGE AREA
    # ========================================================

    message_area = st.empty()

    # ========================================================
    # INPUT
    # ========================================================

    with st.form(
        key=f"chat_form_{active_chat['id']}",
        clear_on_submit=True
    ):

        input_col, send_col = st.columns(
            [9, 1]
        )

        # ====================================================
        # QUESTION INPUT
        # ====================================================

        with input_col:

            user_question = st.text_input(
                "Message",
                placeholder="Type your cattle health question...",
                label_visibility="collapsed",
                key=f"question_{active_chat['id']}"
            )

        # ====================================================
        # SEND BUTTON
        # ====================================================

        with send_col:

            send_button = st.form_submit_button(
                "➤",
                use_container_width=True
            )

    # ========================================================
    # PROCESS MESSAGE
    # ========================================================

    if send_button:

        question = str(
            user_question
        ).strip()

        if question:

            previous_messages = (
                active_chat["messages"].copy()
            )

            # ------------------------------------------------
            # USER MESSAGE
            # ------------------------------------------------

            active_chat["messages"].append(
                {
                    "role": "user",
                    "content": question
                }
            )

            # ------------------------------------------------
            # CHAT TITLE
            # ------------------------------------------------

            if active_chat["title"] == "New Chat":

                active_chat["title"] = (
                    make_chat_title(
                        question
                    )
                )

            # ------------------------------------------------
            # ANSWER
            # ------------------------------------------------

            with st.spinner(
                "Searching cattle health knowledge..."
            ):

                answer = ask_rag(
                    question,
                    previous_messages
                )

            answer = clean_response(
                answer
            )

            # ------------------------------------------------
            # AI MESSAGE
            # ------------------------------------------------

            active_chat["messages"].append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

    # ========================================================
    # DISPLAY MESSAGES
    # ========================================================

    with message_area.container():

        if not active_chat["messages"]:

            st.info(
                """
👋 **Hello Farmer!**

I am your **Smart Cattle AI Assistant**.

You can ask me about:

🩺 Cattle diseases  
🔍 Symptoms  
🛡️ Prevention  
🌾 Nutrition  
🧼 Hygiene  
🐄 General cattle care
"""
            )

        else:

            for message in active_chat["messages"]:

                if message["role"] == "user":

                    show_user_message(
                        message["content"]
                    )

                else:

                    show_assistant_message(
                        message["content"]
                    )

                    render_voice_assistant(
                        message["content"]
                    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    render_chatbot()
# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    render_chatbot()