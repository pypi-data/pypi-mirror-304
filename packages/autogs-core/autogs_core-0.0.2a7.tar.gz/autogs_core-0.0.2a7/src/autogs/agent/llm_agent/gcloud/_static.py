import vertexai.preview.generative_models as gm

GENERATION = {
    "max_output_tokens": 2048,
    "stop_sequences": ["input:"],
    "temperature": 1,
    "top_p": 1,
}

SAFETY = {
    gm.HarmCategory.HARM_CATEGORY_HATE_SPEECH: gm.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    gm.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: gm.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    gm.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: gm.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    gm.HarmCategory.HARM_CATEGORY_HARASSMENT: gm.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}
