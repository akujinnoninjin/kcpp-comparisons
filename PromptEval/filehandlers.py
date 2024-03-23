#from json import load, dump
import yaml
from os import path

def _load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load_all(file)
            return list(yaml_data)[0] # Only keeps the first entry in a multi document yaml
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file '{file_path}': {exc}")
    # TODO: Handle errors more gracefully

def load_prompt_group(prompt_dir, prompt_group):
    file_path = path.join(prompt_dir, prompt_group) + '.yaml'
    prompt_list = _load_yaml(file_path)
    if not prompt_list:
        print(f"Error loading YAML file: {file_path}")
        return None
    else:
        return prompt_list
    # TODO: Handle errors more gracefully
    
# def prompts_to_json(file_path, new_data):
    # existing_data = []
    # # Todo: replace this with a try, and a silenced 'doesn't exist' error?
        # # To remove the need for the os.path import
    # if path.exists(file_path):
        # # If the file exists, read its content
        # with open(file_path, "r") as file:
            # existing_data = load(file)
        
        # new_model = next(iter(new_data))
        
        # existing_model = existing_data.get(new_model)
        
        # if existing_model == None:
            # print("New model! Append whole thing!")
        # else:
            # print("Existing model! Checking prompts!")
            # for newprompt in new_data[new_model]['prompts']:
                # existing_prompt = existing_data[new_model]['prompts'].get(newprompt)
                # if existing_prompt == None:
                    # print("New Prompt! Append it to the section!")
                # else:
                    # print("Existing Prompt! Checking seeds!")
                    # for newseed in new_data[new_model]['prompts'][newprompt]['seeds']:
                        # print(newseed)
                        # existing_response = existing_data[new_model]['prompts'][newprompt]['seeds'].get(str(newseed))
                        # if existing_response == None:
                            # print("New Seed! Append it to the section!")
                        # else:
                            # print("Existing Seed! Skip!")
    # else:
        # existing_data = new_data

    # # Write the updated data to the JSON file
    # with open(file_path, "w") as file:
        # dump(existing_data, file, indent=4)

    # print("Outputs have been been written to", file_path)
    # return None