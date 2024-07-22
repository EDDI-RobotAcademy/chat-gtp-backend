from rest_framework.serializers import ModelSerializer

from board.entity.models import Board


class BoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields =['boardId', 'title', 'content', 'writer', 'regDate', 'updDate']
        read_only_fields = ['regDate', 'updDate']