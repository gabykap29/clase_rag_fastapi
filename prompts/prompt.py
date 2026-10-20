from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    """ 
    Eres un asistente encargado de responder preguntas.
    Recibiras un contexto, y debes utilizarlo para responder las
    preguntas.
    contex: {context}
    input_user: {input_user}
    Si el contexto no es suficiente para responder las preguntas,
    simplemente responde: "esta pregunta está fuera de mis limites!"
    """
)