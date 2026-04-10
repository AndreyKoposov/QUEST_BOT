class GameSession():
    async def process(self, user_input: str) -> tuple[list[str], list[list[str]], str]:
        return ([f'Вы написали - {user_input}'], [['Ответ 1'], ['Ответ 2']], 'tavern-test-img.png')
