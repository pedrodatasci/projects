import requests
import json
from time import sleep
import pandas as pd
import sys
import csv
import openpyxl

# functions

def formated_cnpj_list_from_file(f):
    cnpjs = [] # creates empty list to store data from csv
    reader = csv.reader(f) # object that contain each line from the csv as a list
    data = list(reader) # a list of lists, basically
    for i in range(len(data)): # for each line as an string
        cnpjs.append(data[i][0].replace('.','').replace('/', '').replace('-','')) # perform some replacements and append
    return consulting_aws(cnpjs) # returns consulting_aws function with the appended list as a parameter

def consulting_aws(cnpjs):
    payload={}
    headers = {
    }

    for cnpj in cnpjs: # for each element in the list
        response = requests.request("GET", url=f'https://www.receitaws.com.br/v1/cnpj/{cnpj}', headers=headers, data=payload) # use the element in a link to request a response as an json
        if json.loads((response.text))['status'] == 'ERROR': # if the request returns with status = ERROR
            response_to_df_and_save_it([cnpj, json.loads((response.text))])
            sleep(20)
        else:
            if not json.loads((response.text))['qsa']: # if there's no info in the 'qsa' key
                aux = [json.loads((response.text))['cnpj'],json.loads((response.text))['nome'],json.loads((response.text))['fantasia'],json.loads((response.text))['situacao'], json.loads((response.text))['abertura'],json.loads((response.text))['email'],json.loads((response.text))['telefone'], json.loads((response.text))['logradouro'], json.loads((response.text))['numero'],json.loads((response.text))['complemento'], json.loads((response.text))['bairro'], json.loads((response.text))['municipio'],json.loads((response.text))['cep'],json.loads((response.text))['uf'], json.loads((response.text))['atividade_principal'][0]['text'],json.loads((response.text))['atividade_principal'][0]['code'], json.loads((response.text))['qsa']]        
                response_to_df_and_save_it(aux)
            else:
                aux = [json.loads((response.text))['cnpj'],json.loads((response.text))['nome'],json.loads((response.text))['fantasia'],json.loads((response.text))['situacao'], json.loads((response.text))['abertura'],json.loads((response.text))['email'],json.loads((response.text))['telefone'], json.loads((response.text))['logradouro'], json.loads((response.text))['numero'],json.loads((response.text))['complemento'], json.loads((response.text))['bairro'], json.loads((response.text))['municipio'],json.loads((response.text))['cep'],json.loads((response.text))['uf'], json.loads((response.text))['atividade_principal'][0]['text'],json.loads((response.text))['atividade_principal'][0]['code'], json.loads((response.text))['qsa'][0]['qual'], json.loads((response.text))['qsa'][0]['nome']]
                response_to_df_and_save_it(aux) # append the response
                sleep(20) # sleep for 20 seconds, because we can only make 3 requests each minute

def response_to_df_and_save_it(response):
    df = pd.DataFrame(response)
    df.to_excel(writer, "Main")
    writer.save()

def renaming_dataframe(): 
    df = pd.read_excel('resultado.xlsx')
    df.rename(columns={0:'CNPJ', 1:'Nome', 2:'Fantasia', 3:'Situação', 4:'Data de Abertura', 5:'Email', 6:'Telefone', 7:'Logradouro', 8:'Número', 9:'Complemento', 10:'Bairro', 11:'Município', 12:'CEP', 13:'UF', 14:'Atividade Principal', 15:'CNAE', 16:'QSA', 17:'Nome Sócio'}, inplace=True) # rename the columns
    df.to_excel('resultado.xlsx')

def main():
    with open(sys.argv[1], newline='') as f: # open the csv file informed in terminal
        formated_cnpj_list_from_file(f) # runs this function
    renaming_dataframe()
    print('Done! Verify folder to check results.')

# run it

book = openpyxl.load_workbook('resultado.xlsx')
writer = pd.ExcelWriter('resultado.xlsx', engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
main()
