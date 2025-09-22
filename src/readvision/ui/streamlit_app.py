#!/usr/bin/env python3
"""
Streamlit Web UI for ReadVision OCR PDF Processor
"""

import streamlit as st
import tempfile
import os
from pathlib import Path
import time
from io import BytesIO

try:
    from readvision.core.processor import PDFOCRProcessor
except ImportError:  # pragma: no cover - fallback for direct script execution
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from readvision.core.processor import PDFOCRProcessor


def setup_page():
    """Configure the Streamlit page."""
    st.set_page_config(
        page_title="ReadVision OCR",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📖 ReadVision OCR PDF Processor")
    st.markdown("Convert PDF documents to text and Word files using Google Cloud Vision API")


def sidebar_configuration():
    """Create the sidebar with configuration options."""
    st.sidebar.header("⚙️ Configuration")

    # Text direction
    text_direction = st.sidebar.selectbox(
        "Text Direction",
        options=["rtl", "ltr"],
        index=0,  # Default to RTL (Arabic)
        help="Choose the text direction for the output document"
    )

    # Language hint
    language_hint = st.sidebar.selectbox(
        "Language Hint",
        options=["ar", "en", "fr", "es", "de", "it", "pt", "ru", "zh", "ja", "th"],
        index=0,  # Default to Arabic
        help="Language hint to improve OCR accuracy"
    )

    # Encoding
    encoding = st.sidebar.selectbox(
        "Text Encoding",
        options=["utf-8", "utf-16", "ascii", "latin1"],
        index=0,  # Default to UTF-8
        help="Character encoding for the output text file"
    )

    # Debug mode
    debug_mode = st.sidebar.checkbox(
        "Debug Mode",
        value=False,
        help="Enable debug output for troubleshooting"
    )

    # Custom bucket
    use_custom_bucket = st.sidebar.checkbox(
        "Use Custom GCS Bucket",
        value=False,
        help="Use a custom Google Cloud Storage bucket for large files"
    )

    custom_bucket = None
    if use_custom_bucket:
        custom_bucket = st.sidebar.text_input(
            "Bucket Name",
            placeholder="my-custom-bucket",
            help="Enter your Google Cloud Storage bucket name"
        )

    return {
        "text_direction": text_direction,
        "language_hint": language_hint,
        "encoding": encoding,
        "debug": debug_mode,
        "bucket_name": custom_bucket if use_custom_bucket else None
    }


def credentials_upload():
    """Handle Google Cloud credentials upload."""
    st.subheader("🔑 Google Cloud Credentials")

    # Check if credentials file already exists
    if os.path.exists("gcp.json"):
        st.success("✅ Credentials file found: `gcp.json`")
        return "gcp.json"

    # Upload credentials
    uploaded_creds = st.file_uploader(
        "Upload your Google Cloud credentials JSON file",
        type=["json"],
        help="Upload your service account key file from Google Cloud Console"
    )

    if uploaded_creds is not None:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".json", delete=False) as tmp_file:
            tmp_file.write(uploaded_creds.getvalue())
            return tmp_file.name

    return None


def pdf_upload():
    """Handle PDF file upload."""
    st.subheader("📄 Upload PDF Document")

    uploaded_pdf = st.file_uploader(
        "Choose a PDF file to process",
        type=["pdf"],
        help="Upload the PDF document you want to convert to text"
    )

    if uploaded_pdf is not None:
        # Display file info
        st.info(f"📁 File: {uploaded_pdf.name} ({uploaded_pdf.size:,} bytes)")

        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as tmp_file:
            tmp_file.write(uploaded_pdf.getvalue())
            return tmp_file.name, uploaded_pdf.name

    return None, None


