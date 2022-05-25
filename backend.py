import requests
import json
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS



#my code part

class AppBackend:   

    def __init__(self):
        pass


    def get_data_and_convert_to_json(from_url:str):

        str_json_data = NetworkWorker.request_json_data("https://www.themealdb.com/api/json/v1/1/categories.php")
        json_data = json.loads(str_json_data)
        print(json_data)




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

    def __init__(self, ip_address):

        self.ip_address = ip_address

    def sendDataToTSDB(to_url: str):

        with InfluxDBClient(url= to_url, token= __token, org=org) as client:
            
            with client.write_api(write_options= SYNCHRONOUS) as write_client:
                
                #data = Point("json")
                write_client.write(__bucket, __org, data)
            

if __name__ == "__main__":
    AppBackend()
