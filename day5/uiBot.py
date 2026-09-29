import ollama
import streamlit as st
st.title(":rainbow[***Welcome to chatBot AI!! 💭***]")
with st.sidebar:
    personalities={
        "Kid": "Give the anwers like you are explaining to a 5 year old kid .Give the answer in 5 lines only.",
        "Professor":"You are an IIT Professor. Explain the topics using correct termilogy.Give the answer in 2-3 lines only.",
        "young dumb":"Give the answers like crazy kid and intresting way.Give the anwers in 5 lines"
    }
    personality=st.selectbox("select a personality 🥸", personalities.keys())
    if st.button("Clear Chat 🧹"):
        st.session_state.messesages=[]
        st.success("Chat cleared successfully")
    st.header("Chat settings 💭")
    uploaded_file = st.file_uploader("upload a file...📁")
    if uploaded_file:
        st.write("file uploaded successfully... ✅")
        with st.expander("Preview"):
            context=uploaded_file.read().decode("utf-8")
            st.text(context)
if "messages" not in st.session_state:
    st.session_state.messages=[]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
question =st.chat_input("you:")
if question:
    with st.chat_message("user"):
        st.write("user: ",question)

st.session_state.messages.append(
    {"role":"user",
    "content":question}
)
if st.button("Summarize !! 🫨"):
            st.session_state.messesages=[]
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
