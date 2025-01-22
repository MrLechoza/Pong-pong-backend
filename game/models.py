from django.db import models

class GameState(models.Model):
    ball_x = models.FloatField()
    ball_y = models.FloatField()
    
class Player(models.Model):
    username = models.CharField(max_length=100)
    score =  models.IntegerField(default=0)
    joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
class Game(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player2')
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='winner', null=True, blank=True)
    score_player1 = models.IntegerField(default=0)  
    score_player2 = models.IntegerField(default=0)  
    create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.player1.username} vs {self.player2.username}'