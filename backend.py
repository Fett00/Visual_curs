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

    def sendDataToTSDB(self, data:dict, in_measure: str = "default"):

        import time

        with InfluxDBClient(url= self.__url, token= self.__token, org= self.__org) as client:
            
            with client.write_api(write_options= SYNCHRONOUS) as write_client:

                for i in data:                                                  
                        
                    field = i
                    value = data[i]
                    #print(value)
                    data = Point("json").measurement(in_measure).field(field, value)
                    write_client.write(self.__bucket, self.__org, data)
                    time.sleep(1)


class AppBackend:

    __json_ip = ""
    __tsdb_ip = ""

    def __init__(self):
        pass

    tsdb_sender = TSBDWorker()#TSBDWorker(ip_address = "")   


    def get_data_and_convert_to_json(self):

        str_json_data = NetworkWorker.request_json_data("http://192.168.1.46:8001")
        json_data = json.loads(str_json_data)
        out = self.flatten_data(json_data)
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
    
    #def auto_sender(self, timeout=1):

    def enter_tsdb_ip(self, ip_address):
        self.__tsdb_ip = ip_address
    
    def enter_json_ip(self, ip_address):
        self.__json_ip = ip_address

if __name__ == "__main__":
    a = AppBackend()
    json_data = a.get_data_and_convert_to_json()
    a.send_data_to_tsdb(json_data)
    
