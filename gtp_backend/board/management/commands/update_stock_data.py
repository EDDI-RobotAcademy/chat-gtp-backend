from django.core.management.base import BaseCommand
from board.service.board_service_impl import BoardServiceImpl

class Command(BaseCommand):
    help = 'Update stock data'

    def handle(self, *args, **kwargs):
        print("Starting stock data update...")
        service = BoardServiceImpl.getInstance()
        service.update()
        print("Stock data update process completed.")

#         python manage.py update_stock_data 사용해서 업데이트 진행가능
