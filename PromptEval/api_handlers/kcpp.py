from ..api import APIInterface
from ..config import SamplerSettings
from json import dumps
from requests import post, get

class API(APIInterface):
    headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }
    sampler_settings = None
    url = None

    def __init__(self, url: str):
        print(f"Kcpp API Initialised at '{url}'")
        
        # Save endpoint URL
        self.url = url
        
        # Set up default sampler settings
        self.sampler_settings = SamplerSettings()
        
    def generate(self, prompt: str, seed: int):
        print (f"Kcpp Generator called for '{seed}:{prompt}'")
        payload = self.sampler_settings
        payload.prompt = prompt
        payload.sampler_seed = seed
        
        # api_response = post(self.url+"/api/v1/generate", headers=self.headers, data=dumps(payload))
        # if api_response is not None:
        #   if api_response.status_code == 200:
                # Access the response body as json
                # try:
                    # response[0] = api_response.json()['results'][0]['text']
                    # # print(response[0])
                    # return(response[0])
                # except (KeyError, IndexError) as e:
                    # print('Error accessing generation response:', e)
                    # return None
            # else:
                # print('Generation request failed with status code:', api_response.status_code)
                # return None
        # else:
            # print('Empty generation response - malformed prompt request?')
            # return None
        # # TODO: Handle errors more gracefully
        
        response = f'(response)'#: {vars(payload)}']
        return(response)
        
    def get_model_name(self):
        # response = get(api_url+"/api/v1/model", headers=self.headers)
        # if response is not None:
            # if response.status_code == 200:
                # # Access the response body as text
                # try:
                    # response_json = response.json()['result'];
                    # #print(response_json)
                    # return(response_json)
                # except (KeyError, IndexError) as e:
                    # print('Error accessing model name response:', e)
                    # return None
            # else:
                # print('Model name request failed with status code:', response.status_code)
                # return None
        # else:
            # print('Empty model name - ???')
            # return None
        # # TODO: Handle errors more gracefully
        response = f'modelname'
        return (response)
        
    def sampler_setup(self, **kwargs):
        self.sampler_settings = SamplerSettings(**kwargs)
        # print(vars(self.sampler_settings))