import os
import openai
openai.organization = "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" #"org-Z4h3pUophf0Rjw2q8YphIYYL"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()