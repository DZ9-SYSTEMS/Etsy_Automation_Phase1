import sqlite3
from contextlib import closing
import openai
from PIL import Image
from io import BytesIO
import requests
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = openai.Client(api_key=os.getenv('OPENAI_API_KEY'))

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')  # Use the correct initialization for the OpenAI client

# Function to connect to the SQLite database
def get_db_connection():
    connection = sqlite3.connect('settings.db')  # Consider using a relative path if needed
    return connection

# Function to create a table for API keys if it doesn't exist
def create_api_key_table():
    with closing(get_db_connection()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_key TEXT NOT NULL
            )
        ''')
        connection.commit()

# Function to insert an API key into the database (overwrites existing key)
def insert_api_key(api_key):
    with closing(get_db_connection()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute('''
            INSERT OR REPLACE INTO api_keys (id, api_key) VALUES (1, ?)
        ''', (api_key,))
        connection.commit()

# Function to retrieve the API key from the database
def get_api_key():
    with closing(get_db_connection()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute('SELECT api_key FROM api_keys WHERE id = 1')
        result = cursor.fetchone()
        return result[0] if result else None

# Function to create a table for images if it doesn't exist
def create_images_table():
    with closing(get_db_connection()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT NOT NULL,
                prompt TEXT NOT NULL
            )
        ''')
        connection.commit()

# Function to insert an image into the database
def insert_image(image_path, prompt):
    with closing(get_db_connection()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute('''
            INSERT INTO images (image_path, prompt) VALUES (?, ?)
        ''', (image_path, prompt))
        connection.commit()

# Function to retrieve images from the database
def delete_all_data():
    with closing(get_db_connection()) as connection, closing(connection.cursor()) as cursor:
        try:
            # Check if the api_keys table exists before attempting to delete
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_keys'")
            if cursor.fetchone():
                cursor.execute('DELETE FROM api_keys')
            else:
                print("Table 'api_keys' does not exist.")

            # Check if the images table exists before attempting to delete
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='images'")
            if cursor.fetchone():
                cursor.execute('DELETE FROM images')
            else:
                print("Table 'images' does not exist.")

            # Commit the changes
            connection.commit()
            print("All data deleted successfully.")
            return "All data deleted successfully."
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            return f"Error deleting data: {e}"


# Function to generate images using OpenAI's DALL-E 3
def generate_images(prompt, num_images, model, size='1024x1024'):
    try:
        response = client.images.generate(
            model=model,
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
