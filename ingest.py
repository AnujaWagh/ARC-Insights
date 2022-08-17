import requests
import psycopg2

with requests.get("https://127.0.0.1:5000/very_large_request/10", stream=True) as r:

    conn = psycopg2.connect(dbname="arc_test",
                            user="postgres", password="1234")
    cur = conn.cursor()
    sql = "INSERT INTO user_details (id, firstname, lastname, email) VALUES (%s, %s, %s, %s)"

    buffer = ""
    for chunk in r.iter_content(chunk_size=1):
        if chunk.endswith(b'\n'):
            t = eval(buffer)
            print(t)
            cur.execute(sql, (t[0], t[1], t[2]))
            conn.commit()
            buffer = ""
        else:
            buffer += chunk.decode()