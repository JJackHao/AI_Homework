from transformers import pipeline
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch
import numpy as np


tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-chinese")
model = AutoModelForMaskedLM.from_pretrained("google-bert/bert-base-chinese")

def get_poem_vector(poem):
    inputs = tokenizer(poem, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs).logits
    # Average the token embeddings to get a single vector for the poem
    poem_vector = outputs.mean(dim=1)
    return poem_vector

def find_closest_word(target_vector, tokenizer, model):
    vocab = tokenizer.get_vocab()
    closest_word = None
    min_distance = float("inf")
    
    for word, idx in vocab.items():
        inputs = tokenizer(word, return_tensors="pt")
        with torch.no_grad():
            word_vector = model(**inputs).logits.mean(dim=1).numpy()
        
        distance = np.linalg.norm(target_vector - word_vector)
        
        if distance < min_distance:
            min_distance = distance
            closest_word = word
    
    return closest_word


def img2text(url):
    img_to_text_pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
    text = img_to_text_pipe(url)[0]["generated_text"]
    return text

def textGeneration_langChain(msg,type):
    """
    msg is the scenario for the story from the pic (hugging face model output);
    type is the genre of the story- Horror, Fantasy, Adventure, Comedy, Mystery, Romance
    """
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.2,
        max_tokens=200,
        timeout=None,
        max_retries=2
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert {story_type} Chinese poet. Using a simple description of a picture as the imagery in the poem, you generate {story_type} poem in Chinese with English translation to express your feelings.",
            ),
            (
                "human", 
                "{scenario_lang}"
            ),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    out_message = chain.invoke({
        "story_type" : type,
        "scenario_lang" : msg,
    })

    return out_message

def runModels_langchain(url, type):
    scenario = img2text(url)
    story = textGeneration_langChain(scenario,type)
    return([scenario,story])


def getRetriever(dir):
    """
    dir is the directory of the vector DB
    """
    embeddings_used = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorDB = Chroma(persist_directory=dir,embedding_function=embeddings_used)
    retriever = vectorDB.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    return retriever


def textGeneration_langChain_RAG(msg,type,retrieverDir):
    """
    msg is the scenario for the story from the pic (hugging face model output);
    type is the genre of the story- Horror, Fantasy, Adventure, Comedy, Mystery, Romance
    retriever is the vector DB with relevant stories from txt version of 
        stories dataset from Hugging face - https://huggingface.co/datasets/ShehryarAzhar/stories
    """
    llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2,
            max_tokens=200,
            timeout=None,
            max_retries=2
        )

    system_prompt = (
        "You are an expert {story_type} Chinese poet. " 
        "Use the following pieces of retrieved context to generate {story_type} poem in Chinese with English translation. "
        "Using a simple description of a picture as the imagery in the poem, you generate {story_type} poem"
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{scenario_lang}"),
        ]
    )

    rag_chain = prompt | llm | StrOutputParser()

    retriever = getRetriever(retrieverDir)

    out_message = rag_chain.invoke({
            "story_type" : type,
            "context":retriever,
            "scenario_lang" : msg,
        })
    
    return out_message

def runModels_langchain_RAG(url, type, retrieverDir):
    scenario = img2text(url)
    story = textGeneration_langChain_RAG(scenario,type,retrieverDir)
    # print(story)
    return([scenario,story])