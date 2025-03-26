import streamlit as st
from utils import word_generation,tools
import os

llm = tools.define_llm()


st.title("大模型文档生成")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "请选择你需要生成的文档!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 单选列表
path = "./word/template"
all_template = os.listdir(path)

options = all_template
selected_option = st.selectbox("选择文档类型", options)
st.write(f"你选择了: {selected_option}")


if prompt := st.chat_input():
    if selected_option!=None:
        file_path = path+"/"+selected_option
        file_output_path = "./word/output/"+selected_option

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        word=word_generation.Word_Generation(word_examples=None,word_template_path=file_path,output_path=file_output_path)
        word_file=word.run(prompt,llm)

        msg = word.output_messages()

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

        st.download_button(
            label="下载文件",
            data=word_file,
            file_name="generated_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
