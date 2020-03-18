import logging
import pyodbc
import azure.functions as func
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # connect to database
        logging.debug('Starting connection to database...')
        logging.log(10,'starting conn...')
        conn = pyodbc.connect(os.environ['ConnString'])
        cursor = conn.cursor()
        logging.debug('Connected to database')  
    
        # read JSON body
        req_body = req.get_json()
        logging.debug('Content of JSON body: ' + str(req_body))
        
        # insert data into SQL
        cursor.execute(
            '''INSERT INTO [dbo].[Machines] (Model, ModelNum, ModelPhoto, SerialNum, VendorID, LocationID)
            VALUES (?,?,?,?,?,?)''', (req_body['Model'], req_body['ModelNum'], req_body['ModelPhoto'], req_body['SerialNum'], req_body['VendorID'], req_body['LocationID'])
            )

        # commit data to database
        logging.debug('Commiting new machine ID to database')
        conn.commit()
        logging.debug('Commit complete')

        # close connection
        conn.close()
        
        # POST request successful
        logging.info('Http trigger request complete')
        return func.HttpResponse(f"Successful request")

    except ValueError as jerr:
        logging.error("Incorrect JSON format " + str(jerr))
        return func.HttpResponse('Incorrect JSON format')
    except pyodbc.DatabaseError as derr:
        logging.error("Connection to the database failed " + str(derr))
        return func.HttpResponse('Connection failed')
    except pyodbc.ProgrammingError as perr:
        logging.error("Your record could not be added " + str(perr))
        return func.HttpResponse('Machine could not be added')

     # no POST request was made
    logging.info("No POST request was made")
    return func.HttpResponse(   
        "Please pass a POST request in the request body",   
        status_code=400 
        )