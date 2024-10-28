import requests
from typing import Dict, List
from datetime import datetime
import pandas as pd
import pytz

class ApiDatabricks:
    
    def __init__(self,  base_url: str, access_token: str):
        self.base_url = base_url
        self.header_default =  {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        }

            
    def convertTime(self, timestamp_ms: int):
        if timestamp_ms == '' or timestamp_ms == 0:
            return ''
        else:  
            timestamp_s = timestamp_ms / 1000
            date = datetime.fromtimestamp(timestamp_s)
            formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
            return formatted_date
    
    
    def duration(self, data_start: str, data_end: str):
        if data_end == '' or data_end == 0:
            # Define o fuso horário de Brasília
            fuso_brasilia = pytz.timezone('America/Sao_Paulo')
            # Obtém a data e hora atuais no fuso horário de Brasília
            data_hora_brasilia = datetime.now(fuso_brasilia).strftime("%Y-%m-%dT%H:%M:%S.%f")

            start = data_start
            # --------------------------------------            
            timestamp_s_start = start / 1000
            data_1 = datetime.fromtimestamp(timestamp_s_start)
            # -------------------------------------- 
            data_2 =  datetime.strptime(data_hora_brasilia[:26], "%Y-%m-%dT%H:%M:%S.%f")
            # Calcula a diferença
            diferenca = data_2 - data_1
            # Extraindo horas, minutos e segundos
            horas, resto = divmod(diferenca.seconds, 3600)
            minutos, segundos = divmod(resto, 60)
            # Exibindo no formato HH:mm:ss
            nova_data = (f"{horas:02}:{minutos:02}:{segundos:02}")
            return nova_data
        else:  
            start = data_start
            end = data_end

            # --------------------------------------            
            timestamp_s_start = start / 1000
            data_1 = datetime.fromtimestamp(timestamp_s_start)
            # -------------------------------------- 
            timestamp_s_end = end / 1000
            data_2 =  datetime.fromtimestamp(timestamp_s_end)
            # Calcula a diferença
            diferenca = data_2 - data_1
            # Extraindo horas, minutos e segundos
            horas, resto = divmod(diferenca.seconds, 3600)
            minutos, segundos = divmod(resto, 60)
            # Exibindo no formato HH:mm:ss
            nova_data = (f"{horas:02}:{minutos:02}:{segundos:02}")
            return nova_data
    

    def get_runs_jobs(self,data: str, ids_jobs: List[str]) -> List[Dict[str, str]]:
        new_list = []
        has_more = True
        next_page_token = ""
        date_from = f"{data} 00:00:00"
        date_to = f"{data} 23:59:59"
        date_obj_from = datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
        date_obj_to = datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
        timestamp_ms_from = int(date_obj_from.timestamp() * 1000)
        timestamp_ms_to = int(date_obj_to.timestamp() * 1000)
        while has_more:
            url = f"{self.base_url}/api/2.1/jobs/runs/list?start_time_from={timestamp_ms_from}&start_time_to={timestamp_ms_to}{next_page_token}"
            #print(url)
            resp = requests.get(url, headers=self.header_default)   
            for item in resp.json()['runs']:
                new_list.append({
                        "job_id": item.get("job_id", ''),
                        "run_name": item.get("run_name", ''),
                        "start_time": self.convertTime(item.get("start_time", '')),
                        "end_time": self.convertTime(item.get("end_time", '')),
                        "duration": self.duration(item.get("start_time", ''), item.get("end_time", '')),
                        "status": item.get("status", {}).get("state", ''),
                        "termination_details": item.get("status", {}).get("termination_details", {}).get("code", ''),
                        # "invoked_by": item.get("invokedBy", {}).get("invokedByType", '')            
                        })
            #&page_token=CAEQgdq5zKsyIO325e7Av2c=
            has_more = resp.json()['has_more']
            if(has_more):
                next_page_token = f"&page_token={resp.json()['next_page_token']}"
            else:
                next_page_token = ""
                break
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