import requests
import json
from time import sleep
import pandas as pd
import sys
import csv
import openpyxl

def formated_cnpj_list_from_file(f):
    cnpjs = [] # creates empty list to store data from csv
    reader = csv.reader(f) # object that contain each line from the csv as a list
    data = list(reader) # a list of lists, basically
    for i in range(len(data)): # for each line as an string
        cnpjs.append(data[i][0].replace('.','').replace('/', '').replace('-','')) # perform some replacements and append
    return consulting_aws(cnpjs) # returns consulting_aws function with the appended list as a parameter

def consulting_aws(cnpjs):
    responses = [] # empty list to store lists that will become lines in a dataframe later

    payload={}
    headers = {
    }

    for cnpj in cnpjs: # for each element in the list
        response = requests.request("GET", url=f'https://www.receitaws.com.br/v1/cnpj/{cnpj}', headers=headers, data=payload) # use the element in a link to request a response as an json
        if json.loads((response.text))['status'] == 'ERROR': # if the request returns with status = ERROR
            responses.append([cnpj, json.loads((response.text))]) # append the element and the ERROR status and message
            sleep(20)
        else:
            if not json.loads((response.text))['qsa']: # if there's no info in the 'qsa' key
                aux = [json.loads((response.text))['cnpj'],json.loads((response.text))['nome'],json.loads((response.text))['fantasia'],json.loads((response.text))['situacao'], json.loads((response.text))['abertura'],json.loads((response.text))['email'], json.loads((response.text))['logradouro'], json.loads((response.text))['numero'],json.loads((response.text))['complemento'], json.loads((response.text))['bairro'], json.loads((response.text))['municipio'],json.loads((response.text))['cep'], json.loads((response.text))['atividade_principal'][0]['text'],json.loads((response.text))['atividade_principal'][0]['code'], json.loads((response.text))['qsa']]        
            else:
                aux = [json.loads((response.text))['cnpj'],json.loads((response.text))['nome'],json.loads((response.text))['fantasia'],json.loads((response.text))['situacao'], json.loads((response.text))['abertura'],json.loads((response.text))['email'], json.loads((response.text))['logradouro'], json.loads((response.text))['numero'],json.loads((response.text))['complemento'], json.loads((response.text))['bairro'], json.loads((response.text))['municipio'],json.loads((response.text))['cep'], json.loads((response.text))['atividade_principal'][0]['text'],json.loads((response.text))['atividade_principal'][0]['code'], json.loads((response.text))['qsa'][0]['qual'], json.loads((response.text))['qsa'][0]['nome']]
        responses.append(aux) # append the response
        sleep(20) # sleep for 20 seconds, because we can only make 3 requests each minute

    return dataframe_the_response(responses) # return the dataframe function with those responses as parameters

def dataframe_the_response(responses): 
    df = pd.DataFrame(responses) # creates a df
    df.rename(columns={0:'CNPJ',1:'Nome',2:'Nome Fantasia', 3:'Situação', 4:'Data de Abertura', 5:'Email', 6:'Logradouro', 7:'Número', 8:'Complemento', 9:'Bairro', 10:'Municipio', 11:'CEP', 12:'Atividade Principal', 13:'CNAE', 14:'QSA', 15:'Nome Sócio'}, inplace=True) # rename the columns
    df.to_excel('resultado_consulta_receita.xlsx') # save it as an excel file

def main():
    with open(sys.argv[1], newline='') as f: # open the csv file informed in terminal
        formated_cnpj_list_from_file(f) # runs this function
    print('Done! Verify folder to check results.')

main()
