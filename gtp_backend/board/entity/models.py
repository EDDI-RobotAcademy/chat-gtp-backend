from django.db import models

# Create your models here.


class Board(models.Model):
    boardId = models.AutoField(primary_key=True)
    boardName = models.CharField(max_length=32, null=False)
    boardContext = models.TextField(null=False)
    boardWriter = models.CharField(max_length=32, null=False)
    regDate = models.DateTimeField(auto_now_add=True)
    updDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.boardId, self.boardName

    class Meta:
        db_table = "board"



