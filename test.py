import PromptEval.api as prompt_api
import PromptEval.filehandlers as file
import PromptEval.config as config

api_obj = prompt_api.get_API(type="kcpp", url="target")    
    
responses = {}

promptlist = file.load_prompt_group(config.prompts_path, 'default')

# Check for shared sysprompt 
group_memory = promptlist.get('group_memory')
if group_memory is not None:
    api_obj.sampler_setup(memory=group_memory)

# Generations for each prompt
for prompt in promptlist['prompts']: 
    responses[prompt['name']] = {}
    
    # Check for and apply optional sampler settings
    sampler_settings = prompt.get('sampler_settings')
    if sampler_settings is not None:
        api_obj.sampler_setup(**sampler_settings)

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
            
print(responses)
# print(api_obj.sampler_setup(top_p=52052))