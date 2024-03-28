import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/paper-rag-agent")

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot integrates with a 
        [LangChain](https://python.langchain.com/docs/get_started/introduction)
        agent to address queries related to Machine Learning research papers. 
       It employs a Retrieval-Augmented Generation (RAG) approach, 
       which leverages targeted data retrieval to enrich the language model's responses 
       with up-to-date and relevant information.
        """
    )

    st.header("Example Questions")
    st.markdown("- List papers that discuss the use of reinforcement learning in autonomous driving systems?")
    st.markdown("- Can you provide a summary of the paper titled 'Attention is All You Need' and its impact on the field?")
    st.markdown("- Which papers in the dataset have been co-authored by Geoffrey Hinton, and what topics do they cover?")
    st.markdown("- What are the main contributions of the 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding' paper?")
    st.markdown(
        "What are the key algorithms proposed in recent papers for improving recommendation systems?"
    )
    st.markdown("- Are there any case studies in the dataset focusing on machine learning applications in precision medicine?")
    st.markdown(
        "- How does the approach in 'Generative Adversarial Networks' compare to that in 'Variational Autoencoders' according to recent papers?"
    )
    st.markdown("- What critiques or discussions exist around the methodology used in the 'Deep Residual Learning for Image Recognition' paper?")

    st.markdown("- Can you list recent publications from the dataset that resulted from collaborations between academia and industry?")
    st.markdown("- Can you provide an overview of review papers in the dataset covering advances in deep learning over the last decade?")

st.title("ML Research Papers Chatbot")
st.info(
    "Ask me questions about current ML research papers"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Searching for an answer..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]

        else:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )