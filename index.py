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
    '''
    Inserts the details of the user into the database
    '''
    try:
        args = request.args
        firstname = args.get('firstname')
        lastname = args.get('lastname')
        email = args.get('email')

        conn = psycopg2.connect(dbname="postgres",
                                host='arcdb.czcf8pemmlto.us-east-1.rds.amazonaws.com',
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
    '''
    Gets the details of the user from the database
    '''
    data = []
    try:
        conn = psycopg2.connect(dbname="postgres",
                                host='arcdb.czcf8pemmlto.us-east-1.rds.amazonaws.com',
                                user="postgres", password="mystrongpassword")
        cur = conn.cursor()
        query = "SELECT * FROM public.user_details order by id;"
        cur.execute(query)
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        conn.close()
        return render_template("index.html", headings=["id", "firstname", "lastname", "email"], data=data)
    except Exception as e:
        return(str(e))

@app.route("/getPlotCSV", methods=["GET"])
def getPlotCSV():
    '''
    export the data to csv file
    '''
    try:
        conn = psycopg2.connect(dbname="postgres",
                                host='arcdb.czcf8pemmlto.us-east-1.rds.amazonaws.com',
                                user="postgres", password="mystrongpassword")
        cur = conn.cursor()
        cur.execute('''SELECT * FROM public.user_details order by id;''')
        rows=cur.fetchall()
        
        #Generate CSV FILE
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet(os.path.split('/tmp/output.csv')[1])

        worksheet.set_panes_frozen(True)
        worksheet.set_horz_split_pos(0)
        worksheet.set_remove_splits(True)

        #first element of each tuple is the header
        for colidx,heading in enumerate(cur.description):
            worksheet.write(0,colidx,heading[0]) 

        #Write rows to CSV file
        for rowidx, row in enumerate(rows):
            for colindex, col in enumerate(row):
                worksheet.write(rowidx+1, colindex, col)

        workbook.save('/tmp/output.csv')

        csv_file = "/tmp/output.csv"
        csv_path = os.path.join(csv_file)
        
        #check if file exists
        if not os.path.isfile(csv_path):
            return "ERROR: file %s was not found on the server" % csv_file

        conn.close()
        #Send the file back to the client
        return send_file(csv_path, as_attachment=True,  mimetype='text/csv', download_name=csv_file)

    except Exception as e:
        return(str(e))

if __name__ == "__main__":
    '''
    Run the app on localhost port 5000
    '''
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)