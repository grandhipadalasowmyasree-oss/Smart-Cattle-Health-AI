# ============================================================
# ground_work_page.py
# SMART CATTLE HEALTH AI - GROUND WORK
# ============================================================

from pathlib import Path
import webbrowser

import streamlit as st
from PIL import Image


# ============================================================
# OPEN IMAGE
# ============================================================

def open_image_large(image_path):

    try:
        webbrowser.open(
            image_path.resolve().as_uri()
        )
    except Exception as error:
        st.error(
            f"Could not open image: {error}"
        )


# ============================================================
# MAIN GROUND WORK PAGE
# ============================================================

def render_ground_work(BASE_DIR):

    st.title("📸 Ground Work")

    st.write(
        "Our team field work and project development journey."
    )

    st.markdown("---")

    # ========================================================
    # PROJECT DESCRIPTION
    # ========================================================

    st.subheader("🐄 Project Ground Work")

    st.write(
        """
        Our team worked on cattle image collection,
        dataset preparation, disease annotation,
        YOLO model training and testing.
        """
    )

    st.markdown("---")

    # ========================================================
    # PROJECT GALLERY
    # ========================================================

    st.subheader("📷 Project Gallery")

    st.write(
        "Our team and project work images."
    )

    # ========================================================
    # GROUND WORK FOLDER
    # ========================================================

    ground_work_dir = (
        Path(BASE_DIR) / "ground_work"
    )

    # ========================================================
    # CHECK FOLDER
    # ========================================================

    if not ground_work_dir.exists():

        st.error(
            "❌ ground_work folder not found."
        )

        st.code(
            str(ground_work_dir)
        )

        return

    # ========================================================
    # IMAGE TYPES
    # ========================================================

    image_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".jfif",
        ".bmp",
    }

    # ========================================================
    # FIND IMAGES
    # ========================================================

    gallery_images = []

    for image_path in ground_work_dir.rglob("*"):

        if not image_path.is_file():
            continue

        if image_path.suffix.lower() in image_extensions:

            gallery_images.append(
                image_path
            )

    gallery_images = sorted(
        gallery_images,
        key=lambda x: x.name.lower()
    )

    # ========================================================
    # IMAGE COUNT
    # ========================================================

    st.caption(
        f"📁 Found {len(gallery_images)} image(s)"
    )

    # ========================================================
    # NO IMAGES
    # ========================================================

    if not gallery_images:

        st.warning(
            "⚠️ No supported images were found."
        )

        st.code(
            str(ground_work_dir)
        )

        return

    # ========================================================
    # DESCRIPTIONS
    # ========================================================

    descriptions = [

        (
            "🐄 Cattle Image Collection",
            "Cattle images were collected as part of the dataset preparation process."
        ),

        (
            "📸 Field Observation",
            "The cattle images help us study visible health conditions and disease symptoms."
        ),

        (
            "🔍 Disease Identification",
            "Images were examined to identify important visual symptoms of cattle diseases."
        ),

        (
            "🎯 Disease Annotation",
            "Disease-affected regions were marked using bounding boxes for object detection."
        ),

        (
            "🤖 YOLO Model Training",
            "The annotated images were used to train our YOLO-based cattle disease detection model."
        ),

        (
            "🧪 Model Testing",
            "The trained AI model was tested using cattle images to check its detection performance."
        ),

        (
            "⚠️ Early Disease Detection",
            "The system helps identify possible disease-affected areas at an early stage."
        ),

        (
            "👨‍🌾 Farmer Support",
            "The final system is designed to provide useful health information and guidance to farmers."
        ),

    ]

    # ========================================================
    # GALLERY
    # ========================================================

    for start in range(
        0,
        len(gallery_images),
        3
    ):

        row_images = gallery_images[
            start:start + 3
        ]

        columns = st.columns(3)

        for index, (
            column,
            image_path
        ) in enumerate(
            zip(
                columns,
                row_images
            )
        ):

            with column:

                try:

                    # ========================================
                    # LOAD IMAGE
                    # ========================================

                    image = Image.open(
                        image_path
                    ).convert("RGB")

                    # ========================================
                    # SHOW IMAGE
                    # ========================================

                    st.image(
                        image,
                        use_column_width=True
                    )

                    # ========================================
                    # OPEN THIS IMAGE
                    # ========================================

                    image_number = (
                        start + index
                    )

                    if st.button(
                        "🔍 Open Image",
                        key=f"open_image_{image_number}",
                        use_container_width=True
                    ):

                        open_image_large(
                            image_path
                        )

                    # ========================================
                    # DESCRIPTION
                    # ========================================

                    if (
                        image_number
                        <
                        len(descriptions)
                    ):

                        title, description = (
                            descriptions[
                                image_number
                            ]
                        )

                        st.markdown(
                            f"**{title}**"
                        )

                        st.caption(
                            description
                        )

                    else:

                        st.markdown(
                            f"**🐄 Project Work "
                            f"{image_number + 1}**"
                        )

                        st.caption(
                            "This image represents our Smart Cattle Health AI project work."
                        )

                except Exception as error:

                    st.error(
                        f"Could not load {image_path.name}"
                    )

                    st.caption(
                        str(error)
                    )

    # ========================================================
    # FINAL SECTION
    # ========================================================

    st.markdown("---")

    st.subheader(
        "🌱 From Field Work to AI"
    )

    st.write(
        """
        Our project combines real-world cattle image collection,
        disease annotation, computer vision and YOLO-based AI
        detection to support early cattle disease identification
        and better farmer decision-making.
        """
    )