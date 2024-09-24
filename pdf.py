# We will be using these PDF loaders but you can check out other loaded documents
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from dotenv import load_dotenv

load_dotenv()

# This is the name of the report which should be in the directory
# You can download the precise PDF I am using from here https://www.pc.gov.pk/uploads/archives/PSDP_2023-24.pdf
name = 'Ammar.pdf'

# This loader uses PyMuPDF
loader_py = PyMuPDFLoader(name)

#This loader uses Unstructured
#loader_un = UnstructuredLoader(name)

# Storing the loaded documents as langChain Document object
pages_py = loader_py.load()

#pages_un = loader_un.load()

# text splitter

text_splitter = CharacterTextSplitter(
    # shows how to seperate
    separator="\n",
    # Shows the document token length
    chunk_size=1000,
    # How much overlap should exist between documents
    chunk_overlap=150,
    # How to measure length
    length_function=len
)

# Applying the splitter
docs = text_splitter.split_documents(pages_py)

# a simple function that removes \n newline from the content
def remove_ws(d):
    text = d.page_content.replace('\n','')
    d.page_content = text
    return d

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# applied on the docs
docs = [remove_ws(d) for d in docs]

print(f"Going to add {len(docs)} to Pinecone")
PineconeVectorStore.from_documents(docs, embeddings, index_name="pdf")
print("****Loading to vectorstore done ***")