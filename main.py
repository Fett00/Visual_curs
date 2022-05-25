import frontend
import backend

class ProjectCoordinator:

    def __init__(self):
        pass

    backend_object = backend.AppBackend()
    
    @staticmethod
    def createEntryPoint():
        pass
        #Входная точка программы


if __name__ == '__main__':
    
    ProjectCoordinator.createEntryPoint()