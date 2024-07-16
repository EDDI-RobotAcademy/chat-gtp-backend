from rest_framework.serializers import Serializer

from board.entity.models import Board


class BoardSerializer(Serializer):
    class Meta:
        model = Board
        fields = ['boardId', 'boardName', 'boardWriter', 'boardContext', 'regDate', 'updDate']
        read_only_fields = ['regDate', 'updDate']