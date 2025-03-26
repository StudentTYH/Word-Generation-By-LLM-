from kor import create_extraction_chain, Object, Text, from_pydantic
from langchain_ollama import ChatOllama
from kor import prompts, examples

def define_llm(model_name="qwen2"):

    llm = ChatOllama(
        model=model_name,
        temperature=0,
        # other params...
    )
    return llm


def structure_generation(llm,pydantic_class):

    def _generate_examples(node):
        examples_list = examples.generate_examples(node)
        return examples_list if examples_list else [("", {node.id: {}})]


    prompts.generate_examples = _generate_examples


    new_class=pydantic_class

    schema, validator = from_pydantic(new_class, description="", many=True)

    chain = create_extraction_chain(
        llm, schema, encoder_or_encoder_class="json", validator=validator, input_formatter="triple_quotes"
    )

    return chain


