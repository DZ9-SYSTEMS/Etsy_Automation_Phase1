import streamlit as st
from helper import generate_images, set_image_dpi

# Set the page configuration (custom tab title)
st.set_page_config(page_title="DALL-E Design & DPI Converter", page_icon="assets/etsy.png")
# Streamlit App
def main():
    st.title("DALL-E Design Generator and DPI Converter")

    # User inputs for generating images
    prompt = st.text_input("Enter a design prompt for DALL-E")
    num_images = st.number_input("Number of images to generate", min_value=1, max_value=10, value=1, step=1)
    dpi_level = st.number_input("Set DPI level", min_value=72, max_value=600, value=300, step=10)

    if st.button("Generate Design"):
        if prompt:
            # Generate images from DALL-E 3
            images = generate_images(prompt, num_images)

            if images:
                st.write(f"Generated {len(images)} images.")

                for idx, image in enumerate(images):
                    st.image(image, caption=f"Generated Design {idx + 1}")

                    # Convert image to custom DPI
                    formatted_image_path = set_image_dpi(image, dpi_level)
                    st.success(f"Image {idx + 1} formatted to {dpi_level} DPI!")

                    # Allow user to download the image
                    st.download_button(f"Download Image {idx + 1} at {dpi_level} DPI",
                                       open(formatted_image_path, 'rb'),
                                       file_name=f"design_{idx + 1}_{dpi_level}dpi.jpg")
            else:
                st.error("Failed to generate images")
        else:
            st.warning("Please enter a prompt")

if __name__ == "__main__":
    main()
