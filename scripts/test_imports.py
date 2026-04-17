try:
    from langchain.chains import ConversationalRetrievalChain
    print("Success: ConversationalRetrievalChain")
except ImportError as e:
    print(f"Error: ConversationalRetrievalChain: {e}")

try:
    from langchain.memory import ConversationBufferMemory
    print("Success: ConversationBufferMemory")
except ImportError as e:
    print(f"Error: ConversationBufferMemory: {e}")

try:
    from langchain.prompts import PromptTemplate
    print("Success: PromptTemplate")
except ImportError as e:
    print(f"Error: PromptTemplate: {e}")

try:
    from langchain_community.vectorstores import FAISS
    print("Success: FAISS")
except ImportError as e:
    print(f"Error: FAISS: {e}")

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
    print("Success: Google AI")
except ImportError as e:
    print(f"Error: Google AI: {e}")
