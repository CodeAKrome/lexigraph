import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.inference.ai.azure.com"
model_name = "Llama-3.2-90B-Vision-Instruct"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

with open("dotfile2.txt", "r") as f:
    system = f.read()

with open("rag.txt", "r") as f:
    rag = f.read()

# response = client.complete(
#     messages=[
#         SystemMessage(content="You are a helpful assistant."),
#         UserMessage(content="What is the capital of France?"),
#     ],
#     temperature=1.0,
#     top_p=1.0,
#     max_tokens=1000,
#     model=model_name
# )

response = client.complete(
    messages=[
        SystemMessage(content=system),
        UserMessage(
            content="Create a Knowledge Graph in dot file format of the following articles. Assign the entity name to the dot label like 'Jimmy Dean' and the type of entity as type like 'PERSON' for example [label=\"Jimmy Dean\", type=\"PERSON\"]\n"
            + rag
        ),
    ],
    temperature=1.0,
    top_p=1.0,
    max_tokens=2000,
    model=model_name,
)

print(response.choices[0].message.content)
