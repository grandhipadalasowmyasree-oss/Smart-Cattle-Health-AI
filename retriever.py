from .chunk_document import create_chunks
from .read_document import read_pdf


# ============================================================
# LOAD DOCUMENT
# ============================================================

document_text = read_pdf()
chunks = create_chunks(document_text)


# ============================================================
# DISEASE KEYWORDS
# ============================================================

DISEASE_KEYWORDS = {
    "lumpy": [
        "lumpy",
        "lumpy skin",
        "skin nodules",
        "nodules",
        "skin lumps"
    ],

    "mastitis": [
        "mastitis",
        "udder",
        "teat",
        "abnormal milk",
        "udder swelling"
    ],

    "fmd": [
        "foot and mouth",
        "fmd",
        "mouth lesions",
        "salivation",
        "lameness",
        "foot pain"
    ],

    "healthy": [
        "healthy",
        "normal cattle",
        "routine health",
        "preventive care"
    ]
}


# ============================================================
# TOPIC KEYWORDS
# ============================================================

TOPIC_KEYWORDS = {
    "symptoms": [
        "symptom",
        "symptoms",
        "sign",
        "signs",
        "fever",
        "pain",
        "swelling",
        "lesions"
    ],

    "prevention": [
        "prevent",
        "prevention",
        "precaution",
        "biosecurity",
        "control",
        "protect"
    ],

    "cause": [
        "cause",
        "caused",
        "virus",
        "bacteria",
        "agent"
    ],

    "transmission": [
        "transmission",
        "spread",
        "spreads",
        "vector",
        "infected"
    ],

    "care": [
        "care",
        "management",
        "monitor",
        "monitoring"
    ]
}


# ============================================================
# RETRIEVE RELEVANT CHUNKS
# ============================================================

def retrieve_relevant_chunks(question, top_k=3):

    question_lower = question.lower()

    scored_chunks = []

    # Detect disease from question
    detected_disease = None

    for disease, keywords in DISEASE_KEYWORDS.items():

        if any(keyword in question_lower for keyword in keywords):

            detected_disease = disease
            break

    # Detect topic from question
    detected_topic = None

    for topic, keywords in TOPIC_KEYWORDS.items():

        if any(keyword in question_lower for keyword in keywords):

            detected_topic = topic
            break

    # Score every chunk
    for chunk in chunks:

        chunk_lower = chunk.lower()

        score = 0

        # --------------------------------------------
        # Disease relevance
        # --------------------------------------------

        if detected_disease:

            disease_words = DISEASE_KEYWORDS[detected_disease]

            disease_matches = sum(
                1
                for word in disease_words
                if word in chunk_lower
            )

            score += disease_matches * 10

        # --------------------------------------------
        # Topic relevance
        # --------------------------------------------

        if detected_topic:

            topic_words = TOPIC_KEYWORDS[detected_topic]

            topic_matches = sum(
                1
                for word in topic_words
                if word in chunk_lower
            )

            score += topic_matches * 3

        # --------------------------------------------
        # Normal word matching
        # --------------------------------------------

        question_words = set(
            question_lower
            .replace("?", "")
            .replace(".", "")
            .replace(",", "")
            .split()
        )

        chunk_words = set(
            chunk_lower
            .replace("?", "")
            .replace(".", "")
            .replace(",", "")
            .split()
        )

        score += len(
            question_words.intersection(chunk_words)
        )

        if score > 0:

            scored_chunks.append(
                (score, chunk)
            )

    # Highest score first
    scored_chunks.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        chunk
        for score, chunk in scored_chunks[:top_k]
    ]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    question = input(
        "\n🐄 Enter your cattle health question: "
    )

    results = retrieve_relevant_chunks(question)

    print("\n========================================")
    print("🔎 RAG RETRIEVAL RESULTS")
    print("========================================")

    if not results:

        print("\n❌ No relevant information found.")

    else:

        for i, result in enumerate(results, start=1):

            print(f"\n--- RESULT {i} ---\n")
            print(result)

    print("\n========================================")