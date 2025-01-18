from django.db import models

class GameState(models.Model):
    ball_x = models.FloatField()
    ball_y = models.FloatField()