import streamlit as st
from helper import generate_images, set_image_dpi, insert_api_key, get_api_key, create_api_key_table, delete_all_data
import os

# Initialize the database and API key table
create_api_key_table()

# Set the page configuration with a custom tab title and favicon
st.set_page_config(page_title="DALL-E Design & DPI Converter", page_icon="assets/etsy.png")

# Sidebar for API Key Input
def sidebar():
    st.sidebar.image("assets/dall-e.png", width=250)
    st.sidebar.subheader("API Key Setup")

    # Retrieve existing API key from the database or session state
    if 'api_key' not in st.session_state:
        st.session_state.api_key = get_api_key()

    # Input field for the API key
    api_key_input = st.sidebar.text_input("Enter your OpenAI API Key", value=st.session_state.api_key, type="password")

    if st.sidebar.button("Save API Key"):
        if api_key_input:
            insert_api_key(api_key_input)
            st.session_state.api_key = api_key_input  # Update session state
            st.sidebar.success("API Key saved successfully!")
        else:
            st.sidebar.error("Please enter a valid API key")

    # Delete all data button
    if st.sidebar.button("Delete All Data"):
        delete_all_data()  # Call the function to delete all data
        result_message = delete_all_data()  # Call the function to delete all data
        st.sidebar.success(result_message)

# Main application page
def main_page():
    st.title("DALL-E Design Generator and DPI Converter")

    # Check if API key is present in the session state
    saved_api_key = st.session_state.get('api_key', None)

    if not saved_api_key:
        st.success("Please enter your API key in the sidebar before using the app. You can get an API key from OpenAI here: https://platform.openai.com/api-keys")

    # User inputs for generating images
    prompt = st.text_input("Enter a design prompt for DALL-E")
    num_images = st.number_input("Number of images to generate", min_value=1, max_value=10, value=1, step=1)
    dpi_level = st.number_input("Set DPI level", min_value=72, max_value=600, value=300, step=10)

    # Select box for DALL-E model selection
    dall_e_models = ["dall-e-1", "dall-e-2", "dall-e-3"]  # Replace with actual model names
    selected_model = st.selectbox("Select DALL-E Model", dall_e_models)

    if st.button("Generate Design"):
        if prompt:
            # Generate images from DALL-E
            images = generate_images(prompt, num_images, model=selected_model)

            if images:
                st.write(f"Generated {len(images)} images.")

                for idx, image in enumerate(images):
                    st.image(image, caption=f"Generated Design {idx + 1}")

                    # Convert image to custom DPI
                    formatted_image_path = set_image_dpi(image, dpi_level)
                    st.success(f"Image {idx + 1} formatted to {dpi_level} DPI!")

                    # Allow user to download the image
                    st.download_button(
                        f"Download Image {idx + 1} at {dpi_level} DPI",
                        data=open(formatted_image_path, 'rb').read(),
                        file_name=f"design_{idx + 1}_{dpi_level}dpi.jpg"
                    )
            else:
                st.error("Failed to generate images")
        else:
            st.warning("Please enter a prompt")

# Main Streamlit Application Logic
def main():
    sidebar()  # Display the sidebar for API key input
    main_page()  # Display the main page for generating images

if __name__ == "__main__":
    main()
