import tiktoken
import openai





def num_tokens_from_string(string: str,encoding_model_strings) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_model_strings)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def num_tokens_from_messages(messages,encoding_model_messages,encoding_model_strings):
    """Returns the number of tokens used by a list of messages. Compatible with  model """

    try:
        encoding = tiktoken.encoding_for_model(encoding_model_messages)
    except KeyError:
        encoding = tiktoken.get_encoding(encoding_model_strings)

    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens



def get_prompt(query: str, context: str) -> str:
    """Return the prompt with query and context."""
    return (
        f"Answer the following query.\n" +
        f"Below you will find some context that may help. Ignore it if it seems irrelevant.\n\n" +
        f"Context:\n{context}" +
        f"don't add informations from your previous knowledge, but cite and quote the sources used from the context points\n\n"+
        f"\n\nTask: {query}?"
    )


def get_message(role: str, content: str) -> dict:
    """Generate a message for OpenAI API completion."""
    return {"role": role, "content": content}





def get_context(query: str,embed_model,index,context_cap_per_query,match_min_score,context_tokens_per_query,encoding_model_messages,encoding_model_strings) -> list:
    """Generate message for OpenAI model. Add context until hitting `context_token_limit` limit. Returns prompt string."""
    openai.api_key_path = "openai_api_key.txt"
    embeddings = openai.Embedding.create(
        input=[query],
        engine=embed_model
    )

    # search the database
    vectors = embeddings['data'][0]['embedding']
    embeddings = index.query(vectors, top_k=context_cap_per_query, include_metadata=True)
    matches = embeddings['matches']

    # filter and aggregate context
    usable_context = ""
    context_count = 0
    for i in range(0, len(matches)):
        matches[i]['score']
        source = matches[i]['metadata']['source']
        if matches[i]['score'] < match_min_score:
            # skip context with low similarity score
            continue
                    
        context = matches[i]['metadata']['text']
        msg=usable_context + '\n---\n' + context
        token_count = num_tokens_from_string(string=msg,encoding_model_strings=encoding_model_strings)

        if token_count < context_tokens_per_query:
            usable_context = usable_context + '\n---\n' + context 
            context_count = context_count + 1
            

    print(f"Found {context_count} contexts for your query")

    return (usable_context,matches)



def complete(messages,chat_engine_model,temperature):
    """Query the OpenAI model. Returns the first answer. """

    res = openai.ChatCompletion.create(
        model=chat_engine_model,
        messages=messages,
        temperature=temperature
    )
    return res.choices[0].message.content.strip()