from flask import Flask, request, render_template
import psycopg2
import os
import csv
import xlwt
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

@app.route("/getPlotCSV", methods=["GET"])
def getPlotCSV():
    data = []
    output_file_1= "test.csv"
    try:
        conn = psycopg2.connect(dbname="postgres",
                                host='test-db-postgres.c8cxqgsirbs0.eu-west-2.rds.amazonaws.com',
                                user="postgres", password="mystrongpassword")
        cur = conn.cursor()
    except Exception as e:
        return(str(e))

    try:
        cur.execute('''SELECT * FROM public.user_details order by id ;''')
    except:
        print("Enable to execute query")

    rows=cur.fetchall()

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(os.path.split(output_file_1)[1])

    worksheet.set_panes_frozen(True)
    worksheet.set_horz_split_pos(0)
    worksheet.set_remove_splits(True)

    for colidx,heading in enumerate(cur.description):
        worksheet.write(0,colidx,heading[0]) # first element of each tuple

    # Write rows
    for rowidx, row in enumerate(rows):
        for colindex, col in enumerate(row):
            worksheet.write(rowidx+1, colindex, col)

    # All done
    workbook.save(output_file_1)

    print("Download process done!!")
    conn.commit()
    conn.close()

    return "File downloaded successfully!"

if __name__ == "__main__":
    port = 5000
    app.run(host='0.0.0.0', port=port)