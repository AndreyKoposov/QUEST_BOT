import unittest
from app.game.structures import ActionResult


class TestActionResult(unittest.TestCase):
    """Тесты для класса AcionResult"""
    def test_add(self):
        """Тест оператора +"""
        # Arrange
        res1 = ActionResult(["Вы пришли в таверну!"], ["Игрок пришел в таверну"])
        res2 = ActionResult(["Вы пришли в замок!"], ["Игрок пришел в замок"])
        expected = ActionResult(["Вы пришли в таверну!", "Вы пришли в замок!"],
                                ["Игрок пришел в таверну", "Игрок пришел в замок"])

        # Act
        real = res1 + res2

        # Assert
        self.assertEqual(real.messages, expected.messages)
        self.assertEqual(real.story, expected.story)
