import json
import yaml
import os
import requests

# TODO: Make a lot of this passable as command arguments

# Time estimates: 
    # Each generation is default 500 tokens
    # Each prompt is default 3 seeds right now - will be going up to 10
        # Make the seeds cycle a toggle? So can do 10 for models want to go more in depth with, 3 for surface stuff
        # Could also do 1 in theory; but it's potentially not as informative
    # Therefore each prompt is 1500 / 5000 tokens 
        # Which is 25/80 minutes at 1t/s
        # Or 2.5/8 minutes at 10t/s
        # Or 50s/2m45 at 30t/s
    # So this is *fucking slow*, and gets geometrically slower as you add more things
        # Certain tests are going to be much faster
        # And this is a worst case scenario where it doesn't hit any stopping strings
    
#If URL specified, assume only using hosted model
api_url = "http://10.10.100.112:5001/api/v1/" #127.0.0.1:5001" #TODO: Read from command line args

#If path is specified, assume loading model
#kcpp_path = "./koboldcpp-main/koboldcpp/koboldcpp.py"
    # --model single model
    # --models model folder
    # --numactl 24 numactl threads, assumed 0 if not specified
    # --usecublas #assume 200 offload layers for now; difficult to specify partials 
    # --useblas toggle`

# Assume input prompt file is in same folder, prompts.yaml
promptlists_path = "prompts/default.yaml"

# Assume configs are in same folder, config.yaml
seeds = [8675309] #, 12345678] #, 314159265, 181811]

sampler_defaults = {
              "max_context_length": 1600,
              "max_length": 500,
              "rep_pen": 1,
              "temperature": 1,
              "smoothing_factor" : 0.25,
              "top_p": 1,
              "top_k": 0,
              "top_a": 0,
              "typical": 1,
              "tfs": 1,
              "rep_pen_range": 320,
              "rep_pen_slope": 0.7,
              "sampler_order": [6, 0, 1, 3, 4, 2, 5],
              "memory": "",
              "min_p": 0,
              "dynatemp_range": 0,
              "presence_penalty": 0,
              "logit_bias": {},
              #"prompt": prompt['prompt'],
              "quiet": True,
              "stop_sequence": ["You:", "\nYou ", "\n: "],
              "use_default_badwordsids": False,
              #"sampler_seed": seed
            }


def API_GetGeneration(payload):
    headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }
    # make API POST request
    # api_response = requests.post(api_url+"generate", headers=headers, data=json.dumps(payload))
    return ('testprompt' + str(payload['sampler_seed']))  ################################### DEBUG
    #print(response)
    #Save response to file
    if api_response is not None:
        if api_response.status_code == 200:
        # Access the response body as json
            try:
                response = api_response.json()['results'][0]['text']
                # print(response)
                return(response)
            except (KeyError, IndexError) as e:
                print('Error accessing generation response:', e)
                return None
        
        else:
            print('Generation request failed with status code:', api_response.status_code)
            return None
    else:
        print('Empty generation response - malformed prompt request?')
        return None
    # TODO: Handle errors more gracefully

def API_GetModel():
    headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }
    return 'testmodel'                  ################################# DEBUG
    response = requests.get(api_url+"model", headers)
    if response is not None:
        if response.status_code == 200:
            # Access the response body as text
            try:
                response_json = response.json()['result'];
                #print(response_json)
                return(response_json)
            except (KeyError, IndexError) as e:
                print('Error accessing model name response:', e)
                return None
        else:
            print('Model name request failed with status code:', response.status_code)
            return None
    else:
        print('Empty model name - ???')
        return None
    # TODO: Handle errors more gracefully
    
def File_LoadYaml(file_path):
    try:
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load_all(file)
            return list(yaml_data)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file '{file_path}': {exc}")
    # TODO: Handle errors more gracefully

def File_LoadPromptList(file_path):
    # Interface function, in case I decide to change this up to a YAML or CSV or something
    prompt_list = File_LoadYaml(promptlists_path)
    if not prompt_list:
        print("Error loading YAML file: " promptlists_path)
        return None
    else:
        return prompt_list
    # TODO: Handle errors more gracefully

def File_WriteToJson(file_path, new_data):
    existing_data = []
    if os.path.exists(file_path):
        # If the file exists, read its content
        with open(file_path, "r") as file:
            existing_data = json.load(file)
        
        new_model = next(iter(new_data))
        
        existing_model = existing_data.get(new_model)
        
        if existing_model == None:
            print("New model! Append whole thing!")
        else:
            print("Existing model! Checking prompts!")
            for newprompt in new_data[new_model]['prompts']:
                existing_prompt = existing_data[new_model]['prompts'].get(newprompt)
                if existing_prompt == None:
                    print("New Prompt! Append it to the section!")
                else:
                    print("Existing Prompt! Checking seeds!")
                    for newseed in new_data[new_model]['prompts'][newprompt]['seeds']:
                        print(newseed)
                        existing_response = existing_data[new_model]['prompts'][newprompt]['seeds'].get(str(newseed))
                        if existing_response == None:
                            print("New Seed! Append it to the section!")
                        else:
                            print("Existing Seed! Skip!")

     
       
       
    else:
        existing_data = new_data

    # Write the updated data to the JSON file
    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)

    print("Outputs have been been written to", file_path)
    return None

def Generations(prompt_list, seeds):
    # Takes prompt list and seeds, makes gen requests, returns an object in format
    # { prompt_name: {seed:gen, seed:gen, seed:gen }, prompt_name: {seed:gen... etc
    responses = {}
    
    for prompt in prompt_list: 
        responses[prompt['name']] = {}
        generation_payload = sampler_defaults.copy()
        
        # TODO: Break this out into its own function for some sanity checks on the values
        if prompt.get('settings') is not None:
            for setting, default_value in sampler_defaults.items():
                generation_payload[setting] = prompt['settings'].get(setting, default_value)
        generation_payload['prompt'] = prompt['prompt']
        #print(generation_payload)
        
        # TODO: Consider breaking this out into a subfunction; splitting single gen from multigen
        for seed in seeds:
                generation_payload['sampler_seed'] = seed
                #print(json.dumps(payload))
                generation = API_GetGeneration(generation_payload)
                responses[prompt['name']][seed] = generation
                
    return responses
    # TODO: Graceful error handling - how do I want to handle it failing partway through a set?

###################################################
###################################################
# Main routine

# Get prompt lists
    # Todo: Make this a database thing too?
    # Or just keep saved?
    # That all needs thought through a bit more...
prompt_list = File_LoadPromptList(prompts_path)

# Run all selected prompt groups for currently loaded model
results = Generations(prompt_list, seeds)
    
    
# Get model name, store in variable
gen_model    = API_GetModel()
## THIS BREAKS ON HORDE, NEEDS SOLUTION
print(results)

# Now save this to the database


# (Loop back for next model)