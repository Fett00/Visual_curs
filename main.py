#import frontend
import backend

class ProjectCoordinator:

    def __init__(self):
        pass

    backend_object = backend.AppBackend()
    
    @staticmethod
    def createEntryPoint():
        pass
        #Входная точка программы
    
    @staticmethod
    def createEntryPointForIndependentBackend():
        ProjectCoordinator.startBackend()

    @staticmethod
    def startBackend():

        import requests
        import json
        from datetime import datetime

        from influxdb_client import InfluxDBClient, Point, WritePrecision
        from influxdb_client.client.write_api import SYNCHRONOUS

        a = backend.AppBackend()

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


if __name__ == '__main__':
    
    ProjectCoordinator.createEntryPointForIndependentBackend()