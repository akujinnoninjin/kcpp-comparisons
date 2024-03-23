from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import List
from typing_extensions import Annotated

class SamplerSettings(BaseModel):
    max_context_length:       int = Field(default=1600, gt=0)
    max_length:               int = Field(default=500, gt=0)
    rep_pen:                float = Field(default=1, gt=0)
    temperature:            float = Field(default=1, gt=0)
    smoothing_factor:       float = Field(default=0.25)
    top_p:                  float = Field(default=1, ge=0, le=1)
    top_k:                  float = Field(default=0, ge=0)
    top_a:                  float = Field(default=0, ge=0)
    typical:                float = Field(default=1, ge=0)
    tfs:                    float = Field(default=1, ge=0)
    rep_pen_range:            int = Field(default=320, ge=0)
    rep_pen_slope:          float = Field(default=0.7)
    sampler_order: List[Annotated[int, Field(ge=0,le=6)]] = [6, 0, 1, 3, 4, 2, 5]
    memory:                   str = Field(default="")
    min_p:                  float = Field(default=0, ge=0)
    dynatemp_range:         float = Field(default=0, ge=0)
    presence_penalty:       float = Field(default=0)
    #logit_bias: {}
    prompt:                   str = Field(default="")
    quiet:                   bool = Field(default=True)
    stop_sequence:      List[str] = ["You:", "\nYou ", "\n: "]
    use_default_badwordsids: bool = Field(default=False)
    sampler_seed:             int = Field(default=-1, ge=-1) #, lt=99999999)
    
    @field_validator("rep_pen_range")
    def rep_pen_range_must_be_smaller_than_context(cls, rep_pen_range, config) -> int:
        if rep_pen_range > config.data['max_context_length']:
            rep_pen_range = config.data['max_context_length']
        return rep_pen_range

#class RunConfig():
seeds = [8675309, 12345678] #, 314159265, 181811]

#If URL specified, assume only using hosted model
api_url = "http://10.10.100.112:5001/api/v1/" #127.0.0.1:5001" #TODO: Read from command line args

# Assume input prompt file is in same folder, prompts.yaml
prompts_path = ".\prompts"

#If path is specified, assume loading model
#kcpp_path = "./koboldcpp-main/koboldcpp/koboldcpp.py"
# --model single model
# --models model folder
# --numactl 24 numactl threads, assumed 0 if not specified
# --usecublas #assume 200 offload layers for now; difficult to specify partials 
# --useblas toggle`
    
    
    
# try:
    # set = SamplerSettings(rep_pen_range="-2")
    # print(set.rep_pen_range)
# except ValidationError as e:
    # print(e)