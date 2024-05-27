from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

try:
    # 初始化 embeddings 对象
    embeddings = HuggingFaceEmbeddings(model_name='llm/shareData/text2vec-base-chinese')
    ddb = Chroma(persist_directory="llm/Chromadb", embedding_function=embeddings)
    print("向量库启动成功！")
except Exception as e:
    print(f"出现异常：{e}")


def save_to_memory(file_path):
    # 加载单文本
    loader = TextLoader(file_path)
    # 将文本转成 Document 对象
    document = loader.load()
    #print(document)
    # 初始化加载器
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)  # 默认使用\n\n做分割
    # 切割加载的 document
    split_docs = text_splitter.split_documents(document)
    #print(split_docs)
    # 将 document 计算 embedding 向量信息并临时存入 Chroma 向量数据库，用于后续匹配查询
    db = Chroma.from_documents(split_docs, embeddings, persist_directory="llm/Chromadb")
    # 持久化数据
    db.persist()
# 文本检索
def text_search(query):
    docs = ddb.similarity_search(query)
    return docs[0].page_content
    #print('文本检索:%s' % query)
    #print(docs[0].page_content)

# 向量检索
def vector_search(query):
    embedding_vector = embeddings.embed_query(query)
    docs = ddb.similarity_search_by_vector(embedding_vector)
    return [doc.page_content for doc in docs[:4]] 
    #print('向量检索:%s' % embedding_vector[0:8])
    #print(docs[0].page_content)

# 清空向量数据库
def clear_database():
    try:
        ddb.clear()
        print("向量数据库已成功清空！")
    except Exception as e:
        print(f"清空向量数据库时出现异常：{e}")


if __name__ == '__main__':
    #save_to_memory()
    # 保存文本到内存
    #save_to_memory()
    # 文本检索
    #print(text_search("你的名字是什么？"))
    # 向量检索
    while  True:
        question = input("请输入问题：")
        if question == "exit":
            break
        print(vector_search(question))