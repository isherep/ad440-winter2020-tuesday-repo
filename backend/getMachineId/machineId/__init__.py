import logging
import azure.functions as func
import os
import pyodbc
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        #connect to database
        # Setting connection to the database via key vault connection string.
        conn = pyodbc.connect(os.environ['ConnString'])
        logging.info("Connected to database")
        cursor = conn.cursor()
    
        #variable for machine id parameter 
        machineId = req.route_params.get('MachineID')
        logging.info(machineId)
    
        #select specific machine by ID from machine table in database
        rows = cursor.execute('''SELECT * FROM [dbo].[Machines] WHERE MachineID = ?''', machineId).fetchone()
        logging.info(rows)
        
        #get column names and turn into json file 
        column_names = [column[0] for column in cursor.description]
        result = [dict(zip(column_names, rows))]
        
        #commit the query 
        conn.commit()
        
        #return the query 
        return func.HttpResponse(json.dumps(result))
    
        #disconnect database
        cursor.close()
        conn.close()
        logging.info("Connection to database closed")
        
    #connection failed error  
    except pyodbc.DatabaseError:
        logging.error("Could not connect to database")
    
    #machine id not found error
    except TypeError:
        logging.error("Machine ID not found")
    
    #invalid input
    except ValueError:
        logging.debug("Invaled input")
        
  
        
        
    
        
    
    