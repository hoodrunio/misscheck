import requests
import json
import time
import traceback as tb

logfile = "error.log"


def logtime():
    t = time.localtime()
    return "%s%02d%02d-%02d:%02d:%02d" % (t[0], int(t[1]), int(t[2]), int(t[3]), int(t[4]), int(t[5]))


class Logger:
    def __init__(self, fname):
        self.fname = fname

    def message(self, msg):
        with open(self.fname, "a") as logger:
            logger.write(f"{logtime()} {msg}\n")


class Validator:
    def __init__(self, address, moniker):
        self.address = address
        self.moniker = moniker
        
    def __str__(self):
        return f"{self.address}|||{self.moniker}"


class Chain:
    def __init__(self, name, apiurl):
        self.name = name
        self.api = apiurl
        self.validators = {}
        self.get_validators()

    def save(self):
        fname = "chain_" + self.name + ".txt"
        with open(fname,"w") as out:
            for validator in self.validators.values():
                out.write(str(validator) + "\n")
            
    def get_validators(self):
        self.validators = {}
        text = requests.get(f"{self.api}/cosmos/staking/v1beta1/validators?status=BOND_STATUS_BONDED&pagination.limit=8000").text
        validatorlist = json.loads(text)
        print(len(validatorlist["validators"]))
        for validator in validatorlist["validators"]:
            addr = ""
            moniker = ""            
            try:
                addr = validator["operator_address"]
                moniker = validator["description"]["moniker"]
                self.validators[addr] = Validator(addr, moniker)
                
            except:
                tb.print_exc
                logger.message(f"Chain {self.name} address {addr} problem with json")
                

logger = Logger(logfile)

chains = {
    "umee": Chain("umee", "https://api.umee.huginn.tech"),
    "kujira" : Chain("kujira", "https://lcd.kaiyo.kujira.setten.io")
    }

for chain in chains.values():
    chain.save()
