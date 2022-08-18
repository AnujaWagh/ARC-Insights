from flask import Flask, request, render_template, send_file
import psycopg2
import os
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
    try:
        conn = psycopg2.connect(dbname="postgres",
                                host='test-db-postgres.c8cxqgsirbs0.eu-west-2.rds.amazonaws.com',
                                user="postgres", password="mystrongpassword")
        cur = conn.cursor()
        cur.execute('''SELECT * FROM public.user_details order by id;''')
        rows=cur.fetchall()
        
        # Generate CSV FILE
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet(os.path.split('output.csv')[1])

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
        workbook.save('output.csv')

        csv_file = "output.csv"
        csv_path = os.path.join(csv_file)
        
        # Also make sure the requested csv file does exist
        if not os.path.isfile(csv_path):
            return "ERROR: file %s was not found on the server" % csv_file
        # Send the file back to the client
        conn.close()
        return send_file(csv_path, as_attachment=True,  mimetype='text/csv', download_name=csv_file)

    except Exception as e:
        return(str(e))



    # workbook = xlwt.Workbook()
    # worksheet = workbook.add_sheet(os.path.split('output.csv')[1])

    # worksheet.set_panes_frozen(True)
    # worksheet.set_horz_split_pos(0)
    # worksheet.set_remove_splits(True)

    # for colidx,heading in enumerate(cur.description):
    #     worksheet.write(0,colidx,heading[0]) # first element of each tuple

    # # Write rows
    # for rowidx, row in enumerate(rows):
    #     for colindex, col in enumerate(row):
    #         worksheet.write(rowidx+1, colindex, col)

    # All done
    # workbook.save('output.csv')

if __name__ == "__main__":
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)