import requests
from typing import Dict, List
import time
from datetime import datetime, timedelta, timezone
import pandas as pd
import json

class ApiDataFactory:
    
    def __init__(self,  tenent_id: str, client_id: str, client_secret: str, subscriptions: str, resource_groups: str, factories: str):
        self.subscriptions = subscriptions
        self.resource_groups = resource_groups
        self.factories = factories
        self.tenent_id = tenent_id  
        self.client_id = client_id 
        self.client_secret = client_secret
        self.token_expiry = time.time() + 0
        self.header_default =  {
        'Content-Type': 'application/json',
        'Authorization': f'',
        }
        self.__renovar_token()
           
    def __auth(self):  
        url = f"https://login.microsoftonline.com/{self.tenent_id}/oauth2/v2.0/token"
        payload = f'grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}&scope=https://management.azure.com/.default'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if(response.status_code == 200):
            access_token =  response.json()['access_token']
            self.token_expiry = time.time() + response.json()['expires_in']
            data_hora = datetime.fromtimestamp(self.token_expiry)
            data_formatada = data_hora.strftime('%Y-%m-%d %H:%M:%S')
            #print(f"Token resgatado expira em: {data_formatada}, será renovado de forma automatica")
            self.header_default['Authorization'] = f"Bearer {access_token}"
        else:
            error = response.json()['error']
            raise ValueError(error)
        
    def __renovar_token(self):
        if  self.header_default['Authorization'] == '' or time.time() >= (self.token_expiry):
            self.__auth()
            
    def convertTime(self, data_str: str):
        if data_str == '':
            return ''
        else:  
            # data_str = "2024-10-25T22:15:13.0232522Z"
            # Convertendo a string para um objeto datetime (ignorando os últimos dígitos dos milissegundos)
            data = datetime.strptime(data_str[:26], "%Y-%m-%dT%H:%M:%S.%f")

            nova_data = data - timedelta(hours=0)
            #print("Data original:", data.strftime('%Y-%m-%d %H:%M:%S'))
            #print("Data ajustada:", nova_data.strftime('%Y-%m-%d %H:%M:%S'))
            return nova_data.strftime('%Y-%m-%d %H:%M:%S')
    
    
    def duration(self, data_start: str, data_end: str):
        if data_end == '':
            # data_str = "2024-10-25T22:15:13.0232522Z"
            # Convertendo a string para um objeto datetime (ignorando os últimos dígitos dos milissegundos)
            data_1 = datetime.strptime(data_start[:26], "%Y-%m-%dT%H:%M:%S.%f")
            # acrescenta 3 horas para ficar no fuso do power automate
            data_2 =  datetime.strptime(str(datetime.now(timezone.utc))[:26], "%Y-%m-%d %H:%M:%S.%f")
            # Calcula a diferença
            diferenca = data_2 - data_1

            # Extraindo horas, minutos e segundos
            horas, resto = divmod(diferenca.seconds, 3600)
            minutos, segundos = divmod(resto, 60)

            # Exibindo no formato HH:mm:ss
            nova_data = (f"{horas:02}:{minutos:02}:{segundos:02}")
            return nova_data
        else:  
            # data_str = "2024-10-25T22:15:13.0232522Z"
            # Convertendo a string para um objeto datetime (ignorando os últimos dígitos dos milissegundos)
            data_1 = datetime.strptime(data_start[:26], "%Y-%m-%dT%H:%M:%S.%f")
            data_2 = datetime.strptime(data_end[:26], "%Y-%m-%dT%H:%M:%S.%f")
            # Calcula a diferença
            diferenca = data_2 - data_1

            # Extraindo horas, minutos e segundos
            horas, resto = divmod(diferenca.seconds, 3600)
            minutos, segundos = divmod(resto, 60)

            # Exibindo no formato HH:mm:ss
            nova_data = (f"{horas:02}:{minutos:02}:{segundos:02}")
            return nova_data
    

    def get_pipelines(self,data: str, name_pipelines: List[str]) -> List[Dict[str, str]]:
        self.__renovar_token()
        filters = { "lastUpdatedAfter": f"{data}T00:00:00.0000000Z",
                "lastUpdatedBefore": f"{data}T23:59:59.3686473Z",
                "filters": [
                {
                "operand": "PipelineName",
                "operator": "In",
                    "values": []}] }
        new_list = []
        for id in name_pipelines:
            filters['filters'][0]['values'].append(id)
            
        payload = json.dumps(filters)
        resp = requests.post(f"https://management.azure.com/subscriptions/{self.subscriptions}/resourceGroups/{self.resource_groups}/providers/Microsoft.DataFactory/factories/{self.factories}/queryPipelineRuns?api-version=2018-06-01", headers=self.header_default, data=payload)     
        for item in resp.json()['value']:
            new_list.append({
                    "id_pipelineName": item.get("pipelineName", ''),
                    "pipelineName": item.get("pipelineName", ''),
                    "start_time": self.convertTime(item.get("runStart", '')),
                    "end_time": self.convertTime(item.get("runEnd", '')),
                    "duration": self.duration(item.get("runStart", ''), item.get("runEnd", '')),
                    "status": item.get("status", ''),
                    "invoked_by": item.get("invokedBy", {}).get("invokedByType", '')            
                    })
        return self.SQLQuery(new_list)
    
    
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