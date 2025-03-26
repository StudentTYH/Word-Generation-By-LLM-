# Word-Generation-By-LLM
# 通过Langchain进行文档生成。

代码还写得不是那么好，后续继续优化（3.26）。


## Example



![alt text](./image/cad804930ac84ee29f01612a36415e8d.png)

![alt text](./image/5a441403e482df4233217dbd388a7928_720.png)


## 生成步骤

1、手动做一个word模板，并且将需要填写的数据通过jinjia2语法进行占位。

2、输如一段本文，通过Langchain结构提取将本文中的关键信息进行提取，输出json格式数据。

3、将提取到的关键信息通过jinjia2语法填入word。

