from flask import Flask, request, render_template
import psycopg2
import csv
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/insert_details", methods=["GET"])
def insert_details():

    try:
        args = request.args
        # id = args.get('id')
        firstname = args.get('firstname')
        lastname = args.get('lastname')
        email = args.get('email')

        conn = psycopg2.connect(dbname="postgres",
                                host='test-db-postgres.c8cxqgsirbs0.eu-west-2.rds.amazonaws.com',
                                user="postgres", password="mystrongpassword")
        cur = conn.cursor()
        sql = "INSERT INTO public.user_details(firstname, lastname, email)	VALUES (%s, %s, %s);"
        cur.execute(sql, (firstname, lastname, email))
        conn.commit()   

        query = "SELECT * FROM public.user_details order by id;"
        cur.execute(query)
  
        with open('result.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for row in cur.fetchall():
                writer.writerow(row)
        cur.close()
        conn.close()

        return "Record inserted successfully!"
    except Exception as e:
        return(str(e))

@app.route("/get_user_details", methods=["GET"])
def get_user_details():
    data = []
    try:
        conn = psycopg2.connect(dbname="postgres",
                                host='test-db-postgres.c8cxqgsirbs0.eu-west-2.rds.amazonaws.com',
                                user="postgres", password="mystrongpassword")
        cur = conn.cursor()
        query = "SELECT * FROM public.user_details order by id;"
        cur.execute(query)
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        conn.close()
        print(data)
        return render_template("index.html", headings=["id", "firstname", "lastname", "email"], data=data)
    except Exception as e:
        return(str(e))

if __name__ == "__main__":
    port = 5000
    app.run(host='0.0.0.0', port=port)