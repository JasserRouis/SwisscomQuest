import pinecone
import openai
import os
import json


# Connect to Pinecone
api_key = os.getenv("PINECONE_API_KEY")
env = os.getenv("PINECONE_ENVIRONMENT")
index_name = "supportagentdb"
pinecone.init(api_key="0e08aab9-a9d8-438f-8b28-d429c325e131", environment="gcp-starter")

#pinecone.create_index("supportagentdb", dimension=1536)

index = pinecone.Index("supportagentdb")

# Load data from JSON files that were previously generated
for c in range(0,10):
    for i in range(1, 9):
        json_file_path = f"swisscom_split/json_part_{c}_{i}.json"
        with open(json_file_path, "r") as file:
            data = json.load(file)
        # Upload data to the Pinecone index
        index.upsert(data)
        print(f"file {c}_{i} uploaded")
