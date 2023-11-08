from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.document_loaders import DataFrameLoader

class ConversationalRetrievalAgent:
    def __init__(self, dataset=None):
        self.dataset = dataset
        self.chat_history = []
        self.qa = None

    def prepare_data(self, reviews):
        data = pd.DataFrame(reviews, columns=["id", "title", "rating", "author", "content", "date"])
        data['values'] = data['title'] + ' ' + data['author'] + ' ' + data['content'] + ' ' + data['date'].astype(str)
        vector_data = data[['id', 'values']].copy()
        loader = DataFrameLoader(vector_data, page_content_column="values")
        self.dataset = loader.load()

    def create_vector_store(self):
        embeddings = OpenAIEmbeddings(openai_api_key='XXXX')
        db = Chroma.from_documents(self.dataset, embeddings)
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":2})
        return retriever

    def initialize_chain(self):
        retriever = self.create_vector_store()
        self.qa = ConversationalRetrievalChain.from_llm(OpenAI(openai_api_key='XXXX'), retriever)

    def process_query(self, query):
        result = self.qa({"question": query, "chat_history": self.chat_history})
        self.chat_history.append((query, result["answer"]))
        return result["answer"]