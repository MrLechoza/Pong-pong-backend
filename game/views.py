from django.http import JsonResponse
from .models import GameState

def get_game_state(request):
    game_state = GameState.objects.first()
    
    if not game_state:
        game_state = GameState.objects.create(ball_x=0, ball_y=0)
    
    return JsonResponse({
        'ball_x': game_state.ball_x,
        'ball_y': game_state.ball_y,
    })