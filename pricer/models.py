from django.db import models

class Equity(models.Model):
    symbol = models.CharField(max_length=32)

class EquityOption(models.Model):
    underlying = models.ForeignKey(Equity, on_delete=models.CASCADE)
    strike = models.IntegerField(default=0)
    expiration_date = models.DateTimeField()
    contract_type = models.CharField(max_length=1)
    exercise_early = models.BooleanField()
