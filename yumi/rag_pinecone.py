from typing import List

# from langchain.schema import Document
# from langchain_community.document_loaders import PyMuPDFLoader
# from langchain_openai import OpenAIEmbeddings
# from langchain_pinecone import PineconeVectorStore

index_name = "yumi-test-1"

# embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")


# def vectorstore(
#     index_name: str = index_name, embeddings_model: OpenAIEmbeddings = embeddings_model
# ) -> PineconeVectorStore:
#     return PineconeVectorStore(
#         embedding=embeddings_model,
#         index_name=index_name,
#     )


# async def basic_retriever(
#     query: str,
#     index_name: str = index_name,
# ) -> List[Document]:
#     docs = await vectorstore(index_name).asimilarity_search(query=query)
#     documents = [doc.page_content for doc in docs]
#     return documents


async def load_pdfs_to_pinecone(attachments: List[str], index_name: str = index_name):
    for attachment in attachments:
        await attachment.save(f"received_files/{attachment.filename}")
    #     loader = PyMuPDFLoader(f"received_files/{attachment.filename}")
    #     data = loader.load()
    #     vectorstore(index_name=index_name).add_documents(data)
    # return "Documents added to Pinecone"
    pass
