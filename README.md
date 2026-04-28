# Instrument Repair DB
Full stack relational database system to track instrument repair tickets and job progress. Built with Django and Bootstrap 5.

## To Run
1. Download and extract the zip
2. Open a terminal in the extracted folder and run:
    ```
    pip3 install -r requirements.txt
    python3 manage.py migrate
    python3 manage.py runserver
    ```
3. Visit **http://127.0.0.1:8000** in your browser

> To start with sample data, include `db.sqlite3` from the zip (already populated). If it is not included, the database will start empty.
