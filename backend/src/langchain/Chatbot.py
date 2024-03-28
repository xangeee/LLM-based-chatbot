import dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents import (
    create_openai_functions_agent,
    Tool,
    AgentExecutor,
)
from langchain import hub
from backend.src.langchain.tools import get_current_temperature
from backend.src.langchain.config import paper_template
from backend.src.langchain.path import PAPERS_CHROMA_PATH
import backend.src.langchain.config as config

dotenv.load_dotenv()
K=10

class Chatbot:
    papers_retriever=None
    paper_chain=None
    tools=[]
    paper_agent_executor=None
    
    def __init__(self):

        chat_model = ChatOpenAI(model=config.OPENAI_MODEL, temperature=0)
        output_parser = StrOutputParser()
        
        paper_prompt_template=self.createPromptTemplate()
        self.initRetriever(K)
        self.createChain(paper_prompt_template,chat_model,output_parser)
        self.createTools()
        self.initAgentExecutor()
        
    def createPromptTemplate(self):
        paper_system_prompt = SystemMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=["context"],
                    template=paper_template,
                )
            )

        paper_human_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["question"],
                template="{question}",
            )
        )
        messages = [paper_system_prompt, paper_human_prompt]

        paper_prompt_template = ChatPromptTemplate(
            input_variables=["context", "question"],
            messages=messages,
        )
        
        return paper_prompt_template
        
    def initRetriever(self,K):
          
        paper_vector_db = Chroma(
            persist_directory=PAPERS_CHROMA_PATH,
            embedding_function=OpenAIEmbeddings()
        )

        self.papers_retriever  = paper_vector_db.as_retriever(k=K)

        
    
    def createChain(self,paper_prompt_template,chat_model,output_parser):
        # the | symbol, which is used to chain review_prompt_template and chat_model together
        self.paper_chain = ( {"context": self.papers_retriever, "question": RunnablePassthrough()}
            |paper_prompt_template | chat_model | output_parser)
    
    def createTools(self): 
        
        self.tools = [
            Tool(
                name="Papers",
                func=self.paper_chain.invoke,
                description=config.TOOL_PAPER,
            ),
            Tool(
                name="Cities",
                func=get_current_temperature,
                description=config.TOOL_CITY,
            ),
        ]

    
    def initAgentExecutor(self):
        paper_agent_prompt = hub.pull(config.PAPER_AGENT_PROMPT)
        
        agent_chat_model = ChatOpenAI(
            model=config.AGENT_CHAT_MODEL,
            temperature=0,
        )

        paper_agent = create_openai_functions_agent(
            llm=agent_chat_model,
            prompt=paper_agent_prompt,
            tools=self.tools,
        )

        self.paper_agent_executor = AgentExecutor(
            agent=paper_agent,
            tools=self.tools,
            return_intermediate_steps=True,
            verbose=True,
        )

