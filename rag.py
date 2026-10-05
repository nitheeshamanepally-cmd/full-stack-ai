from sentence_transformers import SentenceTransformer
import chromadb, ollama, streamlit as st
#model = SentenceTransformer("all-MiniLM-L6-v2")
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")
model = load_model()
st.title("Chat Assistant!! 👾")
if "messages" not in st.session_state:
    st.session_state.messages=[]
with st.sidebar:
    personalities={
            "Kid": "Give the anwers like you are explaining to a 5 year old kid .Give the answer in 5 lines only.",
            "Professor":"You are an IIT Professor. Explain the topics using correct termilogy.Give the answer in 2-3 lines only.",
            "young dumb":"Give the answers like crazy kid and intresting way.Give the anwers in 5 lines"
        }
    personality=st.selectbox("select a personality 🥸", personalities.keys())
    top_k=st.slider("Select no of top results",min_value=1,max_value=5,value=3)
    uploaded_file = st.file_uploader("Upload a file")
    if uploaded_file:
        text=uploaded_file.read().decode("utf-8")
        with st.expander("Preview"):
            st.text(text)

# chunking
        chunks = []
        chunk_size = 100
        chunk_overlap = 20
        step = chunk_size - chunk_overlap
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i+chunk_size]
            chunks.append(chunk)
        # for i in range(len(chunks)):
        # print(f"chunk {i + 1} -> {chunks[i]}")
        # Embedding
        embeddings = model.encode(chunks)
        # print(embeddings[0])
        # print(embeddings.shape)

        # Vector DB
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="My_Documents")
        ids = []
        for i in range(len(chunks)):
            ids.append(f"{uploaded_file.name}_{i}")

        collection.add(
            documents=chunks,
            ids=ids,
            embeddings=embeddings.tolist()

        )
        st.subheader("Chat options")
        with st.container():
            if st.button("Clear chat"):
                 st.session_state.messages=[]
                 st.success("Chat history dleted..")
        with st.expander("Chat history"):
             for msg in st.session_state.messages:
                  with st.chat_message(msg["role"]):
                       st.write(msg["content"])
                  
        # results = collection.get()
        # chunk1 = collection.get(ids=['sample.txt_0'])
        # print(chunk1)


# Query Phase
question = st.chat_input("Ask a question: ")
if question:
        if uploaded_file:
            st.write(question)
            q_embedding = model.encode(question)
            results = collection.query(
                query_embeddings=[q_embedding.tolist()],
                n_results=top_k
            )
            retrieved_chunks = (results['documents'][0])
            retrieved_ids = results["ids"][0]
            #for i in range(len(results['documents'][0])):
            #    print(f"chunk {i + 1}")
            #   print(results['documents'][0][i])
            context = '\n'.join(retrieved_chunks)

            # Prompting phase
            prompt = f'''
            Answer the question using the context given below only.
            Question: {question}
            Context: {context}
            Answer:
            '''
            response = ollama.chat(
                model = "llama3.2:3b",
                messages = [{"role":"user",
                "content": prompt}]
            )
            st.write(response["message"]["content"])
        else:
            with st.chat_message("user"):
                    st.write("user: ",question)
            
            st.session_state.messages.append(
                {"role":"user",
                "content":question}
            )
            with st.spinner("thinking.... 🤔"):
                response =ollama.chat(
                        model="llama3.2:3b",
                        messages=[{ 
                            "role": "system","content":personalities[personality]
                            }] + st.session_state.messages
                    )
            
            st.session_state.messages.append(
                    {"role":"assistant",
                     "content":response["message"]["content"]
                    }
                )
            with st.chat_message("assistant"):
                st.write("AI:",response["message"]["content"])
            