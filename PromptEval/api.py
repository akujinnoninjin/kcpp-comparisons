from abc import ABC, abstractmethod

# API Interface Superclass 
class APIInterface(ABC):
    @abstractmethod
    # Returns a list of string, will be length 1 for non-batching APIs
    def generate(self, **kwargs) -> list[str]:
        pass
    # Requests the model name from the API 
    @abstractmethod
    def get_model_name(self) -> str:
        pass
    @abstractmethod
    def sampler_setup(self, **kwargs):
        pass

# Function to return an API object, which must inherit from the above
def get_API(type: str, url: str, token: str = None):
    if type == "kcpp":
        import PromptEval.api_handlers.kcpp
        print(f"Creating KCPP object at {url}")
        api =  PromptEval.api_handlers.kcpp.API(url)
    else:
        print(f"Invalid API type")
        raise ValueError(type)
    
    # Double check the returned API is actually an instance of the API superclass
    if not isinstance(api, APIInterface):
        raise TypeError(api)
    return api