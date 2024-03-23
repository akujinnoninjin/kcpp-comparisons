
# generate(prompt, seeds, count=1)
# generate_single(prompt,seed) [alias for generate with count=1)
# generate_group(promptgroup, seeds, count=1)
# generate_batch(??) [special, tbd]
# generate_conversation(prompt, seed, count)

# Conversational/batch/single might actually be best put in the API functions
# Then this module becomes response management

DEFAULT_COUNT = 3
DEFAULT_EXCHANGES = 3

"""
def generate_group(api, promptlist, configobject, count: int = DEFAULT_COUNT):
    # Check for shared sysprompt 
    group_memory = promptlist.get('group_memory')
    if group_memory is not None:
        api.sampler_setup(memory=group_memory)
        
    # Generations for each prompt
    for prompt in promptlist['prompts']: 
        responses[prompt['name']] = {}
        
        # Check for and apply optional sampler settings
        sampler_settings = prompt.get('sampler_settings')
        if sampler_settings is not None:
            api.sampler_setup(**sampler_settings)
        
        seeds = configobject.seeds
        
        for i in range(0, min(count,len(seeds))):
            # Generate non-conversational response
            if prompt.get('conversation') is None:
                responses = api.generate(prompt['text'],seeds[i])
            # Generate a set of conversational responses
            else:
                # exchanges = prompt['conversation'].get('exchanges', DEFAULT_EXCHANGES)
                responses = generate_conversation(prompt,seeds[i]) #,exchanges)
            responses[prompt['name']][seed] = generation 
    return responses

"""
"""
def generate_conversation(prompt, seeds: list[int], exchanges=1):
    response = []
    context = prompt['text']
    
    for i in range (0, exchanges):
        new_gen = api_obj.generate(context,seed)
        response.append(new_gen)
        s1 = prompt['conversation'].get('user_string')
        s2 = prompt['conversation'].get('assistant_string')
        
        # Swap user/assistant strings 
        if i%2 == 0:
            s1, s2 = s2, s1
            
        context += s1 + new_gen
    return response


"""
"""




# Generations for each prompt

    


    # For each seed, generate an output
    for seed in config.seeds:
            generation = []
            # If this isn't a conversational prompt, generate one response
            if prompt.get('conversation') is None:
                generation = api_obj.generate(prompt['text'],seed)
                responses[prompt['name']][seed] = generation
            # Else generate a set of back-and-forth
            else:
                exchanges = prompt['conversation'].get('exchanges', 2)
                context = prompt['text']
                for i in range (0, exchanges):
                    new_gen = api_obj.generate(context,seed)
                    generation.append(new_gen)
                    context += new_gen
                # ToDo: Check this is actually how this works
                responses[prompt['name']][seed] = generation 