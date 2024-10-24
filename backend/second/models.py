from django.db import models


class Calculator(models.Model):
    a = models.FloatField()
    b = models.FloatField()
    c = models.FloatField()
    root1 = models.FloatField(blank=True, null=True)
    root2 = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.a}x^2 + {self.b}x + {self.c} = 0'
