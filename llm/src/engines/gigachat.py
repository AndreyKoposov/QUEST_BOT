from gigachat import GigaChat

from ..engine import AIEngine


THREADS = 1

class GigaChatEngine(AIEngine):
    def __init__(self, key: str, model: str, temp: float):
        super().__init__(THREADS)

        self.giga = GigaChat(
            credentials=key,
            model=model,
            verify_ssl_certs=False,
            temperature=temp,
            scope="GIGACHAT_API_PERS",
            timeout=30,
        )

    @AIEngine.with_semaphore
    async def chat(self, query: str) -> str:
        response = await self.giga.achat(query)
        return response.choices[0].message.content
