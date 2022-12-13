import requests
import json


SERVER="https://chains.cosmos.directory"


class RestApi:
    def __init__(self, url, provider=None):
        self.url = url
        self.provider = provider

    def request(self, endpoint, returnjson=True):
        content = requests.get(f"{self.url}{endpoint}").text
        if returnjson:
            return json.loads(content)
        return content


class Peer:
    def __init__(self, pid, address):
        self.pid = pid
        self.address = address
    
        
class Cosmos:
    def __init__(self):
        self.chains = {}
        pass

    def getchain(self, chainname):
        if chainname in self.chains.keys():
            return self.chains[chainname]
        

    def search(self, n):
        n = n.upper()
        for cname, chain in self.chains.items(): 
            x = cname.upper().find(n)
            if x > -1:
                print(cname, n)
    
    def load_chains(self):
        content = requests.get(SERVER)
        chainlist = json.loads(content.text)
        for chain in chainlist["chains"]:
            name = chain["name"]
            self.chains[name] = Chain(name)
            restapis = chain["best_apis"]["rest"]
            for api in restapis:
                provider = None
                if "provider" in api.keys():
                    provider = api["provider"]
                self.chains[name].add_restapi(api["address"], provider=provider)


class Chain:
    def __init__(self, name):
        self.name = name
        self.restapi = {}
        self.peers = {}

    def add_restapi(self, url, provider):
        api = RestApi(url, provider)
        self.restapi[url] = api
