from cosmos import Cosmos

c = Cosmos()
c.load_chains()

ume = c.getchain("umee")

print(ume.restapi["https://umee-api.polkachu.com/"].url)