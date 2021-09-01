import json
import os
from time import time

try:
    import pandas as pd
except:
    os.system('''python -m pip install pandas''')
    import pandas as pd
try:
    import requests
except:
    os.system('''python -m pip install requests''')
    import requests
try:
    import easygui
except:
    os.system('''python -m pip install easygui''')
    import easygui

def get_info(json):
    df = pd.json_normalize(json)
    tracking_number = df['trackingNumber']
    return tracking_number

def requesting(code_list):
    print('Code list:\n',code_list)
    tracking_numbers = []
    i = 0
    for code in code_list:
        i += 1
        print(f'{i}/{len(code_list)} / {round(i/len(code_list),2)*100}%')
        url = "https://www.sypost.net/queryTrack?toLanguage=en_US&trackNumber=" + code

        payload={}
        headers = {
          'Referer': 'https://www.sypost.net/search?orderNo='+ code
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        response_json = response.text[15:]
        response_json = response_json[:-1]
        response_json = json.loads(response_json)['data']
        if response_json[0]['has'] == False:
            tracking_numbers.append('Erro. Código não identificado.')
        elif response_json[0]['has'] == True:
            tracking_number = get_info(response_json)
            tracking_numbers.append(tracking_number[0])                             
    return into_df(code_list, tracking_numbers)

def into_df(code_list, new_code_list):
    data = {'codigo_SY': code_list, 'novo_codigo': new_code_list}

    new_df = pd.DataFrame(data)

    new_df.to_excel('./resultado.xlsx')

def main():
    print('Welcome! Choose a file.\n')
    f = easygui.fileopenbox(filetypes='*.csv')
    t1 = time()
    requesting(pd.read_csv(f).iloc[:, 0])
    t2 = time()
    print(f'Done! Verify folder to check results. It took {round(t2-t1, 2)} seconds to run!')

main()

