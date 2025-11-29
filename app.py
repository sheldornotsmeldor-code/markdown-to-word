import streamlit as st
import pypandoc
import os
import tempfile

# Page configuration
st.set_page_config(page_title="Sheldor's Converter", page_icon="📝", layout="wide")

st.title("📝 Sheldor's Markdown to Word Converter")
st.markdown("Convert Markdown with LaTeX math ($E=mc^2$) into editable Word documents.")

# Split layout: Left for input, Right for instructions/preview
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input")
    # Default text to show the user how it works
    default_text = """# Sample Document
Here is some text.

## Math Equation
This is a quadratic formula:
$$
x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}
$$

## Inline Math
The value of $\\pi$ is approximately 3.14159.
"""
    markdown_input = st.text_area("Paste your Markdown/LaTeX here:", value=default_text, height=400)

with col2:
    st.subheader("Preview (Web Render)")
    # This shows the web preview (Math might look slightly different here than in Word, that's normal)
    st.markdown(markdown_input)

# Conversion Logic
st.markdown("---")
if st.button("Convert to Word (.docx)", type="primary"):
    if markdown_input:
        try:
            # Create a temporary file to save the docx
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
                output_path = tmp_file.name

            # Convert Markdown string to Docx file using Pandoc
            # "markdown" format in Pandoc handles standard MD + LaTeX math
            pypandoc.convert_text(
                markdown_input,
                'docx',
                format='markdown',
                outputfile=output_path,
                extra_args=['--standalone']
            )

            # Read the file back so the user can download it
            with open(output_path, "rb") as file:
                btn = st.download_button(
                    label="📥 Download Word Document",
                    data=file,
                    file_name="converted_document.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            
            st.success("Conversion successful! Click the button above to download.")
            
        except Exception as e:
            st.error(f"An error occurred during conversion: {e}")
            st.info("Note: If you are running this locally, make sure Pandoc is installed.")
    else:
        st.warning("Please enter some text first.")
