import os
import streamlit as st
import google.generativeai as genai

def main():
    # Set your Gemini API key directly here
    api_key = 'AIzaSyARwKZ02kUD7qmzrPA-GpWEI2PV48rDS7o'
    genai.configure(api_key=api_key)

    # Set up the Streamlit interface
    st.title("Design Software Recommendation")

    # User input for design requirement
    user_input = st.text_area(
        "Please describe your design requirement (e.g., 'I need to create a poster')",
        height=200
    )

    # Dropdown to select software type
    software_type = st.selectbox(
        "What type of software are you looking for?",
        ("High-End Software", "Low-End Software")
    )

    # Button to generate software recommendation
    if st.button("Suggest Software"):
        if user_input.strip():
            # Create a prompt for generating the software recommendation based on the type
            if software_type == "High-End Software":
                prompt = f"""
                Based on the following design requirement, please suggest the best high-end design software (e.g., Adobe Photoshop, Adobe Illustrator):

                "{user_input}"

                Provide a brief explanation of why this software is suitable for the task.
                """
            else:
                prompt = f"""
                Based on the following design requirement, please suggest the best low-end or mobile editing tool (e.g., Canva, Adobe Spark):

                "{user_input}"

                Provide a brief explanation of why this software is suitable for the task.
                """

            try:
                # Use the Gemini generative model to generate the recommendation
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                recommendation = response.text

                # Store the generated recommendation in the session state to keep it persistent
                st.session_state.generated_recommendation = recommendation
                st.session_state.copy_status = "Copy Recommendation to Clipboard"  # Reset the copy button text

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.warning("We couldn't generate the recommendation. Please try again later.")
        else:
            st.warning("Please provide a description of your design requirement.")

    # Check if the generated recommendation is in session state
    if 'generated_recommendation' in st.session_state:
        st.subheader("Recommended Design Software:")
        recommendation_text_area = st.text_area("Generated Recommendation:", st.session_state.generated_recommendation, height=400, key="recommendation_content")

        # Button to copy recommendation to clipboard
        copy_button = st.button(st.session_state.get('copy_status', "Copy Recommendation to Clipboard"), key="copy_button")

        if copy_button:
            # JavaScript code to copy the text and change button text
            st.write(f"""
                <script>
                function copyToClipboard() {{
                    var recommendationContent = document.querySelector('#recommendation_content');
                    var range = document.createRange();
                    range.selectNode(recommendationContent);
                    window.getSelection().removeAllRanges();  // Clear current selection
                    window.getSelection().addRange(range);  // Select the content
                    document.execCommand('copy');  // Copy the selected content
                    window.getSelection().removeAllRanges();  // Clear selection
                    document.getElementById('copy_button').innerText = 'COPIED';
                }}
                copyToClipboard();
                </script>
                """, unsafe_allow_html=True)
            st.session_state.copy_status = "COPIED"  # Update the button text to "COPIED"

if __name__ == "__main__":
    main()
