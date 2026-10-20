from langchain_ollama import OllamaLLM

class LLMModel:
    def __init__(self) -> None:
        pass

    def get_model() -> OllamaLLM:
        return OllamaLLM(
            model="qwen3.5-4b-Q4_K_M",
            temperature=0.0,
            reasoning=False
        )