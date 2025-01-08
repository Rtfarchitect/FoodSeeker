import time
import streamlit as st
import pandas as pd
import pydeck as pdk
from langchain_openai import OpenAI
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS

import os
from functions import get_current_location, find_places_nearby, extract_conditions_with_ai, search_vectorstore, filter_results_with_ai
from dotenv import load_dotenv
load_dotenv()



st.title("Food Seeker!")




col1, col2 = st.columns([1, 2])

with col2:
# Create a DataFrame with the user's location
    latitude, longitude = get_current_location()
    places = find_places_nearby(latitude, longitude, radius_km=5, keyword="restaurant")
    for i in places:
        i["lon"] = float(i["lon"])
        i["lat"] = float(i["lat"])

    location_data = pd.DataFrame({
        'lat': [latitude],
        'lon': [longitude]
    })

    # Map view settings
    view_state = pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=12,
        pitch=50
    )

    # Create a layer for the map
    layer1 = pdk.Layer(
        'ScatterplotLayer',
        data=location_data,
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 160]',
        get_radius=150
    )

    layer2 = pdk.Layer(
        'ScatterplotLayer',
        data=places,
        get_position='[lon, lat]',
        get_color='[30,200, 0, 160]',
        get_radius=50
    )
    # Render the map
    st.pydeck_chart(pdk.Deck(
        initial_view_state=view_state,
        layers=[layer1, layer2]
    ))

urls=[
    'https://www.ubereats.com/ca-fr/brand-city/montreal-qc/poulet-rouge?srsltid=AfmBOor9Gz-n3ksZ5NFJ9zRRJlTrDzxtximoYKsYYQlP6EVsWzlGNnMS',
    'https://www.ubereats.com/ca/store/pizzeria-napoletana/x4Zp9IKwSNGNgqIz2gCI-w?srsltid=AfmBOoqLYZb1IvIigYijDf1XZhmQnrX8YXj2KaPDsat7NOX4agTGm3zP',
    'https://www.ubereats.com/ca/brand-city/montreal-qc/dominos?srsltid=AfmBOoqaRKsDFKCc-Je-POpmsWJ1t_AWwplON9psd-2msuWN31RZ-apn'

]

names = ["poulet rouge", "pizzeria-napoletana", "domino"]


class Restaurant:
    def __init__(self, name, location, url):
        """Initialize a Restaurant object with name, location, and url."""
        self.name = name
        self.location = location
        self.url = url

restaurants = [Restaurant(names[i], (0,0), urls[i]) for i in range(len(urls))]
dictionary = {}
for i in range(len(urls)):
    dictionary[urls[i]] = names[i]


loader = UnstructuredURLLoader(urls=urls)
data = loader.load()



text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
docs = text_splitter.split_documents(data)

for i in docs:
  i.metadata['restaurant_name'] = dictionary[i.metadata['source']]

all_splits = docs


index_path = "faiss_index"

if not os.path.exists(index_path):
    # If not saved, create and save the index
    vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())
    vectorstore.save_local(index_path)
    print("FAISS index created and saved.")
else:
    vectorstore = FAISS.load_local(index_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    print("FAISS index already exists.")







# vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
print("hello")

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})



with col1:
    query = st.chat_input("Ask me anything: ") 
    if query:
    
        conditions = extract_conditions_with_ai(query)


        results = search_vectorstore(conditions, vectorstore, top_k=10)


        filtered_results = filter_results_with_ai(results, conditions)
        print(filtered_results)
        for item in filtered_results:
            st.subheader(item["food_name"])
            st.markdown(f"**Price:** {item['price']}")
            st.markdown(f"**Restaurant:** {item['restaurant_name']}")
            st.markdown(f"**Description:** {item['text']}")
            if item["url"] != "N/A":
                st.markdown(f"[More Info]({item['url']})")
            st.markdown("---")  # Divider
        # st.write(filtered_results)
























    # with col3:
    #     for item in filtered_results:
    #         st.subheader(item["food_name"])
    #         st.markdown(f"**Price:** {item['price']}")
    #         st.markdown(f"**Restaurant:** {item['restaurant_name']}")
    #         st.markdown(f"**Description:** {item['text']}")
    #         if item["url"] != "N/A":
    #             st.markdown(f"[More Info]({item['url']})")
    #         st.markdown("---")  # Divider









# llm = OpenAI(temperature=0.4, max_tokens=500)






# prompt = query

# system_prompt = (
#     "You are an assistant for question-answering tasks. "
#     "Use the following pieces of retrieved context to answer "
#     "the question. If you don't know the answer, say that you "
#     "don't know. Use three sentences maximum and keep the "
#     "answer concise."
#     "\n\n"
#     "{context}"
# )


# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         ("human", "{input}"),
#     ]
# )


