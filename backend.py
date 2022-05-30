import requests
import json
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS



#my code part




class NetworkWorker:

    @staticmethod
    def request_json_data(from_url:str):

        response = requests.get(url=from_url)

        if response.status_code == 200:

            try:

                return response.text

            except requests.exceptions.JSONDecodeError:

                print("Failed to parse JSON")
        else:

            print("Error, requests status is: " + response.status_code)
            return ""


class TSBDWorker:

    # You can generate an API token from the "API Tokens Tab" in the UI
    __token = "alNYIZmAFTYCdivqewugYUEXsU3ZGbAR08748qjJCa82yEgLUfMwIn11Mo4-ZvaVm4Z5f39IdKXr5tZoSvuFPQ=="
    __org = "sdk"
    __bucket = "Visual_curs"
    __url = "http://192.168.1.46:8086"

    #url  "http://192.168.1.46:8086"

    def sendDataToTSDB(self, json_data:dict, tsdb_url:str, in_measure: str = "default"):

        import time

        with InfluxDBClient(url= tsdb_url, token= self.__token, org= self.__org) as client:
            
            with client.write_api(write_options= SYNCHRONOUS) as write_client:

                for i in json_data:                                                  
                        
                    field = i
                    value = json_data[i]
                    print(field)
                    #print(value)
                    data = Point("json").measurement(in_measure).field(field, value)
                    try:
                        write_client.write(self.__bucket, self.__org, data)
                    except:
                        print("Write failed cancel and try again")
                        break


class AppBackend:

    json_ip = ""
    tsdb_ip = ""

    def __init__(self):
        pass

    tsdb_sender = TSBDWorker()#TSBDWorker(ip_address = "")   


    def get_data_and_convert_to_json(self, ip_address:str):

        str_json_data = NetworkWorker.request_json_data(ip_address)
        json_data = json.loads(str_json_data)
        out = self.flatten_data(json_data)
        print("Successful get data and convert it to json")
        return out
        #print(json_data)

    def flatten_data(self, y):
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return out
    
    def send_data_to_tsdb(self, data:dict, url:str, in_measure: str = "default"):
        
        self.tsdb_sender.sendDataToTSDB(data, tsdb_url=url, in_measure= in_measure)
    
    def auto_sender(self, data_key_list:list, timeout=5):
        
        import time

        if self.json_ip == "" or self.tsdb_ip == "":
            print("Failed ip address is missing")

        while True:

            data = self.get_data_and_convert_to_json(self.json_ip)

            if data != None or data != {}:
                
                corrected_data = {}

                for i in data_key_list:
                    corrected_data[i] = data[i]

                self.send_data_to_tsdb(corrected_data, url=self.tsdb_ip)
                time.sleep(timeout)
            else:
                print("Error: no data to send")



    def enter_tsdb_ip(self, ip_address):
        self.tsdb_ip = str(ip_address)
    
    def enter_json_ip(self, ip_address):
        self.json_ip = str(ip_address)

    def get_flat_json_to_table(self):
        pass

if __name__ == "__main__":

    a = AppBackend()

    while True:
        try:
            json_ip = input("Enter Json Ip: ")
            tsdb_ip = input("Enter Tsdb Ip: ")
            requests.get(json_ip)
            a.enter_json_ip(json_ip)
            a.enter_tsdb_ip(tsdb_ip)
            break
        except:
            print("Try again!")

    data = a.get_data_and_convert_to_json(a.json_ip)

    if data != None or data != {}:
        print("Получен json файл. Кол-во полей в котором равно: ", len(data))
        print("Выбирете способ выбора полей для отправки в БД:\n1) Отправить все\n2) Указать диапазон\n3) Указать номер конкретного поля")
        choosen_number = int(input())
        
        while True:
            if choosen_number == 1:
                a.auto_sender(list(data))
                break
            elif choosen_number == 2:

                n = None
                m = None
                
                while True:
                    print("Введите значения n и m где m и n целые числа диапазона и n<m и n >= 1")
                    try:
                        n = int(input("n: ")) - 1
                        m = int(input("m: ")) - 1

                        if (n < m) and (n in range(0, len(data))) and (m in range(0, len(data))):
                            break
                        else:
                            raise ValueError("Error")
                    except:
                        print("Неправильные данные попробуйте еще раз")
                a.auto_sender(list(data)[n:m])
                break
            elif choosen_number == 3:

                n = None

                while True:
                    print("Введите значения n где n целое число и n >= 1")
                    n = int(input("n: ")) - 1
                    if (n in range(0, len(data))):
                        break
                    else:
                        print("Неправильные данные попробуйте еще раз")
                a.auto_sender([(list(data)[n])])
                break
            else:
                print("Пожалуйста введите корректный номер: ")
    a.auto_sender()
    
