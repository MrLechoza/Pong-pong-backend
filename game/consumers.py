import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer


class PingPongConsumer(AsyncWebsocketConsumer):
    players = {}  
    game_state = {
        "ball": {"x": 50, "y": 50, "dx": 1, "dy": 1},  
        "player1": 50,  
        "player2": 50,  
        "score1": 0, 
        "score2": 0, 
    }
    
    speed_multiplier = 1.0

    async def connect(self):
        self.room_group_name = "pingpong_game"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        
        if len(self.players) < 2:
            role = 'player1' if 'player1' not in self.players else 'player2'
            self.players[role] = self.channel_name
            await self.send(text_data=json.dumps({'type': 'role', 'role': role}))
            if len(self.players) == 2:
                asyncio.create_task(self.start_game())
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        self.players = {role: channel for role, channel in self.players.items() if channel != self.channel_name}

    async def receive(self, text_data):
        data = json.loads(text_data)
        role = data.get('role')
        position = data.get('position')

        max_position = 100 
        paddle_height = 20 
        min_position = 0
        
        if role == 'player1':
            self.game_state['player1'] = max(min_position, min(max_position - paddle_height, position))
        elif role == 'player2':
            self.game_state['player2'] = max(min_position, min(max_position - paddle_height, position))

    async def start_game(self):
        while len(self.players) == 2:
            ball = self.game_state["ball"]
            ball["x"] += ball["dx"] * self.speed_multiplier
            ball["y"] += ball["dy"] * self.speed_multiplier

            # incrementa la velocidad 
            self.speed_multiplier = min(self.speed_multiplier + 0.002, 4.0)
            
            if ball["y"] <= 0 or ball["y"] >= 100:
                ball["dy"] *= -1
                
            
            if ball["x"] <= 7:  
                if self.game_state["player1"] <= ball["y"] <= self.game_state["player1"] + 20:  
                    ball["dx"] *= -1
                else:
                    self.game_state["score2"] += 1  
                    if self.game_state["score2"] >= 5:  
                        await self.end_game("player2")
                        break
                    else:
                        self.reset_ball()
            elif ball["x"] >= 93:  
                if self.game_state["player2"] <= ball["y"] <= self.game_state["player2"] + 20:
                    ball["dx"] *= -1
                else:
                    self.game_state["score1"] += 1  
                    if self.game_state["score1"] >= 5: 
                        await self.end_game("player1")
                        break
                    else:
                        self.reset_ball()

            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "game_update",
                    "message": self.game_state
                }
            )
            await asyncio.sleep(0.05)

    async def game_update(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"type": "update", "state": message}))

    async def end_game(self, winner):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "game_over",
                "message": {
                    "winner": winner, 
                    "score1": self.game_state["score1"], 
                    "score2": self.game_state["score2"]}
            }
        )
       
        self.reset_game()

    def reset_ball(self):
        
        self.game_state["ball"] = {"x": 50, "y": 50, "dx": 1, "dy": 1}
        self.speed_multiplier = 1.0 # se restablece la velocidad

    def reset_game(self):
        
        self.game_state["ball"] = {"x": 50, "y": 50, "dx": 1, "dy": 1}
        self.game_state["player1"] = 50
        self.game_state["player2"] = 50

    async def game_over(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"type": "game_over", "message": message}))
