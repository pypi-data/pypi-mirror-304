from langchain_aws import ChatBedrock
from ..types import LLMClient



class BedrockCLient(LLMClient):
    _model: str
    _temperature: float
    _top_p: float
    _max_tokens: int

    def __init__(self, model: str = "anthropic.claude-3-5-sonnet-20241022-v2:0", temperature=0.2, top_p=1, max_tokens=4096):

        self._model = model
        self._temperature = temperature
        self._top_p = top_p
        self._max_tokens = max_tokens
        self._client = ChatBedrock(
            model_id= self._model,
            model_kwargs=dict(temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        )


    def generate(self, user_message: str, system_message: str) -> str:
        print("Using Model: ", self._model)
        if not self._client:
            print("Cannot use a client without API_KEY")
        result = self._client.invoke(
            messages=[
                ("system", system_message),
                ("user", user_message)
            ]
        )

        return result.content
