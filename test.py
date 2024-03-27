import langchain

langchain.verbose = True
# langchain.debug = True

# OpenAI LLM
import os
from langchain.llms import OpenAI

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
llm_openai = OpenAI(openai_api_key=OPENAI_API_KEY)

from langchain.llms.base import LLM
from typing import Any
from pydantic import root_validator, Field
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LocalLLM(LLM):
    model_name: str = Field('', alias='model_name')
    model: Any = None
    tokenizer: Any = None
    last_query: str = ''
    last_response: str = ''

    @root_validator()
    def validate_environment(cls, values: dict) -> dict:
        model, tokenizer = huggingface_api.load_model(
            values['model_name'],
            device='cuda',
            num_gpus=1,
            max_gpu_memory=None,
            load_8bit=False,
            cpu_offloading=False,
            revision='main',
            debug=True,
        )
        values['model'] = model
        values['tokenizer'] = tokenizer
        return values

    @property
    def _llm_type(self):
        return "vicuna"

    def _call(self, prompt, stop=None, run_manager=None, temperature=0.7):
        self.last_query = prompt

        input_ids = self.tokenizer([prompt]).input_ids
        output_ids = self.model.generate(
            torch.as_tensor(input_ids).cuda(),
            do_sample=True,
            temperature=temperature,
            repetition_penalty=1.0,
            max_new_tokens=512,
        )
        # Convert output
        output_ids = output_ids[0] if self.model.config.is_encoder_decoder else output_ids[0][len(input_ids[0]):]
        self.last_response = self.tokenizer.decode(output_ids,
                                                   skip_special_tokens=True,
                                                   spaces_between_special_tokens=False)
        return self.last_response


llm_custom = LocalLLM(model_name='lmsys/vicuna-13b-v1.3')