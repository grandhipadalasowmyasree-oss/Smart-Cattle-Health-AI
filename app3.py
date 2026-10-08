# ============================================================
# SMART CATTLE HEALTH AI - COMPLETE APP
# ============================================================

import base64
import json
import mimetypes
import re
import html

from pathlib import Path
from datetime import datetime
from login import render_login
import streamlit as st
import pandas as pd
from PIL import Image
from ultralytics import YOLO
import streamlit.components.v1 as components
from dotenv import load_dotenv

from chatbot import render_chatbot
from health_guidance import generate_health_guidance
from ground_work_page import render_ground_work


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Smart Cattle Care - Health AI",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# LOGIN CHECK
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    render_login()
    st.stop()


# ============================================================
# GLOBAL LIGHT SKY BLUE THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       FONT
       ====================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap'
    );


    /* ======================================================
       GLOBAL LIGHT SKY BLUE BACKGROUND
       ====================================================== */

    html,
    body,
    #root,
    .stApp,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    .main,
    .block-container {

        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(173, 216, 230, 0.42),
                transparent 30%
            ),

            radial-gradient(
                circle at 90% 20%,
                rgba(135, 206, 235, 0.30),
                transparent 30%
            ),

            radial-gradient(
                circle at 50% 90%,
                rgba(176, 226, 243, 0.28),
                transparent 35%
            ),

            linear-gradient(
                135deg,
                #DDF5FF 0%,
                #EAF9FF 35%,
                #DFF5FF 65%,
                #CFEFFF 100%
            ) !important;

        color: #17324D !important;

        min-height: 100vh !important;

        font-family:
            'Poppins',
            sans-serif !important;
    }


    /* ======================================================
       MAIN CONTENT
       ====================================================== */

    .block-container {

        max-width: 1400px !important;

        padding-top: 1rem !important;

        padding-bottom: 3rem !important;

        padding-left: 1.5rem !important;

        padding-right: 1.5rem !important;

        background: transparent !important;
    }


    /* ======================================================
       HEADER
       ====================================================== */

    header[data-testid="stHeader"] {

        background: transparent !important;

        box-shadow: none !important;
    }


    /* ======================================================
       TOOLBAR
       ====================================================== */

    [data-testid="stToolbar"] {

        background: transparent !important;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #C7EFFB 0%,
                #B8E7F5 50%,
                #A9DFF0 100%
            ) !important;
    }


    [data-testid="stSidebar"] * {

        color: #17324D !important;

        font-family:
            'Poppins',
            sans-serif !important;
    }


    /* ======================================================
       FONT
       ====================================================== */

    button,
    input,
    textarea,
    select,
    label,
    p,
    span,
    div,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {

        font-family:
            'Poppins',
            sans-serif !important;
    }


    /* ======================================================
       HEADINGS
       ====================================================== */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {

        color:
            #124B70 !important;
    }


    /* ======================================================
       TEXT
       ====================================================== */

    p,
    label {

        color:
            #234B63 !important;
    }


    /* ======================================================
       TOP NAVIGATION BUTTONS
       ====================================================== */

    .stButton > button {

        border-radius:
            10px !important;

        border:
            1px solid
            #9FD5E7 !important;

        background:
            rgba(255,255,255,0.78) !important;

        color:
            #17658A !important;

        font-weight:
            700 !important;

        min-height:
            44px !important;

        box-shadow:
            0 3px 10px
            rgba(72,145,175,0.08) !important;

        transition:
            all 0.2s ease !important;
    }


    .stButton > button:hover {

        background:
            #DDF5FF !important;

        color:
            #0F5877 !important;

        border-color:
            #62BCD9 !important;

        box-shadow:
            0 5px 16px
            rgba(72,145,175,0.15) !important;
    }


    button[kind="primary"] {

        background:
            #2A86AD !important;

        color:
            #FFFFFF !important;

        border:
            none !important;
    }


    button[kind="primary"]:hover {

        background:
            #216F91 !important;

        color:
            #FFFFFF !important;
    }


    /* ======================================================
       FILE UPLOADER
       ====================================================== */

    [data-testid="stFileUploader"] {

        background:
            rgba(255,255,255,0.72) !important;

        border:
            1px solid
            #9FD5E7 !important;

        border-radius:
            14px !important;
    }


    /* ======================================================
       INPUT BOXES
       ====================================================== */

    input,
    textarea {

        background:
            rgba(255,255,255,0.95) !important;

        color:
            #263238 !important;

        border:
            1px solid
            #B7DDEA !important;

        border-radius:
            10px !important;
    }


    /* ======================================================
       SELECT BOX
       ====================================================== */

    [data-baseweb="select"] > div {

        background:
            rgba(255,255,255,0.95) !important;

        color:
            #263238 !important;

        border-radius:
            10px !important;
    }


    /* ======================================================
       METRICS
       ====================================================== */

    [data-testid="stMetric"] {

        background:
            rgba(255,255,255,0.72) !important;

        border:
            1px solid
            #B6DFEC !important;

        border-radius:
            14px !important;

        padding:
            16px !important;

        box-shadow:
            0 5px 18px
            rgba(80,160,190,0.10) !important;
    }


    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {

        color:
            #174B67 !important;
    }


    /* ======================================================
       ALERTS
       ====================================================== */

    [data-testid="stAlert"] {

        border-radius:
            12px !important;
    }


    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {

        border:
            none !important;

        border-top:
            1px solid
            rgba(70,145,175,0.22) !important;

        margin:
            15px 0 25px 0 !important;
    }


    /* ======================================================
       IFRAME
       ====================================================== */

    iframe {

        border:
            none !important;

        background:
            transparent !important;
    }


    /* ======================================================
       AI DETECTION SECTION TITLE
       ====================================================== */

    .ai-section-title {

        color:
            #124B70 !important;

        font-size:
            21px !important;

        font-weight:
            800 !important;

        margin-bottom:
            12px !important;

        margin-top:
            5px !important;
    }


    /* ======================================================
       ANIMAL LABEL
       ====================================================== */

    .animal-label {

        color:
            #124B70 !important;

        font-size:
            21px !important;

        font-weight:
            800 !important;

        margin-bottom:
            12px !important;
    }


    /* ======================================================
       SELECTED ANIMAL
       ====================================================== */

    .animal-selected {

        background:
            #DDF5FF !important;

        border:
            2px solid
            #4CA7C8 !important;

        color:
            #124B70 !important;

        border-radius:
            12px !important;

        padding:
            12px 15px !important;

        text-align:
            center !important;

        font-size:
            16px !important;

        font-weight:
            800 !important;

        margin-top:
            12px !important;
    }


    /* ======================================================
       DIAGNOSIS ANIMAL
       ====================================================== */

    .diagnosis-animal {

        background:
            rgba(255,255,255,0.70) !important;

        border:
            1px solid
            #B6DFEC !important;

        border-radius:
            12px !important;

        padding:
            14px 16px !important;

        margin:
            8px 0 15px 0 !important;

        color:
            #174C68 !important;

        font-size:
            16px;

        font-weight:
            700;
    }


    /* ======================================================
       RADIO BUTTONS
       ====================================================== */

    [data-testid="stRadio"] label {

        color:
            #234B63 !important;
    }


    /* ======================================================
       SLIDER
       ====================================================== */

    [data-testid="stSlider"] label {

        color:
            #124B70 !important;

        font-weight:
            600 !important;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    footer {

        background:
            transparent !important;

        color:
            #46758A !important;
    }


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 768px) {

        .block-container {

            padding-left:
                0.8rem !important;

            padding-right:
                0.8rem !important;
        }

        .stButton > button {

            font-size:
                11px !important;

            min-height:
                40px !important;
        }

        .animal-label {

            font-size:
                18px !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

IMAGES_DIR = BASE_DIR / "images"

LOGO_DIR = BASE_DIR / "assests" / "logos"


# ============================================================
# LOGO PATHS
# ============================================================

LOGO_PATHS = {

    "microsoft":
        LOGO_DIR / "mlogo.png",

    "edunet":
        LOGO_DIR / "elogo.png",

    "ministry":
        LOGO_DIR / "sdlogo.png",

    "skill":
        LOGO_DIR / "skilllogo.png",

    "skillap":
        LOGO_DIR / "saplogo.png",

    "sap":
        LOGO_DIR / "saplogo.png"

}


def get_local_image_data(image_path):

    image_path = Path(image_path)

    if not image_path.is_file():

        return None

    try:

        image_bytes = image_path.read_bytes()
        mime_type = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
        encoded_image = base64.b64encode(image_bytes).decode("ascii")

        return f"data:{mime_type};base64,{encoded_image}"

    except OSError:

        return None


# ============================================================
# VALID PAGES
# ============================================================

VALID_PAGES = {

    "Home",
    "Detection",
    "Assistant",
    "Ground Work",
    "Diseases",
    "About"

}


# ============================================================
# QUERY PARAMETER PAGE SUPPORT
# ============================================================

def get_query_page():

    try:

        if hasattr(
            st,
            "query_params"
        ):

            page = st.query_params.get(
                "page"
            )

        else:

            params = (
                st.experimental_get_query_params()
            )

            page = params.get(
                "page",
                [None]
            )[0]


        if isinstance(
            page,
            list
        ):

            page = (
                page[0]
                if page
                else None
            )


        if page in VALID_PAGES:

            return page


    except Exception:

        pass


    return None


requested_page = get_query_page()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:

    st.session_state.page = "Home"


if requested_page in VALID_PAGES:

    st.session_state.page = requested_page


if "detection_history" not in st.session_state:

    st.session_state.detection_history = []


if "selected_animal" not in st.session_state:

    st.session_state.selected_animal = "Cow"


# ============================================================
# SAFE RERUN
# ============================================================

def safe_rerun():

    if hasattr(
        st,
        "rerun"
    ):

        st.rerun()

    elif hasattr(
        st,
        "experimental_rerun"
    ):

        st.experimental_rerun()


# ============================================================
# TOP NAVIGATION
# ============================================================

def render_top_navigation():

    nav_items = [

        (
            "HOME",
            "Home"
        ),

        (
            "AI DETECT",
            "Detection"
        ),

        (
            "AI ASSISTANT",
            "Assistant"
        ),

        (
            "GROUND WORK",
            "Ground Work"
        ),

        (
            "DISEASES",
            "Diseases"
        ),

        (
            "ABOUT",
            "About"
        )

    ]


    columns = st.columns(
        6,
        gap="small"
    )


    for index, (
        label,
        page_name
    ) in enumerate(
        nav_items
    ):

        with columns[index]:

            if st.button(
                label,
                key=f"top_navigation_{index}",
                use_container_width=True
            ):

                st.session_state.page = (
                    page_name
                )

                safe_rerun()


    # ========================================================
    # NAVIGATION LINE
    # ========================================================

    st.markdown(
        """
        <div style="
            height:1px;
            background:rgba(70,145,175,0.25);
            margin-top:8px;
            margin-bottom:18px;
            width:100%;
        "></div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MODEL PATHS
# ============================================================

COW_MODEL_PATH = Path(
    r"C:\Users\grand\Downloads\Smart-Cattle-Health-Detection"
    r"\Smart-Cattle-Health-Detection"
    r"\cattle_detection.v3i.yolov5pytorch"
    r"\runs\detect\cattle_4class_final-2"
    r"\weights\best.pt"
)


BUFFALO_MODEL_PATH = Path(
    r"C:\Users\grand\OneDrive\Desktop\version1_smart cattle"
    r"\buffalo"
    r"\cattle_detection.v1i.yolov5pytorch"
    r"\runs\detect\runs\detect\buffalo_clean_4class"
    r"\weights\best.pt"
)


# ============================================================
# DATASET PATHS
# ============================================================

COW_DATASET_PATH = Path(
    r"C:\Users\grand\Downloads\Smart-Cattle-Health-Detection"
    r"\Smart-Cattle-Health-Detection"
    r"\cattle_detection.v3i.yolov5pytorch"
)


BUFFALO_DATASET_PATH = Path(
    r"C:\Users\grand\OneDrive\Desktop\version1_smart cattle"
    r"\buffalo"
    r"\cattle_detection.v1i.yolov5pytorch"
)


# ============================================================
# LOAD YOLO MODELS
# ============================================================

@st.cache_resource
def load_models():

    cow_model = None
    buffalo_model = None

    cow_error = None
    buffalo_error = None


    # --------------------------------------------------------
    # COW
    # --------------------------------------------------------

    try:

        if COW_MODEL_PATH.exists():

            cow_model = YOLO(
                str(COW_MODEL_PATH)
            )

        else:

            cow_error = (
                "Cow model not found."
            )

    except Exception as error:

        cow_error = str(
            error
        )


    # --------------------------------------------------------
    # BUFFALO
    # --------------------------------------------------------

    try:

        if BUFFALO_MODEL_PATH.exists():

            buffalo_model = YOLO(
                str(BUFFALO_MODEL_PATH)
            )

        else:

            buffalo_error = (
                "Buffalo model not found."
            )

    except Exception as error:

        buffalo_error = str(
            error
        )


    return (
        cow_model,
        buffalo_model,
        cow_error,
        buffalo_error
    )


(
    cow_model,
    buffalo_model,
    cow_error,
    buffalo_error
) = load_models()


# ============================================================
# DISEASE NORMALIZATION
# ============================================================

def normalize_disease(
    name
):

    name = str(
        name
    ).lower().strip()


    if "foot" in name:

        return "Foot-and-Mouth Disease"


    if "lumpy" in name:

        return "Lumpy Skin Disease"


    if "mastitis" in name:

        return "Mastitis"


    if "healthy" in name:

        return "Healthy Cattle"


    return (
        name
        .replace("_", " ")
        .title()
    )


# ============================================================
# CLASS NAME
# ============================================================

def get_class_name(
    model,
    class_id
):

    try:

        names = model.names


        if isinstance(
            names,
            dict
        ):

            return str(
                names.get(
                    class_id,
                    class_id
                )
            )


        return str(
            names[class_id]
        )


    except Exception:

        return str(
            class_id
        )


# ============================================================
# DISEASE DETECTION
# ============================================================

def detect_disease(
    model,
    image,
    confidence
):

    if model is None:

        return (
            None,
            None,
            None
        )


    try:

        results = model.predict(
            source=image,
            conf=confidence,
            imgsz=640,
            verbose=False
        )


        if not results:

            return (
                None,
                None,
                None
            )


        result = results[0]


        if (
            result.boxes is None
            or len(result.boxes) == 0
        ):

            return (
                None,
                None,
                None
            )


        # ----------------------------------------------------
        # BEST CONFIDENCE BOX
        # ----------------------------------------------------

        best_index = int(
            result.boxes.conf.argmax()
        )


        class_id = int(
            result.boxes.cls[
                best_index
            ]
        )


        prediction_confidence = float(
            result.boxes.conf[
                best_index
            ]
        )


        disease_name = get_class_name(
            model,
            class_id
        )


        # ----------------------------------------------------
        # KEEP ONLY BEST BOX
        # ----------------------------------------------------

        result.boxes = result.boxes[
            best_index:
            best_index + 1
        ]


        annotated = result.plot()


        # BGR -> RGB

        annotated = annotated[
            :,
            :,
            ::-1
        ]


        return (
            annotated,
            normalize_disease(
                disease_name
            ),
            prediction_confidence
        )


    except Exception as error:

        st.error(
            "Unable to analyze image: "
            + str(error)
        )


        return (
            None,
            None,
            None
        )


# ============================================================
# CLEAN GUIDANCE TEXT
# ============================================================

def clean_guidance_text(
    value
):

    if value is None:

        return ""


    if isinstance(
        value,
        list
    ):

        cleaned_items = []


        for item in value:

            item_text = (
                clean_guidance_text(
                    item
                )
            )


            if item_text:

                cleaned_items.append(
                    item_text
                )


        return cleaned_items


    text = str(
        value
    )


    text = html.unescape(
        text
    )


    text = re.sub(
        r"<br\s*/?>",
        "\n",
        text,
        flags=re.IGNORECASE
    )


    text = re.sub(
        r"<li\b[^>]*>",
        "• ",
        text,
        flags=re.IGNORECASE
    )


    text = re.sub(
        r"</li>",
        "\n",
        text,
        flags=re.IGNORECASE
    )


    text = re.sub(
        r"<(p|div|h1|h2|h3|h4|h5|h6)\b[^>]*>",
        "\n",
        text,
        flags=re.IGNORECASE
    )


    text = re.sub(
        r"</(p|div|h1|h2|h3|h4|h5|h6)>",
        "\n",
        text,
        flags=re.IGNORECASE
    )


    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )


    text = re.sub(
        r"^\s*(html|svg|css|javascript|js|xml)\s*$",
        "",
        text,
        flags=re.IGNORECASE | re.MULTILINE
    )


    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )


    return text.strip()


# ============================================================
# HEALTH GUIDANCE
# ============================================================

def render_health_guidance(
    animal_name,
    disease,
    confidence,
    risk_level
):

    risk_text = str(
        risk_level
    ).upper()


    if "HIGH" in risk_text:

        guidance_risk = "High"

    elif "MEDIUM" in risk_text:

        guidance_risk = "Medium"

    else:

        guidance_risk = "Low"


    with st.spinner(
        "Preparing personalized health guidance..."
    ):

        try:

            guidance = generate_health_guidance(
                animal_type=animal_name,
                predicted_condition=disease,
                confidence=confidence,
                risk_level=guidance_risk
            )

        except Exception as error:

            st.error(
                "Unable to prepare health guidance."
            )

            print(
                "HEALTH GUIDANCE ERROR:",
                error
            )

            return


    if not guidance:

        st.warning(
            "Health guidance is currently unavailable."
        )

        return


    if isinstance(
        guidance,
        dict
    ):

        english = guidance.get(
            "english",
            {}
        )

        telugu = guidance.get(
            "telugu",
            {}
        )

    else:

        english = {
            "overview":
                str(guidance)
        }

        telugu = {}


    st.markdown("---")

    st.markdown(
        "## 🩺 Health Guidance"
    )

    st.caption(
        "Personalized guidance based on the detected "
        "condition and risk level."
    )


    english_risk = clean_guidance_text(
        english.get(
            "risk_alert",
            ""
        )
    )


    telugu_risk = clean_guidance_text(
        telugu.get(
            "risk_alert",
            ""
        )
    )


    if guidance_risk == "High":

        if english_risk:

            st.error(
                "🔴 HIGH RISK\n\n"
                + english_risk
            )

        else:

            st.error(
                "🔴 HIGH RISK"
            )


    elif guidance_risk == "Medium":

        if english_risk:

            st.warning(
                "🟠 MEDIUM RISK\n\n"
                + english_risk
            )

        else:

            st.warning(
                "🟠 MEDIUM RISK"
            )


    else:

        if english_risk:

            st.success(
                "🟢 LOW RISK\n\n"
                + english_risk
            )

        else:

            st.success(
                "🟢 LOW RISK"
            )


    english_col, telugu_col = st.columns(
        2
    )


    # ========================================================
    # ENGLISH
    # ========================================================

    with english_col:

        st.markdown(
            "### 🇬🇧 English"
        )


        english_sections = [

            (
                "Condition Overview",
                "overview"
            ),

            (
                "Immediate Precautions",
                "precautions"
            ),

            (
                "Recommended Care",
                "care"
            ),

            (
                "What to Avoid",
                "avoid"
            ),

            (
                "Veterinarian Recommendation",
                "veterinarian"
            )

        ]


        for title, key in english_sections:

            value = clean_guidance_text(
                english.get(
                    key,
                    ""
                )
            )


            if not value:

                continue


            st.markdown(
                "#### "
                + title
            )


            if isinstance(
                value,
                list
            ):

                for item in value:

                    item_text = (
                        clean_guidance_text(
                            item
                        )
                    )


                    if item_text:

                        st.write(
                            "• "
                            + str(item_text)
                        )

            else:

                st.write(
                    value
                )


    # ========================================================
    # TELUGU
    # ========================================================

    with telugu_col:

        st.markdown(
            "### 🇮🇳 తెలుగు"
        )


        telugu_sections = [

            (
                "వ్యాధి వివరణ",
                "overview"
            ),

            (
                "తక్షణ జాగ్రత్తలు",
                "precautions"
            ),

            (
                "సూచించబడిన సంరక్షణ",
                "care"
            ),

            (
                "ఏమి నివారించాలి",
                "avoid"
            ),

            (
                "పశువైద్యుల సలహా",
                "veterinarian"
            )

        ]


        for title, key in telugu_sections:

            value = clean_guidance_text(
                telugu.get(
                    key,
                    ""
                )
            )


            if not value:

                continue


            st.markdown(
                "#### "
                + title
            )


            if isinstance(
                value,
                list
            ):

                for item in value:

                    item_text = (
                        clean_guidance_text(
                            item
                        )
                    )


                    if item_text:

                        st.write(
                            "• "
                            + str(item_text)
                        )

            else:

                st.write(
                    value
                )


    if telugu_risk:

        st.info(
            "🇮🇳 తెలుగు\n\n"
            + telugu_risk
        )


    st.caption(
        "AI screening and this guidance are intended for "
        "general health support only. They do not replace "
        "professional veterinary examination or diagnosis."
    )


# ============================================================
# DATASET SCANNER
# ============================================================

def scan_dataset(
    dataset_path,
    model
):

    counts = {

        "images": 0,
        "healthy": 0,
        "lumpy": 0,
        "foot": 0,
        "mastitis": 0

    }


    if (
        model is None
        or not dataset_path.exists()
    ):

        return counts


    image_extensions = {

        ".jpg",
        ".jpeg",
        ".png",
        ".webp"

    }


    processed_images = set()


    try:

        for split in [
            "train",
            "valid",
            "test"
        ]:

            images_dir = (
                dataset_path
                / split
                / "images"
            )


            labels_dir = (
                dataset_path
                / split
                / "labels"
            )


            if not images_dir.exists():

                continue


            for image_path in images_dir.iterdir():

                if (
                    not image_path.is_file()
                    or image_path.suffix.lower()
                    not in image_extensions
                ):

                    continue


                image_key = str(
                    image_path.resolve()
                ).lower()


                if image_key in processed_images:

                    continue


                processed_images.add(
                    image_key
                )


                counts["images"] += 1


                label_path = (
                    labels_dir
                    / (
                        image_path.stem
                        + ".txt"
                    )
                )


                if not label_path.exists():

                    continue


                detected_classes = set()


                try:

                    with open(
                        label_path,
                        "r",
                        encoding="utf-8"
                    ) as label_file:

                        for line in label_file:

                            parts = (
                                line.strip()
                                .split()
                            )


                            if not parts:

                                continue


                            try:

                                class_id = int(
                                    float(
                                        parts[0]
                                    )
                                )


                                detected_classes.add(
                                    class_id
                                )


                            except Exception:

                                continue


                except Exception:

                    continue


                for class_id in detected_classes:

                    class_name = normalize_disease(
                        get_class_name(
                            model,
                            class_id
                        )
                    )


                    name = class_name.lower()


                    if "healthy" in name:

                        counts["healthy"] += 1

                    elif "lumpy" in name:

                        counts["lumpy"] += 1

                    elif "foot" in name:

                        counts["foot"] += 1

                    elif "mastitis" in name:

                        counts["mastitis"] += 1


    except Exception:

        pass


    return counts


# ============================================================
# DASHBOARD DATA
# ============================================================

def get_dashboard_data():

    cow_data = scan_dataset(
        COW_DATASET_PATH,
        cow_model
    )


    buffalo_data = scan_dataset(
        BUFFALO_DATASET_PATH,
        buffalo_model
    )


    history = st.session_state.get(
        "detection_history",
        []
    )


    history_df = pd.DataFrame(
        history
    )


    # ========================================================
    # COW IMAGE FALLBACK
    # ========================================================

    if cow_data["images"] == 0:

        if not history_df.empty:

            cow_data["images"] = int(
                (
                    history_df["Animal"]
                    .astype(str)
                    .str.lower()
                    == "cow"
                ).sum()
            )


    # ========================================================
    # BUFFALO IMAGE FALLBACK
    # ========================================================

    if buffalo_data["images"] == 0:

        if not history_df.empty:

            buffalo_data["images"] = int(
                (
                    history_df["Animal"]
                    .astype(str)
                    .str.lower()
                    == "buffalo"
                ).sum()
            )


    # ========================================================
    # COW FALLBACK
    # ========================================================

    if (
        cow_data["healthy"]
        + cow_data["lumpy"]
        + cow_data["foot"]
        + cow_data["mastitis"]
        == 0
    ):

        if not history_df.empty:

            cow_df = history_df[
                history_df["Animal"]
                .astype(str)
                .str.lower()
                == "cow"
            ]


            if not cow_df.empty:

                disease_col = (
                    cow_df["Disease"]
                    .astype(str)
                )


                cow_data["healthy"] = int(
                    disease_col.str.contains(
                        "healthy",
                        case=False,
                        na=False
                    ).sum()
                )


                cow_data["lumpy"] = int(
                    disease_col.str.contains(
                        "lumpy",
                        case=False,
                        na=False
                    ).sum()
                )


                cow_data["foot"] = int(
                    disease_col.str.contains(
                        "foot",
                        case=False,
                        na=False
                    ).sum()
                )


                cow_data["mastitis"] = int(
                    disease_col.str.contains(
                        "mastitis",
                        case=False,
                        na=False
                    ).sum()
                )


    # ========================================================
    # BUFFALO FALLBACK
    # ========================================================

    if (
        buffalo_data["healthy"]
        + buffalo_data["lumpy"]
        + buffalo_data["foot"]
        + buffalo_data["mastitis"]
        == 0
    ):

        if not history_df.empty:

            buffalo_df = history_df[
                history_df["Animal"]
                .astype(str)
                .str.lower()
                == "buffalo"
            ]


            if not buffalo_df.empty:

                disease_col = (
                    buffalo_df["Disease"]
                    .astype(str)
                )


                buffalo_data["healthy"] = int(
                    disease_col.str.contains(
                        "healthy",
                        case=False,
                        na=False
                    ).sum()
                )


                buffalo_data["lumpy"] = int(
                    disease_col.str.contains(
                        "lumpy",
                        case=False,
                        na=False
                    ).sum()
                )


                buffalo_data["foot"] = int(
                    disease_col.str.contains(
                        "foot",
                        case=False,
                        na=False
                    ).sum()
                )


                buffalo_data["mastitis"] = int(
                    disease_col.str.contains(
                        "mastitis",
                        case=False,
                        na=False
                    ).sum()
                )


    # ========================================================
    # RECENT HISTORY
    # ========================================================

    recent = []


    if not history_df.empty:

        recent_df = (
            history_df
            .tail(6)
            .iloc[::-1]
        )


        for _, row in recent_df.iterrows():

            try:

                confidence_value = float(
                    row.get(
                        "Confidence",
                        0
                    )
                )

            except Exception:

                confidence_value = 0


            recent.append(
                {

                    "time":
                        str(
                            row.get(
                                "Time",
                                ""
                            )
                        ),

                    "animal":
                        str(
                            row.get(
                                "Animal",
                                ""
                            )
                        ),

                    "disease":
                        str(
                            row.get(
                                "Disease",
                                ""
                            )
                        ),

                    "confidence":
                        confidence_value,

                    "risk":
                        str(
                            row.get(
                                "Risk",
                                ""
                            )
                        )

                }
            )


    # ========================================================
    # TOTALS
    # ========================================================

    total_cows = cow_data["images"]

    total_buffaloes = buffalo_data["images"]

    total_images = (
        total_cows
        + total_buffaloes
    )


    total_healthy = (
        cow_data["healthy"]
        + buffalo_data["healthy"]
    )


    total_lumpy = (
        cow_data["lumpy"]
        + buffalo_data["lumpy"]
    )


    total_foot = (
        cow_data["foot"]
        + buffalo_data["foot"]
    )


    total_mastitis = (
        cow_data["mastitis"]
        + buffalo_data["mastitis"]
    )


    total_disease = (
        total_lumpy
        + total_foot
        + total_mastitis
    )


    return {

        "cow":
            total_cows,

        "buffalo":
            total_buffaloes,

        "images":
            total_images,

        "healthy":
            total_healthy,

        "lumpy":
            total_lumpy,

        "foot":
            total_foot,

        "mastitis":
            total_mastitis,

        "disease":
            total_disease,

        "cow_healthy":
            cow_data["healthy"],

        "cow_lumpy":
            cow_data["lumpy"],

        "cow_foot":
            cow_data["foot"],

        "cow_mastitis":
            cow_data["mastitis"],

        "buffalo_healthy":
            buffalo_data["healthy"],

        "buffalo_lumpy":
            buffalo_data["lumpy"],

        "buffalo_foot":
            buffalo_data["foot"],

        "buffalo_mastitis":
            buffalo_data["mastitis"],

        "recent":
            recent

    }


# ============================================================
# REPLACE LOGO PLACEHOLDERS
# ============================================================

def replace_logo_placeholders(
    html_content
):

    placeholder_mapping = {

        "__MICROSOFT_LOGO__":
            LOGO_PATHS["microsoft"],

        "__EDUNET_LOGO__":
            LOGO_PATHS["edunet"],

        "__MINISTRY_LOGO__":
            LOGO_PATHS["ministry"],

        "__SKILL_LOGO__":
            LOGO_PATHS["skill"],

        "__SKILLAP_LOGO__":
            LOGO_PATHS["skillap"],

        "__SAP_LOGO__":
            LOGO_PATHS["sap"]

    }


    for (
        placeholder,
        image_path
    ) in placeholder_mapping.items():

        image_data = get_local_image_data(
            image_path
        )


        if image_data:

            html_content = html_content.replace(
                placeholder,
                image_data
            )

        else:

            print(
                "LOGO NOT FOUND:",
                image_path
            )


    return html_content


# ============================================================
# APPLY LIGHT SKY BLUE THEME TO EMBEDDED HTML
# ============================================================

def apply_embedded_page_theme(
    html_content
):

    theme_css = """
    <style>

        html,
        body {

            margin: 0 !important;
            padding: 0 !important;

            width: 100% !important;
            min-height: 100% !important;

            background:
                linear-gradient(
                    135deg,
                    #DDF5FF 0%,
                    #EAF9FF 35%,
                    #DFF5FF 65%,
                    #CFEFFF 100%
                ) !important;

            color: #17324D !important;

            overflow-x: hidden !important;
        }

    </style>
    """


    # --------------------------------------------------------
    # Put the override at the end of the embedded HEAD
    # so it overrides page-level body background declarations.
    # --------------------------------------------------------

    if re.search(
        r"</head>",
        html_content,
        flags=re.IGNORECASE
    ):

        html_content = re.sub(
            r"</head>",
            theme_css + "\n</head>",
            html_content,
            count=1,
            flags=re.IGNORECASE
        )

    else:

        html_content = (
            theme_css
            + html_content
        )


    return html_content


# ============================================================
# HTML PAGE LOADER
# ============================================================

def show_html(
    filename
):

    html_file = (
        BASE_DIR
        / filename
    )


    if not html_file.exists():

        st.error(
            "File not found: "
            + str(html_file)
        )

        return


    try:

        with open(
            html_file,
            "r",
            encoding="utf-8"
        ) as file:

            html_content = file.read()


        # ====================================================
        # DISEASE IMAGES
        # ====================================================

        if filename == "diseases.html":

            disease_images = {

                "lumpy.jpg":
                    IMAGES_DIR
                    / "lumpy.jpg",

                "foot cow.jpg":
                    IMAGES_DIR
                    / "foot cow.jpg",

                "mastasis.jpg":
                    IMAGES_DIR
                    / "mastasis.jpg",

                "healthycow.jpg":
                    IMAGES_DIR
                    / "healthycow.jpg",

                "lumpybuffalo.jpg":
                    IMAGES_DIR
                    / "lumpybuffalo.jpg",

                "foot_mouth.jpg":
                    IMAGES_DIR
                    / "foot_mouth.jpg",

                "healthybuffalo.jpg":
                    IMAGES_DIR
                    / "healthybuffalo.jpg",

                "matasisbuffalo.jpg":
                    IMAGES_DIR
                    / "matasisbuffalo.jpg"

            }


            for (
                image_name,
                image_path
            ) in disease_images.items():

                image_data = get_local_image_data(
                    image_path
                )


                if image_data:

                    html_content = html_content.replace(
                        f"images/{image_name}",
                        image_data
                    )

                    html_content = html_content.replace(
                        f"./images/{image_name}",
                        image_data
                    )

                    html_content = html_content.replace(
                        image_name,
                        image_data
                    )


        # ====================================================
        # DASHBOARD
        # ====================================================

        if filename == "dashboard.html":

            dashboard_data = get_dashboard_data()


            dashboard_json = json.dumps(
                dashboard_data
            )


            html_content = html_content.replace(
                "__DASHBOARD_DATA__",
                dashboard_json
            )


            html_content = html_content.replace(
                "DASHBOARD_DATA",
                dashboard_json
            )


        # ====================================================
        # FORCE EMBEDDED PAGE LIGHT SKY BLUE
        # ====================================================

        html_content = apply_embedded_page_theme(
            html_content
        )


        # ====================================================
        # HTML WRAPPER
        # ====================================================

        full_html = f"""
        <!DOCTYPE html>

        <html>

        <head>

            <meta charset="UTF-8">

            <meta name="viewport"
                  content="width=device-width,
                  initial-scale=1.0">

            <style>

                html,
                body {{

                    margin: 0;
                    padding: 0;

                    width: 100%;
                    min-height: 100%;

                    background:
                        linear-gradient(
                            135deg,
                            #DDF5FF,
                            #EAF9FF,
                            #DFF5FF,
                            #CFEFFF
                        ) !important;

                }}

            </style>

        </head>

        <body>

            {html_content}

        </body>

        </html>
        """


        # ====================================================
        # DISEASES PAGE - MORE HEIGHT
        # ====================================================

        if filename == "diseases.html":

            components.html(
                full_html,
                height=3300,
                scrolling=True
            )

        else:

            components.html(
                full_html,
                height=2200,
                scrolling=False
            )


    except Exception as error:

        st.error(
            "Unable to load "
            + filename
            + ": "
            + str(error)
        )


# ============================================================
# HOME PAGE
# ============================================================

def render_home_page():

    home_file = (
        BASE_DIR
        / "home.html"
    )


    if not home_file.exists():

        st.error(
            "❌ home.html file not found."
        )

        st.info(
            "Please place home.html inside: "
            + str(BASE_DIR)
        )

        return


    try:

        with open(
            home_file,
            "r",
            encoding="utf-8"
        ) as file:

            home_html = file.read()


        # ====================================================
        # REPLACE HOME LOGOS
        # ====================================================

        home_html = (
            replace_logo_placeholders(
                home_html
            )
        )


        # ====================================================
        # LOAD styles.css
        # ====================================================

        css_file = (
            BASE_DIR
            / "styles.css"
        )


        css_content = ""


        if css_file.exists():

            try:

                with open(
                    css_file,
                    "r",
                    encoding="utf-8"
                ) as css:

                    css_content = css.read()

            except Exception as error:

                print(
                    "CSS LOAD ERROR:",
                    error
                )


        # ====================================================
        # HOME LIGHT SKY BLUE OVERRIDE
        # ====================================================

        home_html = apply_embedded_page_theme(
            home_html
        )


        # ====================================================
        # HOME HTML
        # ====================================================

        full_html = f"""
        <!DOCTYPE html>

        <html>

        <head>

            <meta charset="UTF-8">

            <meta name="viewport"
                  content="width=device-width,
                  initial-scale=1.0">

            <style>

                {css_content}

                html,
                body {{

                    margin: 0;
                    padding: 0;

                    width: 100%;
                    min-height: 100%;

                    background:
                        linear-gradient(
                            135deg,
                            #DDF5FF,
                            #EAF9FF,
                            #DFF5FF,
                            #CFEFFF
                        ) !important;

                }}

            </style>

        </head>

        <body>

            {home_html}

        </body>

        </html>
        """


        components.html(
            full_html,
            height=2500,
            scrolling=False
        )


    except Exception as error:

        st.error(
            "❌ Home page could not be loaded."
        )

        st.error(
            str(error)
        )


# ============================================================
# MAIN TOP NAVIGATION
# ============================================================

render_top_navigation()


# ============================================================
# HOME
# ============================================================

if st.session_state.page == "Home":

    render_home_page()


# ============================================================
# AI DETECTION
# ============================================================

elif st.session_state.page == "Detection":

    st.subheader(
        "🤖 Cattle Health AI Detection"
    )

    st.write(
        "Select animal type and upload an image "
        "to scan for diseases."
    )


    # ========================================================
    # MAIN COLUMNS
    # ========================================================

    col1, col2 = st.columns(
        2
    )


    # ========================================================
    # ANIMAL SELECTION
    # ========================================================

    with col1:

        st.markdown(
            """
            <div class="animal-label">
                1️⃣ Select Animal Type
            </div>
            """,
            unsafe_allow_html=True
        )


        animal_button_col1, animal_button_col2 = st.columns(
            2
        )


        # ----------------------------------------------------
        # COW
        # ----------------------------------------------------

        with animal_button_col1:

            if st.button(
                "🐄  COW",
                key="select_cow_button",
                use_container_width=True
            ):

                st.session_state.selected_animal = "Cow"

                safe_rerun()


        # ----------------------------------------------------
        # BUFFALO
        # ----------------------------------------------------

        with animal_button_col2:

            if st.button(
                "🐃  BUFFALO",
                key="select_buffalo_button",
                use_container_width=True
            ):

                st.session_state.selected_animal = "Buffalo"

                safe_rerun()


        # ====================================================
        # SELECTED ANIMAL
        # ====================================================

        animal = (
            st.session_state.selected_animal
        )


        if animal == "Cow":

            st.markdown(
                """
                <div class="animal-selected">
                    ✅ Selected Animal: 🐄 COW
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="animal-selected">
                    ✅ Selected Animal: 🐃 BUFFALO
                </div>
                """,
                unsafe_allow_html=True
            )


        # ====================================================
        # MODEL SELECTION
        # ====================================================

        if animal == "Cow":

            selected_model = cow_model

            animal_name = "Cow"

            default_confidence = 0.25

        else:

            selected_model = buffalo_model

            animal_name = "Buffalo"

            default_confidence = 0.05


        # ====================================================
        # MODEL CHECK
        # ====================================================

        if selected_model is None:

            st.error(
                animal_name
                + " model is not loaded."
            )


        # ====================================================
        # DETECTION SENSITIVITY
        # ====================================================

        st.markdown(
            """
            <div class="ai-section-title">
                2️⃣ Detection Sensitivity
            </div>
            """,
            unsafe_allow_html=True
        )


        confidence = st.slider(
            "Confidence Threshold",
            min_value=0.05,
            max_value=0.90,
            value=default_confidence,
            step=0.05,
            key="detection_confidence"
        )


    # ========================================================
    # IMAGE UPLOAD
    # ========================================================

    with col2:

        st.markdown(
            """
            <div class="ai-section-title">
                3️⃣ Upload Livestock Image
            </div>
            """,
            unsafe_allow_html=True
        )


        uploaded_file = st.file_uploader(
            "Upload clear image",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ],
            key="livestock_image_upload"
        )


    # ========================================================
    # PROCESS UPLOADED IMAGE
    # ========================================================

    if uploaded_file is not None:

        st.markdown("---")


        try:

            image = Image.open(
                uploaded_file
            ).convert(
                "RGB"
            )

        except Exception:

            st.error(
                "Unable to read the uploaded image."
            )

            image = None


        if image is not None:

            # =================================================
            # PREVIEW
            # =================================================

            preview_col1, preview_col2 = st.columns(
                2
            )


            with preview_col1:

                st.image(
                    image,
                    caption="Uploaded Image"
                )


            with preview_col2:

                st.info(
                    "Selected Animal: "
                    + animal_name
                )

                st.info(
                    "Confidence Threshold: "
                    + f"{confidence:.2f}"
                )


            st.markdown("---")


            # =================================================
            # RUN BUTTON
            # =================================================

            button_col1, button_col2, button_col3 = st.columns(
                [1, 2, 1]
            )


            with button_col2:

                run_btn = st.button(
                    "🔍 RUN DIAGNOSIS NOW",
                    use_container_width=True,
                    key="run_diagnosis_button"
                )


            # =================================================
            # RUN DETECTION
            # =================================================

            if run_btn:

                if selected_model is None:

                    st.error(
                        animal_name
                        + " model is not ready."
                    )

                else:

                    with st.spinner(
                        "Analyzing image..."
                    ):

                        (
                            result_image,
                            disease,
                            conf
                        ) = detect_disease(
                            selected_model,
                            image,
                            confidence
                        )


                    # =========================================
                    # NO DETECTION
                    # =========================================

                    if disease is None:

                        st.warning(
                            "⚠️ No disease detected. "
                            "Try lowering the confidence threshold."
                        )


                    else:

                        st.markdown("---")


                        # =====================================
                        # RESULT COLUMNS
                        # =====================================

                        res_col1, res_col2 = st.columns(
                            [1.1, 1]
                        )


                        conf_pct = (
                            conf * 100
                        )


                        # =====================================
                        # RISK
                        # =====================================

                        if (
                            "healthy"
                            in disease.lower()
                        ):

                            risk_level = (
                                "LOW (NO INFECTION)"
                            )

                        elif conf_pct >= 75:

                            risk_level = (
                                "HIGH RISK"
                            )

                        elif conf_pct >= 40:

                            risk_level = (
                                "MEDIUM RISK"
                            )

                        else:

                            risk_level = (
                                "LOW RISK"
                            )


                        # =====================================
                        # SESSION HISTORY
                        # =====================================

                        st.session_state.detection_history.append(
                            {

                                "Time":
                                    datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ),

                                "Animal":
                                    animal_name,

                                "Disease":
                                    disease,

                                "Confidence":
                                    round(
                                        conf_pct,
                                        2
                                    ),

                                "Risk":
                                    risk_level

                            }
                        )


                        # =====================================
                        # RESULT IMAGE
                        # =====================================

                        with res_col1:

                            st.image(
                                result_image,
                                caption="AI Detection Result"
                            )


                        # =====================================
                        # DIAGNOSIS REPORT
                        # =====================================

                        with res_col2:

                            st.subheader(
                                "📋 DIAGNOSIS REPORT"
                            )


                            st.markdown(
                                "## 🦠 "
                                + disease
                            )


                            st.markdown(
                                f"""
                                <div class="diagnosis-animal">
                                    Livestock Type: {html.escape(animal_name)}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )


                            metric1, metric2 = st.columns(
                                2
                            )


                            with metric1:

                                st.metric(
                                    "CONFIDENCE",
                                    f"{conf_pct:.2f}%"
                                )


                            with metric2:

                                st.metric(
                                    "RISK STATUS",
                                    risk_level
                                )


                        # =====================================
                        # HEALTH GUIDANCE
                        # =====================================

                        render_health_guidance(
                            animal_name=animal_name,
                            disease=disease,
                            confidence=conf,
                            risk_level=risk_level
                        )


# ============================================================
# AI ASSISTANT
# ============================================================

elif st.session_state.page == "Assistant":

    try:

        render_chatbot()

    except Exception as error:

        st.error(
            "⚠️ AI Assistant could not process your question."
        )

        st.error(
            f"Actual Error: {error}"
        )


# ============================================================
# GROUND WORK
# ============================================================

elif st.session_state.page == "Ground Work":

    render_ground_work(
        BASE_DIR
    )


# ============================================================
# DISEASES
# ============================================================

elif st.session_state.page == "Diseases":

    show_html(
        "diseases.html"
    )


# ============================================================
# ABOUT
# ============================================================

elif st.session_state.page == "About":

    show_html(
        "about.html"
    )


# ============================================================
# END
# ============================================================