import streamlit as st
from helper import (
    insert_api_key,
    get_api_key,
    create_tables,
    delete_all_data,
    insert_channel_user_credentials,
    get_channel_user_credentials,
    display_instructions,
    download_image
)
from midjourney_sdk_py import Midjourney
from dotenv import load_dotenv
import os

# Load environment variables from .env file (optional)
load_dotenv()

# Initialize the database and tables
create_tables()  # This creates both the API key and channel user credential tables

# Set the page configuration with a custom tab title and favicon
st.set_page_config(page_title="MidJourney Image Generator", page_icon="assets/midjourney.png")

# Sidebar for API Key and User Token Input
def sidebar():
    st.sidebar.image("assets/midjourney.png", width=250)
    st.sidebar.subheader("API Key & MidJourney Setup")

    # Check if credentials already exist
    credentials = get_channel_user_credentials()

    if credentials:
        # Load existing credentials into session state
        discord_channel_id, discord_user_token = credentials
        st.session_state.discord_channel_id = discord_channel_id
        st.session_state.discord_user_token = discord_user_token
        st.sidebar.success("Credentials loaded successfully!")
    else:
        # Input fields for Discord Channel ID and User Token
        discord_channel_id = st.sidebar.text_input("Enter Discord Channel ID", value="")
        discord_user_token = st.sidebar.text_input("Enter Discord User Token", value="", type="password")

        # Check if the required inputs are provided
        if st.sidebar.button("Save Credentials"):
            if discord_channel_id and discord_user_token:
                # Save to session state and database
                insert_channel_user_credentials(discord_channel_id, discord_user_token)
                st.session_state.discord_channel_id = discord_channel_id
                st.session_state.discord_user_token = discord_user_token
                st.sidebar.success("Credentials saved successfully!")
            else:
                st.sidebar.error("Please enter both Channel ID and User Token")

    # Delete all data button
    if st.sidebar.button("Delete All Data"):
        delete_all_data()  # Call the function to delete all data
        st.sidebar.success("All data deleted successfully!")



# Main application page
def main_page():
    st.title("MidJourney Image Generator")

    # Check if API key and credentials are present in the session state
    discord_channel_id = st.session_state.get('discord_channel_id', None)
    discord_user_token = st.session_state.get('discord_user_token', None)

    # If credentials are not set, show instructions
    if not discord_channel_id or not discord_user_token:
        st.error("Please enter your Discord Channel ID and User Token in the sidebar before using the app.")
        display_instructions()
        return

    # Initialize the Midjourney SDK with user credentials
    midjourney = Midjourney(discord_channel_id, discord_user_token)

    # User inputs for generating images
    prompt = st.text_input("Enter a design prompt for MidJourney")
    num_images = st.number_input("Number of images to generate", min_value=1, max_value=10, value=1, step=1)

    if st.button("Generate Design"):
        if prompt:
            options = {
                "ar": "3:2",  # Aspect ratio
                "v": "6.0",   # Version
            }

            # Generate images from MidJourney
            for idx in range(num_images):
                message = midjourney.generate(prompt, options)
                image_url = message['upscaled_photo_url']

                # Define a local save path for the image
                save_path = f"generated_image_{idx + 1}.png"

                # Download the image using the helper function
                if download_image(image_url, save_path):
                    # Display the downloaded image in the app
                    st.image(save_path, caption=f"Generated Image {idx + 1}")

                    # Allow user to download the image
                    with open(save_path, 'rb') as img_file:
                        st.download_button(
                            f"Download Image {idx + 1}",
                            data=img_file,
                            file_name=f"design_{idx + 1}.png"
                        )
                else:
                    st.error(f"Failed to download Image {idx + 1}")
        else:
            st.warning("Please enter a prompt")

# Main Streamlit Application Logic
def main():
    sidebar()  # Display the sidebar for API key and credentials input
    main_page()  # Display the main page for generating images

if __name__ == "__main__":
    main()
