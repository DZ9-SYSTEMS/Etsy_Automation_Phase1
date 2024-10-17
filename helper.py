import sqlite3
from contextlib import closing
import requests
import streamlit as st

# Function to connect to the SQLite database
def get_db_connection():
    return sqlite3.connect('settings.db')

# Function to create necessary tables if they don't exist
def create_tables():
    with closing(get_db_connection()) as connection, closing(connection.cursor()) as cursor:
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_key TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS channel_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT NOT NULL,
                user_token TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_url TEXT NOT NULL,
                image_path TEXT NOT NULL
            );
        ''')

        connection.commit()

# Function to insert or update an API key in the database
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

# Function to insert channel information into the database
def insert_channel_user_credentials(channel_id, user_token):
    with closing(get_db_connection()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute('''
            INSERT INTO channel_info (channel_id, user_token) VALUES (?, ?)
        ''', (channel_id, user_token))
        connection.commit()

# Function to retrieve channel information from the database
def get_channel_user_credentials():
    with closing(get_db_connection()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute('SELECT channel_id, user_token FROM channel_info')
        result = cursor.fetchone()
        return result if result else None

# Function to delete all data from all tables
def delete_all_data():
    with closing(get_db_connection()) as connection, closing(connection.cursor()) as cursor:
        try:
            cursor.executescript('''
                DELETE FROM api_keys;
                DELETE FROM channel_info;
            ''')
            connection.commit()
            print("All data deleted successfully.")
            return "All data deleted successfully."
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            return f"Error deleting data: {e}"


# Function to set image DPI to a custom level
def set_image_dpi(image, dpi):
    img_format = image.format if image.format else 'JPEG'
    img_with_dpi = image.copy()
    output_filename = f"output_image_{dpi}dpi.jpg"
    img_with_dpi.save(output_filename, format=img_format, dpi=(dpi, dpi))
    return output_filename



def download_image(image_url, save_path):
    """
    Downloads an image from the given URL and saves it to the specified path.

    Parameters:
    - image_url: str, the URL of the image to download.
    - save_path: str, the path (including filename) where the image will be saved.

    Returns:
    - bool: True if the image was downloaded and saved successfully, False otherwise.
    """
    try:
        # Send a GET request to fetch the image
        response = requests.get(image_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the image to the specified path
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image successfully downloaded and saved as '{save_path}'")
            return True
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# Function to display 3-step instructions
def display_instructions():
    st.header("Set Up Your Discord Channel ID and User Token")

    st.write("To start generating images, please follow the steps below:")

    st.markdown(
    """
    ### Prerequisites
    - You need a [Discord account](https://discord.com/register).
    - You must purchase a Midjourney subscription for your Discord account on the [MidJourney website](https://www.midjourney.com/). The $10 Basic plan will do.
    """
)


    # Step 1
    st.subheader("Step 1: Get Your Discord Channel ID")
    st.markdown(
    """
    Navigate to your [Midjourney Discord server](https://discord.com/channels/@me),&nbsp; click the 'newbies' channel, and copy the Channel ID from the URL.
    """)
    st.image("assets/midjourney_channel_id.png", caption="Go to your Discord server settings and find the Channel ID.")


    # Step 2
    st.subheader("Step 2: Get Your Discord User Token")
    st.markdown(
        """
        To get your User Token, open your browser's developer tools. This will open a window to the bottom or side of your browser.
        """)
    st.image("assets/open_inspect_tools.png", caption="Find your Discord User Token.")

    st.markdown(
        """
        Next, click the the 'Network' tab. Refresh the page and click the 'fetch/XHR' filter. Under the 'Name' column, click '@me'. Under the 'headers' tab scroll down and find 'Authorization:' copy the string to the righ of it. This is your midjourney_user_token.
        """)
    st.image("assets/midjourney_user_token.png", caption="Enter the credentials in the sidebar.")

    # Step 3
    st.subheader("Step 3: Enter Your Credentials")
    st.write("Once you have both the Channel ID and User Token, enter them in the input fields on the left sidebar and click 'Save Credentials'.")
    st.image("assets/credentials.png", caption="Enter the credentials in the sidebar.")

