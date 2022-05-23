import requests
import json

#my code part

class AppBackend:   

    def __init__(self):
        
        str_json_data = NetworkWorker.request_json_data("https://www.themealdb.com/api/json/v1/1/categories.php")

        json_data = json.loads(str_json_data)
        print(json_data)




class NetworkWorker:

    @staticmethod
    def request_json_data(from_url):

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
    
    pass

if __name__ == "__main__":
    AppBackend()
