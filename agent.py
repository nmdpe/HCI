from langchain_community.llms import Tongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ChatMessageHistory
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_core.prompts import MessagesPlaceholder

loader=TextLoader('data/aim.txt')
aim_docs=loader.load()
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
aim_docs=text_splitter.split_documents(aim_docs)
loader=TextLoader('data/spray.txt')
spray_docs=loader.load()
spray_docs=text_splitter.split_documents(spray_docs)
loader=TextLoader('data/weapon.txt')
weapon_docs=loader.load()
weapon_docs=text_splitter.split_documents(weapon_docs)
loader=TextLoader('data/demo.txt')
demo_docs=loader.load()
demo_docs=text_splitter.split_documents(demo_docs)
loader=TextLoader('data/mental.txt')
mental_docs=loader.load()
mental_docs=text_splitter.split_documents(mental_docs)


embedding=SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2') #换自己路径
vector_store=Chroma.from_documents(documents=aim_docs+spray_docs+weapon_docs+mental_docs,embedding=embedding)
retriever=vector_store.as_retriever(
    search_type='similarity_score_threshold',
    search_kwargs={'score_threshold': 0.15, 'k': 3}
)

#print('relavant_docs: ',retriever.invoke('spray'))

#llm=Tongyi(model_name='qwen1.5-32b-chat')
llm=Tongyi()
chat_search=Tongyi()

chat_history=ChatMessageHistory()

c2e={'压枪':'spray','扫射':'spray','扫射转移':'spray transfer'}; #可以自己添加

translate_prompt='''What's more, there are some words translations for reference: '''

for c,e in c2e.items():
    translate_prompt+=f''' '{c}' means '{e}';'''

#print(translate_prompt)

def get_response(user_input,vision=''):
    chat_history.add_user_message(user_input)
    query_transform_prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="messages"),
        (
            "user",
            f"Given the above conversation, generate a search query to look up in order to get information relevant to the conversation. If the query contains abbreviations or other content, do not use knowledge to explain the abbreviations. This search query must be completely English. The query search should be very short, only containing a few key words, no more than 10 words.",
        ),
    ]
    )
    query_transformation_chain = query_transform_prompt | chat_search | StrOutputParser()
    search_query = query_transformation_chain.invoke(
        {
            "messages": chat_history.messages,
        }
    )
    print("query: ",search_query)
    docs = retriever.invoke(search_query)

    knowledge = ''
    for doc in docs:
        knowledge += doc.page_content + '\n'

    print(knowledge)

    #生成聊天历史
    chatHistory = ''
    for i in range(len(chat_history.messages)-1):
        s = chat_history.messages[i]
        if s.type == 'human':
            chatHistory += 'user:' + s.content + '\n'
        elif s.type == 'ai':
            chatHistory += 'Elon Musk(you)' +':' + s.content + '\n'

    # 使用工具
    #vision = ''
    #vision = get_vision(user_input)

    # 生成User Prompt
    from prompt import UserPrompt,SystemPrompt
    agent_input = UserPrompt(worldInfo=translate_prompt,
                            knowledge=knowledge,
                            chatHistory=chatHistory,
                            vision=vision,
                            question=user_input)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SystemPrompt),
        ("user", "{input}")
    ])

    # 调用LLM
    chain = prompt | llm | StrOutputParser()
    #print(agent_input)
    result = chain.invoke({"input": agent_input})

    #存储对话历史
    chat_history.add_ai_message(result)

    #print(result)
    return result

if __name__=="__main__":
    while True:
        user_input=input("please input: ")
        print('LLM:',get_response(user_input))

