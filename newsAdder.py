import os
from os import listdir
import pprint
import sys
from dbAdder import categoryToNewsMapp
from concurrent.futures import ThreadPoolExecutor, as_completed
from decorators import time_taken

subDir = {'australia':1,'canada':2,'malaysia':3,'singapore':4}

mainDir = '{path}/'.format(path=os.getcwd())
pyFileDir = []

def pyFinder():
    #this is to find all python files in dir
    for key, value in subDir.items():
        newpath = ''
        newpath = mainDir + key 
        for file in os.listdir(newpath):
            if file.endswith(".py"):
                pyFileDir.append(os.path.join(newpath, file))

#this is to exectue all python scripts 
#exection of python scripts are needed to be threaded
@time_taken
def pyExecuter():
    with ThreadPoolExecutor(max_workers=7) as executor:
        pool = [executor.submit(runner, item) for item in pyFileDir]
        #for task in as_completed(pool):
        #    task.result()

def runner(item):
    cwd = os.path.join(os.getcwd(), item)
    os.system('{} {}'.format('python3', cwd))    


jsonFileDir = {}
jsonFiles = []
#python script will genrate '*.json' file
#they are needed to be exported to dbAdder.py
#this is to find all json files in dir
def jsonFinder():
    for key, value in subDir.items():
        newpath = ''
        newpath = mainDir + key
        for file in os.listdir(newpath):
            if file.endswith(".json"):
                jsonFiles.append(os.path.join(newpath, file))
        jsonFileDir[value] = jsonFiles.copy()
        jsonFiles.clear()


if __name__ == "__main__":
    pyFinder()
    pyExecuter()
    jsonFinder()
    categoryToNewsMapp(jsonFileDir)
    pprint.pprint(jsonFileDir)
