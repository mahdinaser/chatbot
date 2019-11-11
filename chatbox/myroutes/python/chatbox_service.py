#middleware program to communicate with natural language machine learning model
import sys, json, numpy as np
#import time
import csv
import os
import re


# importing the requests library
import requests



#Read data from stdin
def read_in():
    #lines = [1,2,3,5,6,7]
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])#lines

def chat(q):

    # defining the api-endpoint
    # API_ENDPOINT = "http://52.168.33.198/chatbot"
    API_ENDPOINT = "http://localhost/chatbot"

    sampleQuery = q #'Will muscle relaxers help me sleep and help rls at night during detox?'

    # data to be sent to api
    data = {'query': sampleQuery}

    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data)

    # extracting response text
    pastebin_url = r.text
    print(pastebin_url)

def main():
    #get our data as an array from read_in()
    lines = read_in()
    #lines = [1,2,3,4,5,6,7,8,9]
    #print(lines)
    #create a numpy array
    np_lines = np.array(lines)
    # print('np_lines', np_lines)
    customer_question = np_lines[1]
    # customer_question = customer_question.replace("'", "")
    # print('customer_question:'+ customer_question)
    # print("os.path.abspath('.')", os.path.abspath('.'))#print os.path()


    # print('Hi')
    chat(customer_question)
    print('##end session##')
    count = 1
    # if count == -1:
    #     print ("Error")
    # else:
    #     print("###The file has been stored to the database, successfully!count"+count)
    # print('##end session##')

#start process
if __name__ == '__main__':
    main()