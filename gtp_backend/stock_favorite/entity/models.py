from django.db import models

class FavoriteStocks(models.Model):
    email = models.CharField(max_length=255)
    ticker = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FavoriteProducts {self.id} by Email {self.email}"

    class Meta:
        db_table = 'stock_favorite'