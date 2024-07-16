from unittest import TestCase
from unittest.mock import patch

from board.entity.models import Board
from board.service.board_service_impl import BoardServiceImpl


class BoardViewTest(TestCase):
    @patch('board.service.board_service_impl.BoardRepositoryImpl') # 얘를 가지고 모킹으로 쓰겠다.
    def testList(self, MockBoardRepositoryImpl):
        mockRepository = MockBoardRepositoryImpl.getInstance.return_value # 짝퉁으로 만들어진 값을 가져 오겠다.
        # 리스트를 가져오면 무조건 이 밑에 두개를 불러오겠다.
        mockBoardList = [
            Board(boardId=1, title="Test Board 1", content="Content 1"),
            Board(boardId=2, title="Test Board 2", content="Content 2")
        ]
        mockRepository.list.return_value = mockBoardList

        print(f"Mock Repository Instance: {mockRepository}")
        print(f"Mock Board List: {mockBoardList}")

        BoardServiceImpl._BoardServiceImpl__instance = None
        boardService = BoardServiceImpl.getInstance()

        result = boardService.list()

        print(f"result: {result}")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Test Board 1")
        self.assertEqual(result[1].title, "Test Board 2")

        mockRepository.list.assert_called_once()