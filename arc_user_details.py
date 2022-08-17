from flask import Flask, request
import psycopg2
APP = Flask(__name__)

@APP.route("/get_user_details", methods=["GET"])
def get_user_details():

    try:
        args = request.args
        id = args.get('id')
        firstname = args.get('firstname')
        lastname = args.get('lastname')
        email = args.get('email')

        conn = psycopg2.connect(dbname="arc_test",
                                host='localhost',
                                user="postgres", password="1234")
        cur = conn.cursor()
        sql = "INSERT INTO public.user_details(id, firstname, lastname, email)	VALUES (%s, %s, %s, %s);"
        cur.execute(sql, (id, firstname, lastname, email))
        conn.commit()
        conn.close()
        return "Record inserted successfully!"
    except Exception as e:
        return(str(e))

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    APP.run(host=host, port=port)
    APP.run(debug=True)