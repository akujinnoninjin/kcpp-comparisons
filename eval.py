import json
import yaml
import os



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