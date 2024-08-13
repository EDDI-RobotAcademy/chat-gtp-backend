from django.db import models
import pytz

class StockData(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stock_data'

    @property
    def updated_at_kst(self):
        """UTC 시간을 KST로 변환하여 반환합니다."""
        if self.updated_at:
            kst = pytz.timezone('Asia/Seoul')
            utc = pytz.utc
            utc_dt = self.updated_at.replace(tzinfo=utc)  # UTC로 설정
            return utc_dt.astimezone(kst)  # KST로 변환
        return None

class UpdateLog(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'update_log'

    @property
    def updated_at_kst(self):
        """UTC 시간을 KST로 변환하여 반환합니다."""
        if self.updated_at:
            kst = pytz.timezone('Asia/Seoul')
            utc = pytz.utc
            utc_dt = self.updated_at.replace(tzinfo=utc)  # UTC로 설정
            return utc_dt.astimezone(kst)  # KST로 변환
        return None
