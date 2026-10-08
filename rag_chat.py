import os

from dotenv import load_dotenv
from google import genai

from retriever import retrieve_relevant_chunks


# ============================================================
# LOAD API KEY
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found!")


client = genai.Client(api_key=API_KEY)


# ============================================================
# RAG CHAT FUNCTION
# ============================================================

def ask_rag(question):

    results = retrieve_relevant_chunks(
        question,
        top_k=3
    )

    if not results:
        return (
            "I could not find relevant information in "
            "the cattle health knowledge document."
        )

    context = "\n\n".join(results)

    prompt = f"""
You are a cattle health information assistant.

Answer the farmer's question using ONLY the
information provided in the knowledge context below.

Knowledge Context:
------------------
{context}
------------------

Farmer Question:
{question}

Instructions:

1. Give a simple and clear answer.
2. Do not invent information that is not present
   in the knowledge context.
3. Do not prescribe medicines, antibiotics,
   injections, or dosages.
4. Do not claim that a disease is confirmed.
5. If the signs may indicate a disease, say that
   veterinary confirmation is needed.
6. Give the answer in both English and simple Telugu.
7. Keep the answer practical for a farmer.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    question = input(
        "\n🐄 Ask your cattle health question: "
    )

    print("\n⏳ Finding information...\n")

    answer = ask_rag(question)

    print("\n========================================")
    print("💬 RAG ASSISTANT ANSWER")
    print("========================================\n")

    print(answer)

    print("\n========================================")