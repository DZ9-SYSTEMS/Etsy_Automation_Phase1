import openai
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = openai.Client(api_key=os.getenv('OPENAI_API_KEY'))

# Function to generate images using OpenAI's DALL-E 3
def generate_images(prompt, num_images, size='1024x1024'):
    try:
        response = client.images.generate(
            model='dall-e-3',
            prompt=prompt,
            size=size,
            quality='hd',
            n=num_images,
            style='vivid'
        )

        images = []
        for img_data in response.data:
            image_url = img_data.url
            image_response = requests.get(image_url)
            images.append(Image.open(BytesIO(image_response.content)))

        return images
    except Exception as e:
        print(f"Error generating images: {e}")
        return []

# Function to set image DPI to a custom level
def set_image_dpi(image, dpi):
    img_format = image.format if image.format else 'JPEG'
    img_with_dpi = image.copy()
    output_filename = f"output_image_{dpi}dpi.jpg"
    img_with_dpi.save(output_filename, format=img_format, dpi=(dpi, dpi))
    return output_filename
