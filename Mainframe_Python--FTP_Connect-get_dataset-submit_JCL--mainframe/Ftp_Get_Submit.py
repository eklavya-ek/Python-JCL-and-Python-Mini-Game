# -*- coding: utf-8 -*-
"""
Created on Sat May 25 13:40:12 2019

@author: NEO
"""
"""
This Script can be used to submit JCL, upload or retrieve datasets
out of HOST through FTP. Call the required method in the main function
with correct parameters within the function. 
"""


import getpass
import ftplib
import time


def get_input():
    """
    This function asks the user for FTP URL, user name and password to connect to HOST through FTP.
    The parameters are stored in a dictionary to later access in functions.
    This function can be modified to take additional parameters such as input files.
    """
    #get HOST URL from User
    host = input("Enter FTP URL to connect to:")
    #get Host Username
    user = input("Enter the Host user name: ")
    #get host password
    passwd = getpass.getpass("Enter user password: ")
    #store the parameters in a dictionary
    input_params = {'host' : host,
                    'user' : user,
                    'passwd' : passwd}
    return input_params
    
def ftp_connect(input_params):
    """
    This function connects to FTP using the input parameters provided and,
    can be called everytime we need to connect to HOST through FTP.
    It takes the input parameters as argument and uses it to connect. Returns and FTP object that can be used 
    for further object handling.
    """
    try:
        print("Connecting to Host...")
        #connect to Host using the input params.
        ftp = ftplib.FTP(host = input_params['host'],
                         user = input_params['user'],
                         passwd = input_params['passwd'])
    except ftplib.all_errors as err:
        print(str(err) + "-Incorrect Login Credentials...Program will quit.")
        time.sleep(3)
        quit()
    print("Connected to Host")
    return ftp
        
    
def ftp_disconnect(ftp):
    """
    This function takes the FTP object and closes the FTP connection.
    """
    print("Disconnecting from Host")
    ftp.quit()
    

def get_data(input_params):
    """
    This function retrieves a Host dataset and stores in a textfile(or CSV).
    """
    #create empty List to hold data
    ftp_data = []
    #provide the exact path of the text file location where to write and save the Host data
    output_textFile = open(r"Absolute Path of Output Text file" , 'w')
    try:
        #connect to Host
        ftp = ftp_connect(input_params)
        #Set connection as Active
        ftp.set_pasv(False)
        #Replace HLQ with the High Level Qualifier of the dataset(if dataset name is: ABC.DEFGHI.XYZ, put ABC)
        ftp.cwd("'HLQ'")
        #Replace DATASET.NAME with the second and the remaining qualifiers of the dataset( put DEFGHI.XYZ)
        #Reads the dataset and appends it to the empty List
        ftp.retrlines("RETR DATASET.NAME", ftp_data.append)
        #loops over the List and writes the data to a text file
        for line in ftp_data:
            output_textFile.write(line + '\n')
        #close text file
        output_textFile.close()
        #disconnect FTP
        ftp_disconnect(ftp)
    except ftplib.error_temp as err:
        print(str(err) + "First attempt to retrieve dataset failed, trying again...")
        time.sleep(3)
        #if first attempt is not successful, try again to retrieve the dataset
        get_data(input_params)
        

def put_data(input_params):
    """
    This fuction uploads the data from a text file to a Host dataset
    """
    ftp = ftp_connect(input_params)
    #give the absolute path of text file holding data tobe uplopaded
    input_textFile = open(r"Absolute Path of Input Text file" , 'rb')
    try:
        #connect to Host
        ftp = ftp_connect(input_params)
        #Set connection as Active
        ftp.set_pasv(False)
        #Replace HLQ with the High Level Qualifier of the dataset(if dataset name is: ABC.DEFGHI.XYZ, put ABC)
        ftp.cwd("'HLQ'")
        #Replace DATASET.NAME with the second and the remaining qualifiers of the dataset( put DEFGHI.XYZ)
        ftp.storlines("STOR DATASET.NAME", input_textFile)
        #close the input text file
        input_textFile.close()
        #disconnect from Host
        ftp_disconnect(ftp)
    except ftplib.all_errors as err:
        print(str(err) + "Trying to upload the dataset again...")
        #tries to upload the data again in case of any errors.
        put_data(input_params)
        
def sub_jcl(input_params):
    """
    This function takes a JCL file or a text file containing JCL code and submits it to JES in mainframe.
    It is required to first retrieve the JCL code(by copying it directly or storing it in a dataset and then using the retrieve function),
    from mainframe and save it in a text file.
    """
    #connect to Host
    ftp= ftp_connect(input_params)
    #read the file containing JCL code. Give the exact path of JCL or text file containing code to be submitted.
    jcl_file = open(r"Path of jcl or textfile containing JCL code", 'rb')
    #set connection as Active
    ftp.set_pasv(False)
    #telling the FTP that file type is going to be JES
    ftp.voidcmd('site filetype= JES')
    #Submits the JCL code in jcl_file through Internal Reader and prints the Job number of submitted JCL
    print(ftp.storlines('STOR INTRDR', jcl_file))
    #close the jcl file
    jcl_file.close()
    #disconnect from FTP
    ftp_disconnect(ftp)
    
    
if __name__ == '__main__':
    input_params = get_input()
    """ Call the Required functions as per the need below this"""