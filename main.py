import pinecone
import os
from dotenv import load_dotenv
import os
import webbrowser
import bs4
import os
from help_functions import get_prompt, get_message, get_context, num_tokens_from_messages, num_tokens_from_string,complete






# Define parameters
# Pinecone database name, number of matched to retrieve
# cutoff similarity score, and how much tokens as context
index_name = 'supportagentdb'
context_cap_per_query = 30
match_min_score = 0.75
context_tokens_per_query = 3000

# OpenAI LLM model parameters
chat_engine_model = "gpt-3.5-turbo"
max_tokens_model = 4096
temperature = 0.2 
embed_model = "text-embedding-ada-002"
encoding_model_messages = "gpt-3.5-turbo-0301"
encoding_model_strings = "cl100k_base"



# Connect with Pinecone db and index
# Charger le fichier .env
load_dotenv('env-example')
api_key = os.getenv("PINECONE_API_KEY")
env = os.getenv("PINECONE_ENVIRONMENT")
openIA_key=os.getenv("OPENAI_API_KEY")
pinecone.init(api_key=api_key, environment=env)
index = pinecone.Index(index_name)






def test(query):
    context,metadata = get_context(query=query,embed_model=embed_model,index=index,context_cap_per_query=context_cap_per_query,match_min_score=match_min_score,context_tokens_per_query=context_tokens_per_query,encoding_model_messages=encoding_model_messages,encoding_model_strings=encoding_model_strings)
    prompt = get_prompt(query, context)
    # initialize messages list to send to OpenAI API
    messages = []
    messages.append(get_message('user', prompt))

    if num_tokens_from_messages(messages=messages,encoding_model_messages=encoding_model_messages,encoding_model_strings=encoding_model_strings) >= max_tokens_model:
        raise Exception('Model token size limit reached') 

    print("Working on your query... ")
    answer = complete(messages=messages,chat_engine_model=chat_engine_model,temperature=temperature)

    with open("index.html") as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt)
        h1_elements = soup.find_all('h1', {'class': 'cmp-title__text'})
        span_elements =  soup.find_all("span",{"class":"sc-navy font--light text-h4"}) 
        if len(h1_elements)>0:
            # Change the text of the h1 element
            h1_elements[0].string.replace_with(query) 
        if len(span_elements) >0:
            span_elements[0].string.replace_with(answer)
            
        i=0
        
        for litag in soup.find_all('li',{"class":"icon-002-arrow-down"}):
            litag.find("a")["href"]=metadata[i]["metadata"]["source"]
            litag.find("a").string.replace_with(metadata[i]["metadata"]["title"])
            i+=1
        
        div = soup.find("div",{"id":"text-2c9dfc4455"})
        div.find("p").string.replace_with("\n".join([metadata[i]["metadata"]["text"] for i in range(4)]))
    with open("existing_file.html", "w") as outf:
        outf.write(str(soup))

    webbrowser.open("file:/Users/amirbraham/Desktop/LauzHack2/existing_file.html",new=2)
    