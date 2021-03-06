import sqlite3
import os



class DataBase():
    """Class to manage SQLite database

    :attribute current_path: contain the current path
    :type current_path: String.
    :attribute conn: object for the connexion to the data base
    :type conn: connexion (sqlite3)
    :attribute cur: cursor to do the connexion to the data base
    :type cur: cursor (sqlite3)
    

    """
    #Creation of the file to store the data base
    current_path =os.getcwd()
    
    #Choose a file name
    filename = "bd_test.sq3"
    
    #Connexion to the data_base (file is create if not exist)
    conn =sqlite3.connect(current_path+filename)
    
    #Cursor created to execute requests
    cur =conn.cursor()
    
    
    def create_Table(self, table_name, attributes ):
        """Function to create a new table if not exist

        :param table_name: name of the new table
        :type table_name: String.
        :param attributes: list of attributes in the table .
        :type attributes: List of ["AttributeName AttributeType"]
        
        :returns:  return true if the execution is successful, false else.
        
    
        """
        #Print
        print("Create table : \n")
        
        #Create a request (Beginning)
        request = "CREATE TABLE IF NOT EXISTS "+ table_name +"("; 
        
        #Construct the request with attributes
        for i in attributes :
            request = request+i+",";
        
        #Remove a ',' and end the request
        request = request.strip(',')
        request = request+')'
        
        
        
        #Execution of the request
        self.data_Base_Execute(request)
    
    
    def insert_into_Table(self, table_name,attributes, data):
        """Function to insert in a table

        :param table_name: name of the table to insert.
        :type table_name: String.
        :param attributes: list of attributes in the table .
        :type attributes: List of ["AttributeName AttributeType"].
        :param data: list of data to insert in the table  .
        :type data: List of values.
        
    
        """
        print("Insert into table : \n")
        
        #Create a request (Beginning)
        request ="INSERT INTO "+table_name+"("; 
        
        # Dynamic add of attributes to the request
        for j in attributes :
            l2=j.split(' ')
            request = request+l2[0]+",";
            
        #remove of the last ','
        request = request.strip(',')
        
        #Add to the request
        request= request+ ") VALUES(";
        
        #Add data to the request        
        for k in data :
            request = request+str(k)+",";
        
        #remove of the last ',' and add of the last ')'
        request = request.strip(',')
        request= request+ ");"
    
        
        #Execution of the request
        self.data_Base_Execute(request)

        
    def delete_from_Table(self, table_name,conditions):
        """Function to delete from a table

        :param table_name: name of the new table
        :type table_name: String.
        :param conditions: conditions of lines to delete .
        :type conditions = ["attr1 val1 ", "attr2 val2"] => Delete row from table where attr1=val1 && attr2 = val2

        
    
        """
        print("Delete from table : \n")
        
        #Create a request (Beginning)
        request ="DELETE FROM "+table_name+" WHERE "; 
        
        # Dynamic add of attributes to the request
        for i in conditions :
            ch=i.split(' ')
            attr=ch[0]
            val=ch[1]
            request = attr+" '"+val+"' "+"AND ";
            
        #remove of the last ','
        request = request.strip('AND')
        
        #Add end of the request
        request= request+ ";";
        
        #Execution of the request
        self.data_Base_Execute(request)     

    def close_Data_Base(self):
        """Function to close the DataBase       
    
        """
        
        #Connexion and cursor are closed
        self.cur.close() 
        self.conn.close()
    
    def data_Base_Execute(self, request):
        """Function to execute a request
               
        :param request: request to execute .
        :type request : a SQLite request
        
        :returns:  print an error if occurred
        """
        try:
            print("Execution of request "+request+"\n")
            
            #store delete in cursor
            self.cur.execute(request)
            
            #Execution of inserts
            self.conn.commit()
        except sqlite3.Error as e:
            print "An error occurred:", e.args[0]
        
        
        
        
        
        
