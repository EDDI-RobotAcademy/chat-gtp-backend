from django.db import models

# Create your models here.
class Board(models.Model):
    boardId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, null=False)
    content = models.TextField()
    boardWriter = models.CharField(max_length=32)
    regDate = models.DateTimeField(auto_now_add=True)
    updDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"boardId: {self.boardId}, title: {self.title}"

    class Meta:
        db_table = 'board'