def process_pdf(pdf_path, original_filename, credentials_path, config):
    """Process the PDF with progress tracking."""
    try:
        # Create output filenames
        base_name = Path(original_filename).stem
        output_txt = f"{base_name}_output.txt"
        output_docx = f"{base_name}_output.docx"

        # Initialize processor
        with st.spinner("🔧 Initializing OCR processor..."):
            processor = PDFOCRProcessor(
                credentials_path=credentials_path,
                bucket_name=config["bucket_name"]
            )

        # Get page count for progress tracking
        with st.spinner("📊 Analyzing PDF..."):
            page_count = processor.get_pdf_page_count(pdf_path)
            st.info(f"📄 Document has {page_count} pages")

        # Create progress bars
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Process the PDF
        status_text.text("🔄 Processing PDF with OCR...")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_output_path = os.path.join(temp_dir, output_txt)

            # Process with configuration
            processor.process_pdf(
                pdf_path=pdf_path,
                output_path=temp_output_path,
                text_direction=config["text_direction"],
                encoding=config["encoding"],
                language_hint=config["language_hint"],
                debug=config["debug"]
            )

            progress_bar.progress(1.0)
            status_text.text("✅ Processing complete!")

            # Read the generated files
            with open(temp_output_path, 'r', encoding=config["encoding"]) as f:
                text_content = f.read()

            # Read the Word document
            word_path = temp_output_path.replace('.txt', '.docx')
            with open(word_path, 'rb') as f:
                docx_content = f.read()

            return text_content, docx_content, output_txt, output_docx

    except Exception as e:
        st.error(f"❌ Error processing PDF: {str(e)}")
        return None, None, None, None


def display_results(text_content, docx_content, txt_filename, docx_filename, config):
    """Display processing results and download options."""
    st.subheader("✅ Processing Complete!")

    # Create two columns for downloads
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📄 Download Text File",
            data=text_content.encode(config["encoding"]),
            file_name=txt_filename,
            mime="text/plain",
            help="Download the extracted text as a .txt file"
        )

    with col2:
        st.download_button(
            label="📝 Download Word Document",
            data=docx_content,
            file_name=docx_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            help="Download the formatted Word document"
        )

    # Show text preview
    st.subheader("👀 Text Preview")

    # Character count
    char_count = len(text_content)
    word_count = len(text_content.split())
    st.metric("Statistics", f"{char_count:,} characters, {word_count:,} words")

    # Text preview with option to show full text
    show_full_text = st.checkbox("Show full text", value=False)

    if show_full_text:
        st.text_area(
            "Extracted Text",
            value=text_content,
            height=400,
            help="Full extracted text from the PDF"
        )
    else:
        preview_text = text_content[:1000] + "..." if len(text_content) > 1000 else text_content
        st.text_area(
            "Text Preview (first 1000 characters)",
            value=preview_text,
            height=200,
            help="Preview of the extracted text"
        )


def main():
    """Main Streamlit application."""
    setup_page()

    # Get configuration from sidebar
    config = sidebar_configuration()

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        # Step 1: Upload credentials
        credentials_path = credentials_upload()

        if credentials_path:
            # Step 2: Upload PDF
            pdf_path, original_filename = pdf_upload()

            if pdf_path and original_filename:
                # Step 3: Process button
                if st.button("🚀 Start OCR Processing", type="primary"):
                    text_content, docx_content, txt_filename, docx_filename = process_pdf(
                        pdf_path, original_filename, credentials_path, config
                    )

                    if text_content and docx_content:
                        # Step 4: Display results
                        display_results(
                            text_content, docx_content,
                            txt_filename, docx_filename, config
                        )

                        # Clean up temporary files
                        try:
                            os.unlink(pdf_path)
                            if credentials_path != "gcp.json":
                                os.unlink(credentials_path)
                        except:
                            pass  # Ignore cleanup errors
        else:
            st.warning("👆 Please upload your Google Cloud credentials file to continue")

    with col2:
        # Information panel
        st.subheader("ℹ️ How to Use")
        st.markdown("""
        1. **Upload Credentials**: Upload your Google Cloud service account JSON file
        2. **Upload PDF**: Choose the PDF document to process
        3. **Configure Settings**: Adjust language, direction, and other options in the sidebar
        4. **Start Processing**: Click the button to begin OCR
        5. **Download Results**: Get your text and Word files
        """)

        st.subheader("🌟 Features")
        st.markdown("""
        - ✅ Page-by-page mapping
        - ✅ Arabic/RTL support
        - ✅ Multiple output formats
        - ✅ Progress tracking
        - ✅ Batch processing for large files
        - ✅ Text cleaning & formatting
        """)

        st.subheader("📋 Supported Languages")
        languages = {
            "ar": "Arabic", "en": "English", "fr": "French",
            "es": "Spanish", "de": "German", "it": "Italian",
            "pt": "Portuguese", "ru": "Russian", "zh": "Chinese", "ja": "Japanese"
        }
        for code, name in languages.items():
            st.markdown(f"- **{code}**: {name}")


if __name__ == "__main__":
    main()
