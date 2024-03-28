
import dotenv
#from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import List
from datasets import load_dataset
import os.path
from backend.src.langchain.CsvLoader import CSVLoader
from backend.src.langchain.path import PAPERS_CSV_PATH,PAPERS_CHROMA_PATH,DATASET_PATH

def load_dataset_hugging_face(src_path,dest_path):
    if os.path.isfile(dest_path)==False:
        dataset = load_dataset(src_path)
        dataset['train'].to_csv(dest_path)
    

dotenv.load_dotenv()
load_dataset_hugging_face(DATASET_PATH,PAPERS_CSV_PATH)

loader = CSVLoader(file_path=PAPERS_CSV_PATH, source_column='abstract',encoding="utf8"
                   ,metadata_columns='title'
                   )

papers = loader.load()


papers_vector_db = Chroma.from_documents(
    papers, OpenAIEmbeddings(), persist_directory=PAPERS_CHROMA_PATH
)