#code 参考 https://www.cnblogs.com/yttbk/p/17152062.html
from io import BytesIO

from docxtpl import DocxTemplate
from pydantic import BaseModel, Field, validator,create_model
from typing import List, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
import re
from docx import Document
from utils import tools

class Word_Generation:

    def __init__(self,word_examples,output_path,word_template_path):
        self.word_examples=word_examples
        self.example_prompt = PromptTemplate.from_template("text：{text}。\n 模板：{template}。")
        self.word_template_path = word_template_path
        self.output_path=output_path

    #得到word中的信息,让大模型输出模板一致的数据
    def get_info_word(self,input_text,llm):

        prompt = FewShotPromptTemplate(
            examples=self.word_examples,
            example_prompt=self.example_prompt,
            suffix="text: {input}",
            input_variables=["input"],
        )

        p = prompt.invoke({"input": input_text}).to_string()

        self.res = llm.invoke(p)
        return self.res.content

    def output_messages(self):
        return self.content

    #生成word
    def cop_word(self, data):
        context = data
        tpl = DocxTemplate(self.word_template_path)  # 模板地址
        tpl.render(context[0])  # 渲染替换
        tpl.save(self.output_path)  # 新word保存地址
        return tpl



    def run(self,input_text,llm,out_type: str="memory"):
        if self.word_examples!=None:
            word_content = self.get_info_word(input_text,llm)
        else:
            word_content=input_text
        chain=tools.structure_generation(llm,self.get_var())
        word_content=chain.invoke(word_content)
        self.content = word_content["data"]["word_generation_llm"]

        if out_type == "local":
            word_output=self.cop_word(self.content)
        elif  out_type == "memory":
            word_output=self.cop_word(self.content)
            word_output=self.generate_word_in_memory(word_output)
        return word_output


    #从word中获取变量
    def get_var(self):
        # 动态添加字段
        def add_var_to_pydantic(field_name: dict):
            # 使用 create_model 创建新的 Pydantic 模型，添加新字段
            # 注意：Pydantic 的字段类型是通过类型注解传递的
            new_model = create_model(
                'word_generation_llm',
                **field_name  # 使用字典动态传入字段名和类型
            )
            return new_model

        # 读取 Word 文档
        doc = Document( self.word_template_path)

        # 用于存储找到的变量名
        variables = set()

        # 正则表达式匹配 Jinja2 模板变量（例如：{{ gold_price }}）
        pattern = r"\{\{(.*?)\}\}"

        # 遍历文档中的所有段落
        for para in doc.paragraphs:
            # 查找匹配的模板变量
            matches = re.findall(pattern, para.text)
            variables.update(matches)

        var_dic = {}
        for i in variables:
            var_dic[i] = (Optional[str | None], Field(default=None, description=i))

        new_class = add_var_to_pydantic(var_dic)

        return new_class



    #放在内存中
    def generate_word_in_memory(self,tpl):
        # 将文档保存到内存中
        byte_io = BytesIO()
        tpl.save(byte_io)
        byte_io.seek(0)

        return byte_io