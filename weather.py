import requests

class Weather:

    def __init__(self) -> None:
        self.message = ""

    def get_taf(self, location: str):

        response = requests.get(f"https://api-redemet.decea.mil.br/mensagens/taf/{location}?api_key=sJgea8VlPUfxZDd2pH1p3DDw2Vyog6cMNDfres44")
        data = response.json()

        try:
            print(data['data']['data'][0]['mens'])
            self.message += f"{data['data']['data'][0]['mens']}\n{100*'_'}"
        except:
            self.message += f"No TAF for this location\n{100*'_'}"

        

    #Fetches current weather based on specific location
    def get_metar(self, location: str):

        response = requests.get(f"https://api-redemet.decea.mil.br/mensagens/metar/{location}?api_key=sJgea8VlPUfxZDd2pH1p3DDw2Vyog6cMNDfres44")

        data = response.json()

        try:
            print(data['data']['data'][0]['mens'])
            self.message += f"{data['data']['data'][0]['mens']}\n\n"
        except:
            self.message += 'No METAR for this location\n'


    def return_message(self):
        return self.message
    
    def clear_message(self):
        self.message = ""