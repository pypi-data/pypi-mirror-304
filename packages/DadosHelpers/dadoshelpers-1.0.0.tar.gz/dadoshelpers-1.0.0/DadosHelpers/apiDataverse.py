import requests
from typing import Dict, List
import json
import time
from datetime import datetime
import pandas as pd

class ApiDataverse:
    
    def __init__(self, base_url: str, tenent_id: str, client_id: str, client_secret: str):
        self.base_url = base_url
        self.tenent_id = tenent_id  
        self.client_id = client_id 
        self.client_secret = client_secret
        self.token_expiry = time.time() + 0
        self.header_default =  {
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Prefer': 'odata.include-annotations="*"',
        'Content-Type': 'application/json',
        'Authorization': f'',
        }
        
    
    def insert(self, table: str, values: List[Dict[str, any]]) -> Dict[str, str]:
        url = f"{self.base_url}/api/data/v9.0/{table}"      
        for item in values:
            self.__renovar_token()
            payload = json.dumps(item)
            response = requests.request("POST", url, headers=self.header_default, data=payload)
            if response.status_code in [200, 204]:
                pass
            else:
                print(json.dumps(response.json(),indent=2))
                raise ValueError(response.json())
            
            
    def delete(self, table: str, id: str) -> Dict[str, str]:
        self.__renovar_token()
        url = f"{self.base_url}/api/data/v9.0/{table}({id})"
        response = requests.request("DELETE", url, headers=self.header_default)
        
        if(response.status_code in [200,201,204]):
            pass
        else:
            print(json.dumps(response.json(),indent=2))
            raise ValueError("Erro ao realizar chamada")

                        
  
    def show_tables(self) -> Dict[str, str]:
        self.__renovar_token()
        url = f"{self.base_url}/api/data/v9.0/EntityDefinitions"
        payload = ""
        response = requests.request("GET", url, headers=self.header_default, data=payload)    
        if(response.status_code == 200):
            transformed_data = [{"DisplayName": item["DisplayCollectionName"]['LocalizedLabels'][0]['Label'] if len(item["DisplayCollectionName"]['LocalizedLabels']) > 0 else '',
                                 "LogicalCollectionName": item['LogicalCollectionName']} for item in response.json()['value']]
            return self.SQLQuery(transformed_data)
        else:
            print(json.dumps(response.json(),indent=2))
            raise ValueError("Erro ao realizar chamada!")
        

    def get_table(self, table: str) -> Dict[str, str]:
        self.__renovar_token()
        url = f"{self.base_url}/api/data/v9.0/{table}"
        payload = ""
        response = requests.request("GET", url, headers=self.header_default, data=payload)        
        if(response.status_code == 200):
            return self.SQLQuery(response.json()['value'])
        else:
            raise ValueError("Erro ao realizar chamada!")
        
    def __auth(self):  
        url = f"https://login.microsoftonline.com/{self.tenent_id}/oauth2/v2.0/token"
        payload = f'grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}&scope=https://tivioapps-dsv.crm2.dynamics.com/.default'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if(response.status_code == 200):
            access_token =  response.json()['access_token']
            self.token_expiry = time.time() + response.json()['expires_in']
            data_hora = datetime.fromtimestamp(self.token_expiry)
            data_formatada = data_hora.strftime('%Y-%m-%d %H:%M:%S')
            #print(f"Renovei o token, expira em: {data_formatada}")
            self.header_default['Authorization'] = f"Bearer {access_token}"
        else:
            error = response.json()['error']
            raise ValueError(error)
        
    def __renovar_token(self):
        if  self.header_default['Authorization'] == '' or time.time() >= (self.token_expiry):
            self.__auth()
            
    class SQLQuery:
        
        def format_table(self, data, headers):
            # Calcula a largura máxima de cada coluna
            col_widths = [
                max(len(str(row[header])) for row in data) if data else 0
                for header in headers
            ]
            col_widths = [
                max(col_width, len(header)) + 2  # Espaçamento extra
                for col_width, header in zip(col_widths, headers)
            ]
            
            # Define as bordas da tabela
            top_border = "┌" + "┬".join("─" * width for width in col_widths) + "┐"
            header_border = "├" + "┼".join("─" * width for width in col_widths) + "┤"
            bottom_border = "└" + "┴".join("─" * width for width in col_widths) + "┘"

            # Inicializa a tabela como uma string
            table_str = top_border + "\n"

            # Adiciona o cabeçalho da tabela
            header_row = "│" + "│".join(f"{header:^{col_widths[i]}}" for i, header in enumerate(headers)) + "│"
            table_str += header_row + "\n"

            # Adiciona a borda do cabeçalho
            table_str += header_border + "\n"

            # Adiciona as linhas de dados
            for row in data:
                data_row = "│" + "│".join(f"{str(row[header]):^{col_widths[i]}}" for i, header in enumerate(headers)) + "│"
                table_str += data_row + "\n"

            # Adiciona a borda inferior
            table_str += bottom_border + "\n"
            
            return table_str
        
        def __init__(self, data):
            self.data = data
            self._df_called = False  # Controle interno para saber se `.df()` foi chamado
            self._dict_called = False

        def df(self):
            # Define que `.df()` foi chamado e retorna o DataFrame simulado
            self._df_called = True
            return pd.DataFrame.from_dict(self.data)
        
        def dict(self):
            # Define que `.df()` foi chamado e retorna o DataFrame simulado
            self._df_called = True
            return self.data
             

        def __repr__(self):
            # Retorna um dicionário se `.df()` não foi chamado
            if not self._df_called or not self._dict_called:
                if len(self.data) > 0:
                    # Dados de exemplo
                    headers = self.data[0].keys()
                    data = self.data
                    # Chamada da função para imprimir a tabela formatada
                    return self.format_table(data, headers)
                else:
                    return "Nenhum dados para exibição"
        
            # Caso contrário, retorna uma string vazia, pois o resultado do .df() já foi retornado
            return ""
        
