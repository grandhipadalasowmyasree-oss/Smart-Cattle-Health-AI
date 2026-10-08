# ============================================================
# SMART CATTLE HEALTH AI
# Automatic Bilingual Health Guidance Backend
# ============================================================

import os
import json
from dotenv import load_dotenv
from google import genai


# ============================================================
# 1. LOAD ENVIRONMENT
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-3.8-flash"


# ============================================================
# 2. CREATE CLIENT
# ============================================================

_client = None

if API_KEY:
    try:
        _client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print("Health Guidance client error:", e)
        _client = None


# ============================================================
# 3. FALLBACK GUIDANCE
# ============================================================

def fallback_guidance(
    animal_type,
    predicted_condition,
    confidence,
    risk_level
):
    """
    Safe fallback guidance if automatic generation fails.
    """

    condition = predicted_condition.lower()
    risk = risk_level.lower()

    # --------------------------------------------------------
    # RISK ALERT
    # --------------------------------------------------------

    if risk == "high":
        risk_alert_en = (
            "High Risk: Veterinary attention is recommended "
            "as soon as possible."
        )

        risk_alert_te = (
            "అధిక ప్రమాదం: వీలైనంత త్వరగా పశువైద్యుల "
            "సహాయం తీసుకోవడం మంచిది."
        )

    elif risk == "medium":
        risk_alert_en = (
            "Moderate Risk: Monitor the animal closely and "
            "consider veterinary consultation."
        )

        risk_alert_te = (
            "మధ్యస్థ ప్రమాదం: జంతువును జాగ్రత్తగా గమనించి, "
            "అవసరమైతే పశువైద్యులను సంప్రదించండి."
        )

    else:
        risk_alert_en = (
            "Low Risk: Continue regular monitoring and "
            "preventive care."
        )

        risk_alert_te = (
            "తక్కువ ప్రమాదం: క్రమం తప్పకుండా జంతువును "
            "గమనిస్తూ, నివారణ సంరక్షణను కొనసాగించండి."
        )

    # --------------------------------------------------------
    # HEALTHY
    # --------------------------------------------------------

    if condition == "healthy":

        return {
            "english": {
                "overview": (
                    f"The {animal_type.lower()} appears healthy based "
                    "on the image prediction. This result is not a "
                    "confirmed veterinary diagnosis."
                ),

                "precautions": [
                    "Maintain a clean and dry living area.",
                    "Provide clean drinking water regularly.",
                    "Observe eating, drinking and normal activity.",
                    "Maintain good hygiene while handling the animal."
                ],

                "care": [
                    "Provide balanced and suitable nutrition.",
                    "Keep the animal's surroundings clean.",
                    "Monitor the animal regularly for unusual changes.",
                    "Follow routine veterinary health check-ups."
                ],

                "avoid": [
                    "Avoid keeping the animal in dirty or overcrowded areas.",
                    "Avoid sudden changes in feed or routine.",
                    "Do not ignore unusual symptoms or behavior."
                ],

                "veterinarian": (
                    "Arrange routine veterinary check-ups. If unusual "
                    "symptoms, reduced feeding, fever or behavioral "
                    "changes appear, seek veterinary advice."
                ),

                "risk_alert": risk_alert_en
            },

            "telugu": {
                "overview": (
                    f"చిత్ర ఆధారంగా ఈ {animal_type.lower()} ఆరోగ్యంగా "
                    "ఉన్నట్లు కనిపిస్తోంది. అయితే ఇది ఖచ్చితమైన "
                    "పశువైద్య నిర్ధారణ కాదు."
                ),

                "precautions": [
                    "జంతువు ఉండే ప్రదేశాన్ని శుభ్రంగా మరియు పొడిగా ఉంచండి.",
                    "ఎల్లప్పుడూ శుభ్రమైన తాగునీటిని అందించండి.",
                    "ఆహారం తీసుకోవడం, నీరు తాగడం మరియు సాధారణ చలనం గమనించండి.",
                    "జంతువును చూసుకునేటప్పుడు మంచి పరిశుభ్రత పాటించండి."
                ],

                "care": [
                    "సరైన మరియు సమతుల్యమైన ఆహారం అందించండి.",
                    "జంతువు పరిసరాలను శుభ్రంగా ఉంచండి.",
                    "అసాధారణమైన మార్పులు ఉన్నాయా అని క్రమం తప్పకుండా గమనించండి.",
                    "క్రమం తప్పకుండా పశువైద్యుల ఆరోగ్య పరీక్షలు చేయించండి."
                ],

                "avoid": [
                    "మురికి లేదా ఎక్కువ జంతువులు ఉన్న ప్రదేశాల్లో ఉంచకుండా చూడండి.",
                    "ఆహారం లేదా రోజువారీ అలవాట్లలో అకస్మాత్తుగా మార్పులు చేయవద్దు.",
                    "అసాధారణ లక్షణాలు లేదా ప్రవర్తనను నిర్లక్ష్యం చేయవద్దు."
                ],

                "veterinarian": (
                    "క్రమం తప్పకుండా పశువైద్యుల పరీక్షలు చేయించండి. "
                    "అసాధారణ లక్షణాలు, ఆహారం తగ్గడం, జ్వరం లేదా ప్రవర్తనలో "
                    "మార్పులు కనిపిస్తే పశువైద్యులను సంప్రదించండి."
                ),

                "risk_alert": risk_alert_te
            }
        }

    # --------------------------------------------------------
    # LUMPY SKIN DISEASE
    # --------------------------------------------------------

    if "lumpy" in condition:

        return {
            "english": {
                "overview": (
                    "The image prediction indicates possible signs "
                    "associated with Lumpy Skin Disease. Typical signs "
                    "may include skin nodules, fever or changes in the "
                    "animal's general condition. Image prediction alone "
                    "cannot confirm the disease."
                ),

                "precautions": [
                    "Keep the animal separated from apparently healthy cattle when possible.",
                    "Maintain clean and dry housing conditions.",
                    "Reduce exposure to insects such as flies and mosquitoes.",
                    "Avoid sharing equipment between affected and healthy animals.",
                    "Monitor the animal for changes in fever, appetite and skin condition."
                ],

                "care": [
                    "Provide clean drinking water and suitable nutrition.",
                    "Keep the affected animal comfortable and its resting area clean.",
                    "Observe skin lesions and general health regularly.",
                    "Follow the veterinarian's instructions for further care."
                ],

                "avoid": [
                    "Do not allow unnecessary contact with healthy cattle.",
                    "Do not use medicines or injections without veterinary advice.",
                    "Do not ignore worsening skin lesions, fever or weakness.",
                    "Avoid unhygienic and insect-heavy surroundings."
                ],

                "veterinarian": (
                    "Veterinary examination is recommended to confirm the "
                    "condition and decide appropriate treatment and control "
                    "measures, especially when lesions, fever or weakness "
                    "are increasing."
                ),

                "risk_alert": risk_alert_en
            },

            "telugu": {
                "overview": (
                    "చిత్రంలో లంపీ స్కిన్ డిసీజ్‌కు సంబంధించిన కొన్ని "
                    "లక్షణాలు ఉన్నట్లు కనిపిస్తున్నాయి. చర్మంపై గడ్డలు, "
                    "జ్వరం లేదా ఆరోగ్యంలో మార్పులు కనిపించవచ్చు. "
                    "చిత్రం ఆధారంగా మాత్రమే వ్యాధిని ఖచ్చితంగా నిర్ధారించలేము."
                ),

                "precautions": [
                    "సాధ్యమైనంత వరకు ప్రభావిత జంతువును ఆరోగ్యకరమైన జంతువుల నుంచి వేరు ఉంచండి.",
                    "జంతువు ఉండే ప్రదేశాన్ని శుభ్రంగా మరియు పొడిగా ఉంచండి.",
                    "ఈగలు, దోమలు వంటి కీటకాల ప్రభావాన్ని తగ్గించండి.",
                    "ప్రభావిత మరియు ఆరోగ్యకరమైన జంతువులకు ఒకే పరికరాలను ఉపయోగించకుండా చూడండి.",
                    "జ్వరం, ఆకలి మరియు చర్మ పరిస్థితిలో మార్పులను గమనించండి."
                ],

                "care": [
                    "శుభ్రమైన తాగునీరు మరియు సరైన పోషకాహారం అందించండి.",
                    "జంతువుకు సౌకర్యవంతమైన ప్రదేశం కల్పించి, విశ్రాంతి ప్రదేశాన్ని శుభ్రంగా ఉంచండి.",
                    "చర్మంపై ఉన్న గాయాలు మరియు సాధారణ ఆరోగ్యాన్ని క్రమం తప్పకుండా గమనించండి.",
                    "తదుపరి సంరక్షణ కోసం పశువైద్యుల సూచనలను పాటించండి."
                ],

                "avoid": [
                    "అవసరం లేని విధంగా ఆరోగ్యకరమైన జంతువులతో కలపవద్దు.",
                    "పశువైద్యుల సలహా లేకుండా మందులు లేదా ఇంజెక్షన్లు ఇవ్వవద్దు.",
                    "చర్మ గాయాలు, జ్వరం లేదా బలహీనత పెరుగుతున్నా నిర్లక్ష్యం చేయవద్దు.",
                    "అశుభ్రమైన మరియు ఎక్కువ కీటకాలు ఉన్న ప్రదేశాలను నివారించండి."
                ],

                "veterinarian": (
                    "వ్యాధిని నిర్ధారించడానికి మరియు సరైన చికిత్స, నియంత్రణ "
                    "చర్యలను నిర్ణయించడానికి పశువైద్యుల పరీక్ష అవసరం. "
                    "చర్మ గాయాలు, జ్వరం లేదా బలహీనత పెరుగుతుంటే వెంటనే "
                    "పశువైద్యులను సంప్రదించండి."
                ),

                "risk_alert": risk_alert_te
            }
        }

    # --------------------------------------------------------
    # MASTITIS
    # --------------------------------------------------------

    if "mastitis" in condition:

        return {
            "english": {
                "overview": (
                    "The image prediction indicates possible signs "
                    "associated with Mastitis, an inflammation of the "
                    "udder. Changes around the udder or milk may occur. "
                    "Image prediction alone cannot confirm the condition."
                ),

                "precautions": [
                    "Keep the udder and milking area clean.",
                    "Wash hands and maintain proper hygiene before milking.",
                    "Observe the udder for swelling, heat or unusual changes.",
                    "Monitor the milk for changes in appearance.",
                    "Separate visibly affected animals when appropriate."
                ],

                "care": [
                    "Provide clean bedding and a hygienic resting area.",
                    "Ensure access to clean drinking water and suitable nutrition.",
                    "Follow hygienic milking practices.",
                    "Monitor the animal's appetite, behavior and udder condition."
                ],

                "avoid": [
                    "Do not use medicines or antibiotics without veterinary advice.",
                    "Avoid poor milking hygiene.",
                    "Do not ignore abnormal milk or udder swelling.",
                    "Avoid using contaminated milking equipment."
                ],

                "veterinarian": (
                    "Veterinary examination is recommended, particularly "
                    "when the udder is swollen or painful, milk changes are "
                    "noticed, or the animal develops fever or reduced appetite."
                ),

                "risk_alert": risk_alert_en
            },

            "telugu": {
                "overview": (
                    "చిత్రంలో మాస్టిటిస్‌కు సంబంధించిన లక్షణాలు ఉన్నట్లు "
                    "కనిపిస్తున్నాయి. ఇది పొదుగు భాగంలో వాపుతో సంబంధం ఉన్న "
                    "పరిస్థితి. పొదుగు లేదా పాలలో మార్పులు కనిపించవచ్చు. "
                    "చిత్రం ఆధారంగా మాత్రమే దీనిని ఖచ్చితంగా నిర్ధారించలేము."
                ),

                "precautions": [
                    "పొదుగు మరియు పాలు పితికే ప్రదేశాన్ని శుభ్రంగా ఉంచండి.",
                    "పాలు పితికే ముందు చేతులను శుభ్రంగా కడుక్కోండి.",
                    "పొదుగులో వాపు, వేడి లేదా అసాధారణ మార్పులను గమనించండి.",
                    "పాలలో రంగు లేదా రూపంలో మార్పులు ఉన్నాయా గమనించండి.",
                    "అవసరమైనప్పుడు స్పష్టంగా ప్రభావితమైన జంతువును వేరు ఉంచండి."
                ],

                "care": [
                    "శుభ్రమైన పరుపు మరియు పరిశుభ్రమైన విశ్రాంతి ప్రదేశం కల్పించండి.",
                    "శుభ్రమైన నీరు మరియు సరైన పోషకాహారం అందించండి.",
                    "పాలు పితికేటప్పుడు పరిశుభ్రమైన పద్ధతులను పాటించండి.",
                    "జంతువు ఆకలి, ప్రవర్తన మరియు పొదుగు పరిస్థితిని గమనించండి."
                ],

                "avoid": [
                    "పశువైద్యుల సలహా లేకుండా మందులు లేదా యాంటీబయాటిక్స్ ఇవ్వవద్దు.",
                    "పాలు పితికే సమయంలో అపరిశుభ్రతను నివారించండి.",
                    "అసాధారణమైన పాలు లేదా పొదుగు వాపును నిర్లక్ష్యం చేయవద్దు.",
                    "కలుషితమైన పాలు పితికే పరికరాలను ఉపయోగించవద్దు."
                ],

                "veterinarian": (
                    "పొదుగులో వాపు లేదా నొప్పి, పాలలో మార్పులు, జ్వరం లేదా "
                    "ఆకలి తగ్గడం కనిపిస్తే పశువైద్యుల పరీక్ష అవసరం."
                ),

                "risk_alert": risk_alert_te
            }
        }

    # --------------------------------------------------------
    # FOOT AND MOUTH DISEASE
    # --------------------------------------------------------

    if "foot" in condition or "mouth" in condition:

        return {
            "english": {
                "overview": (
                    "The image prediction indicates possible signs "
                    "associated with Foot and Mouth Disease. Signs may "
                    "include lesions around the mouth or feet and changes "
                    "in feeding or movement. Image prediction alone cannot "
                    "confirm the disease."
                ),

                "precautions": [
                    "Separate the suspected animal from healthy cattle.",
                    "Limit unnecessary movement of the animal.",
                    "Keep feeding and resting areas clean.",
                    "Avoid sharing equipment between animals.",
                    "Monitor feeding, movement and visible mouth or foot changes."
                ],

                "care": [
                    "Provide clean drinking water and suitable nutrition.",
                    "Keep the animal in a clean and comfortable area.",
                    "Monitor the animal closely for changes in movement and feeding.",
                    "Follow veterinary instructions for disease control."
                ],

                "avoid": [
                    "Do not mix the suspected animal with healthy cattle.",
                    "Avoid unnecessary transportation or movement.",
                    "Do not use medicines without veterinary advice.",
                    "Do not ignore mouth lesions, foot lesions or reduced feeding."
                ],

                "veterinarian": (
                    "Veterinary attention is important because Foot and "
                    "Mouth Disease can spread between susceptible animals. "
                    "Seek professional advice promptly when signs are suspected."
                ),

                "risk_alert": risk_alert_en
            },

            "telugu": {
                "overview": (
                    "చిత్రంలో ఫుట్ అండ్ మౌత్ డిసీజ్‌కు సంబంధించిన లక్షణాలు "
                    "ఉన్నట్లు కనిపిస్తున్నాయి. నోరు లేదా కాళ్ల చుట్టూ గాయాలు, "
                    "ఆహారం తీసుకోవడంలో లేదా నడకలో మార్పులు కనిపించవచ్చు. "
                    "చిత్రం ఆధారంగా మాత్రమే వ్యాధిని ఖచ్చితంగా నిర్ధారించలేము."
                ),

                "precautions": [
                    "అనుమానిత జంతువును ఆరోగ్యకరమైన జంతువుల నుంచి వేరు ఉంచండి.",
                    "జంతువును అవసరం లేకుండా ఎక్కువగా తరలించవద్దు.",
                    "ఆహారం మరియు విశ్రాంతి ప్రదేశాలను శుభ్రంగా ఉంచండి.",
                    "జంతువుల మధ్య పరికరాలను పంచుకోవడం నివారించండి.",
                    "ఆహారం తీసుకోవడం, నడక మరియు నోరు లేదా కాళ్ల మార్పులను గమనించండి."
                ],

                "care": [
                    "శుభ్రమైన తాగునీరు మరియు సరైన పోషకాహారం అందించండి.",
                    "జంతువును శుభ్రమైన మరియు సౌకర్యవంతమైన ప్రదేశంలో ఉంచండి.",
                    "నడక మరియు ఆహారం తీసుకోవడంలో మార్పులను జాగ్రత్తగా గమనించండి.",
                    "వ్యాధి నియంత్రణ కోసం పశువైద్యుల సూచనలను పాటించండి."
                ],

                "avoid": [
                    "అనుమానిత జంతువును ఆరోగ్యకరమైన జంతువులతో కలపవద్దు.",
                    "అవసరం లేని రవాణా లేదా తరలింపును నివారించండి.",
                    "పశువైద్యుల సలహా లేకుండా మందులు ఇవ్వవద్దు.",
                    "నోరు లేదా కాళ్లలో గాయాలు, ఆహారం తగ్గడం వంటి లక్షణాలను నిర్లక్ష్యం చేయవద్దు."
                ],

                "veterinarian": (
                    "ఫుట్ అండ్ మౌత్ డిసీజ్ ఇతర జంతువులకు కూడా వ్యాపించే అవకాశం "
                    "ఉన్నందున పశువైద్యుల సహాయం చాలా ముఖ్యం. లక్షణాలు అనుమానంగా "
                    "కనిపించిన వెంటనే నిపుణుల సలహా తీసుకోండి."
                ),

                "risk_alert": risk_alert_te
            }
        }

    # --------------------------------------------------------
    # UNKNOWN CONDITION
    # --------------------------------------------------------

    return {
        "english": {
            "overview": (
                f"The prediction for this {animal_type.lower()} suggests "
                f"{predicted_condition}. The result should be treated as "
                "an image-based indication and not as a confirmed diagnosis."
            ),

            "precautions": [
                "Keep the animal in a clean and comfortable environment.",
                "Provide clean drinking water.",
                "Monitor eating, drinking and normal activity.",
                "Observe the animal for any new or worsening symptoms."
            ],

            "care": [
                "Provide suitable nutrition and adequate rest.",
                "Maintain good hygiene around the animal.",
                "Continue regular health monitoring.",
                "Follow veterinary advice when symptoms are present."
            ],

            "avoid": [
                "Do not give medicines without veterinary advice.",
                "Do not ignore worsening symptoms.",
                "Avoid unhygienic surroundings."
            ],

            "veterinarian": (
                "If symptoms persist or become worse, consult a qualified "
                "veterinarian for proper examination and confirmation."
            ),

            "risk_alert": risk_alert_en
        },

        "telugu": {
            "overview": (
                f"ఈ {animal_type.lower()}కు {predicted_condition} ఉన్నట్లు "
                "చిత్ర ఆధారిత అంచనా సూచిస్తోంది. దీనిని ఖచ్చితమైన వ్యాధి "
                "నిర్ధారణగా పరిగణించకూడదు."
            ),

            "precautions": [
                "జంతువును శుభ్రమైన మరియు సౌకర్యవంతమైన ప్రదేశంలో ఉంచండి.",
                "శుభ్రమైన తాగునీరు అందించండి.",
                "ఆహారం, నీరు తీసుకోవడం మరియు సాధారణ చలనాన్ని గమనించండి.",
                "కొత్తగా లేదా ఎక్కువగా కనిపించే లక్షణాలను గమనించండి."
            ],

            "care": [
                "సరైన పోషకాహారం మరియు తగినంత విశ్రాంతి అందించండి.",
                "జంతువు పరిసరాల్లో పరిశుభ్రత పాటించండి.",
                "క్రమం తప్పకుండా ఆరోగ్యాన్ని గమనించండి.",
                "లక్షణాలు ఉంటే పశువైద్యుల సలహాను పాటించండి."
            ],

            "avoid": [
                "పశువైద్యుల సలహా లేకుండా మందులు ఇవ్వవద్దు.",
                "లక్షణాలు తీవ్రమవుతున్నా నిర్లక్ష్యం చేయవద్దు.",
                "అపరిశుభ్రమైన పరిసరాలను నివారించండి."
            ],

            "veterinarian": (
                "లక్షణాలు కొనసాగితే లేదా తీవ్రంగా మారితే సరైన పరీక్ష మరియు "
                "నిర్ధారణ కోసం అర్హత కలిగిన పశువైద్యులను సంప్రదించండి."
            ),

            "risk_alert": risk_alert_te
        }
    }


