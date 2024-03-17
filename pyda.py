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
    #"prompt": prompt['prompt']
    quiet:                   bool = Field(default=True)
    stop_sequence:      List[str] = ["You:", "\nYou ", "\n: "]
    use_default_badwordsids: bool = Field(default=False)
    #"sampler_seed": seed
    
    @field_validator("rep_pen_range")
    def rep_pen_range_must_be_smaller_than_context(cls, rep_pen_range, config) -> int:
        if rep_pen_range > config.data['max_context_length']:
            rep_pen_range = config.data['max_context_length']
        return rep_pen_range

try:
    set = SamplerSettings(rep_pen_range="-2")
    print(set.rep_pen_range)
except ValidationError as e:
    print(e)