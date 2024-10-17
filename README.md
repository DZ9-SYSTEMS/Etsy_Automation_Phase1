# LangGraphAgents

### Create a virtual environment:
python3 -m venv venv

### Activate the virtual environment:
source venv/bin/activate

### Installing Dependencies
pip install -r requirements.txt

### execute program
streamlit run app.py


### SQ Lite Commands

1. Open a Database:

sqlite3 settings.db

2. Create a New Database:

sqlite3 new_database.db

3. List All Databases:

.databases

4. Show All Tables:

.tables

5. Select Data from a Table:
SELECT * FROM channel_info;