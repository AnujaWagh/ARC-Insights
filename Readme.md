# ARC Insights - Data Engineer - Assessment


### Aim of the assignment 
    1. To be able to ingest data using an API
    2. To be able to load the ingested data into a database of your choice
    3. Export the data to a CSV file

### Steps to run on localhost

* Install packages from the requirements.text

        pip install -r requirements.txt
        
* Run the index.py

        python index.py

* Go to localhost - Homepage will appear

        http://127.0.0.1:5000

* Follow below path to insert data into database (pass user input values to the query parameters)

        http://127.0.0.1:5000/insert_details?firstname=first_name&lastname=last_name&email=email

        e.g:
        http://127.0.0.1:5000/insert_details?firstname=jamie&lastname=paul&email=jamie.paul@test.com

* Fetch the existing data from the database

        http://127.0.0.1:5000/get_user_details

* Download the existing data from the database

        http://127.0.0.1:5000/getPlotCSV

### Steps to run on GCP host:

   https://arc-project-359722.ew.r.appspot.com/

* Insert data into database (pass user input values to the query parameters):

        https://arc-project-359722.ew.r.appspot.com/insert_details?firstname=jamie&lastname=paul&email=jamie.paul@test.com

* Fetch the existing data from the database:

        https://arc-project-359722.ew.r.appspot.com/get_user_details

* Download the existing data from the database:

        https://arc-project-359722.ew.r.appspot.com/getPlotCSV