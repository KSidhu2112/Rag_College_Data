try:
    from langchain_mongodb import MongoDBChatMessageHistory
    print("Import successful: from langchain_mongodb import MongoDBChatMessageHistory")
except ImportError:
    try:
        from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
        print("Import successful: from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory")
    except ImportError as e:
        print(f"Import failed: {e}")