# ============================================================
# 4. AUTOMATIC HEALTH GUIDANCE GENERATOR
# ============================================================

def generate_health_guidance(
    animal_type,
    predicted_condition,
    confidence,
    risk_level
):
    """
    Automatically generates bilingual health guidance.

    Parameters
    ----------
    animal_type : str
        Cow or Buffalo

    predicted_condition : str
        Detected condition

    confidence : float
        Prediction confidence

    risk_level : str
        Low / Medium / High

    Returns
    -------
    dict
        Structured English + Telugu guidance
    """

    # --------------------------------------------------------
    # Validate values
    # --------------------------------------------------------

    animal_type = str(animal_type or "Cattle")
    predicted_condition = str(
        predicted_condition or "Unknown condition"
    )
    risk_level = str(risk_level or "Low")

    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.0

    # --------------------------------------------------------
    # Low confidence warning
    # --------------------------------------------------------

    confidence_warning_en = ""

    confidence_warning_te = ""

    if confidence < 0.60:

        confidence_warning_en = (
            "The prediction confidence is relatively low, so this "
            "result should be treated with extra caution and verified "
            "by a veterinarian."
        )

        confidence_warning_te = (
            "అంచనా నమ్మక స్థాయి తక్కువగా ఉంది. కాబట్టి ఈ ఫలితాన్ని "
            "జాగ్రత్తగా పరిగణించి, పశువైద్యుల ద్వారా నిర్ధారించుకోవడం మంచిది."
        )

    # --------------------------------------------------------
    # Try automatic generation
    # --------------------------------------------------------

    if _client is not None:

        prompt = f"""
You are generating safe health guidance for a cattle health application.

Prediction information:

Animal type: {animal_type}
Predicted condition: {predicted_condition}
Confidence: {confidence:.2%}
Risk level: {risk_level}

Create guidance in BOTH English and natural Telugu.

The response MUST be valid JSON with exactly this structure:

{{
  "english": {{
    "overview": "string",
    "precautions": ["string", "string", "string"],
    "care": ["string", "string", "string"],
    "avoid": ["string", "string", "string"],
    "veterinarian": "string",
    "risk_alert": "string"
  }},
  "telugu": {{
    "overview": "string",
    "precautions": ["string", "string", "string"],
    "care": ["string", "string", "string"],
    "avoid": ["string", "string", "string"],
    "veterinarian": "string",
    "risk_alert": "string"
  }}
}}

Rules:

1. The guidance must be specific to the animal type, condition,
   confidence and risk level.
2. Do not claim that the image prediction is a confirmed diagnosis.
3. If confidence is low, clearly explain that the result is uncertain.
4. Do not prescribe medicines, injections, antibiotics or dosages.
5. Recommend veterinary verification when appropriate.
6. For a healthy prediction, provide preventive care only.
7. For Lumpy Skin Disease, discuss relevant hygiene, isolation,
   insect control and monitoring precautions.
8. For Mastitis, discuss udder hygiene, milking hygiene and monitoring.
9. For Foot and Mouth Disease, discuss isolation, hygiene,
   limiting movement and veterinary attention.
10. Use simple language suitable for cattle owners.
11. Telugu must be natural and easy to understand.
12. English and Telugu must communicate equivalent information.
13. Risk alert must match the supplied risk level.
"""

        try:

            response = _client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            response_text = response.text.strip()

            # ------------------------------------------------
            # Remove accidental markdown JSON fences
            # ------------------------------------------------

            if response_text.startswith("```"):
                response_text = response_text.replace(
                    "```json", ""
                ).replace(
                    "```", ""
                ).strip()

            generated = json.loads(response_text)

            # ------------------------------------------------
            # Validate required structure
            # ------------------------------------------------

            required_sections = [
                "overview",
                "precautions",
                "care",
                "avoid",
                "veterinarian",
                "risk_alert"
            ]

            for language in ["english", "telugu"]:

                if language not in generated:
                    raise ValueError(
                        f"Missing language section: {language}"
                    )

                for section in required_sections:

                    if section not in generated[language]:
                        raise ValueError(
                            f"Missing section: {language}.{section}"
                        )

            # ------------------------------------------------
            # Add confidence warning
            # ------------------------------------------------

            if confidence_warning_en:

                generated["english"]["overview"] += (
                    " " + confidence_warning_en
                )

                generated["telugu"]["overview"] += (
                    " " + confidence_warning_te
                )

            return generated

        except Exception as error:

            print("HEALTH GUIDANCE ERROR:")
            print(error)

    # --------------------------------------------------------
    # Safe fallback
    # --------------------------------------------------------

    guidance = fallback_guidance(
        animal_type=animal_type,
        predicted_condition=predicted_condition,
        confidence=confidence,
        risk_level=risk_level
    )

    if confidence_warning_en:

        guidance["english"]["overview"] += (
            " " + confidence_warning_en
        )

        guidance["telugu"]["overview"] += (
            " " + confidence_warning_te
        )

    return guidance
