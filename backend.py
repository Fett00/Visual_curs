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

    def sendDataToTSDB(self, json_data:dict, in_measure: str = "default"):

        import time

        with InfluxDBClient(url= self.__url, token= self.__token, org= self.__org) as client:
            
            with client.write_api(write_options= SYNCHRONOUS) as write_client:

                for i in json_data:                                                  
                        
                    field = i
                    value = json_data[i]
                    #print(value)
                    data = Point("json").measurement(in_measure).field(field, value)
                    write_client.write(self.__bucket, self.__org, data)


class AppBackend:

    __json_ip = ""
    __tsdb_ip = ""

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
    
    def send_data_to_tsdb(self, data:dict, in_measure: str = "default"):
        
        self.tsdb_sender.sendDataToTSDB(data, in_measure= in_measure)
        print("Successful send data to tsdb")
    
    def auto_sender(self, timeout=5):
        
        import time

        if self.__json_ip == "" or self.__tsdb_ip == "":
            return False

        while True:

            self.send_data_to_tsdb(self.get_data_and_convert_to_json(self.__json_ip))
            time.sleep(timeout)



    def enter_tsdb_ip(self, ip_address):
        self.__tsdb_ip = ip_address
    
    def enter_json_ip(self, ip_address):
        self.__json_ip = ip_address

    def get_flat_json_to_table(self):
        pass

if __name__ == "__main__":
    a = AppBackend()
    a.enter_json_ip(input("EnterJsonIp: "))
    a.enter_tsdb_ip(input("EnterTsdbIp: "))
    a.auto_sender()
    #json_data = a.get_data_and_convert_to_json()
    #a.send_data_to_tsdb(json_data)
    
