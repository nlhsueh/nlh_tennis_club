import requests
session = requests.Session()
# We don't know the password, but we can simulate a logged-in request by finding the session id.
import sqlite3
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute("SELECT session_key FROM django_session LIMIT 1")
row = c.fetchone()
if row:
    session.cookies.set('sessionid', row[0])
    r = session.get('http://127.0.0.1:8000/courts/bookings/')
    print(r.text)
else:
    print("No session found")
