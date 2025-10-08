# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the vLLM project
from openai import OpenAI
from config import *
from util.hallucinations_util import *
import json


# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = VLLM_KEY
openai_api_base = "http" + "://" + VLLM_ADDR + ":" + VLLM_PORT + VLLM_PATH
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

def sync_openai(f):
    transcription = client.audio.transcriptions.create(
        file=f,
        model=VLLM_MODEL_NAME,
        response_format="json",
        language=VLLM_DEFAULT_LANG,
        temperature=0.0,
        # Additional sampling params not provided by OpenAI API.
        extra_body=dict(
            seed=4419,
            repetition_penalty=1.3,
        ),
    )
    cleaned_transcript = remove_hallucinations(transcription.text)

    print(cleaned_transcript)

    if HALLUCINATION_COLLECTOR:
        if (transcription.text not in hallucinations):
            hallucinations.append(transcription.text)
            with open("util/hallucinations.json", "w") as json_file:
                json.dump(hallucinations, json_file, indent=4)
        #end of collect hallucinations

    return cleaned_transcript  
     
if __name__ == "__main__":
  sync_openai()