import socket
import json
from game_state import GameState
#from bot import fight
import sys
from bot import Bot
import pandas as pd

def connect(port):
    #For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print ("Connected to game!")
    return client_socket

def send(client_socket, command):
    #This function will send your updated command to Bizhawk so that game reacts according to your command.
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    #receive the game state and return game state
    pay_load = client_socket.recv(4096)
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)

    return game_state

def main():
    if (sys.argv[1]=='1'):
        client_socket = connect(9999)
    elif (sys.argv[1]=='2'):
        client_socket = connect(10000)
    current_game_state = None
    #print( current_game_state.is_round_over )
    bot=Bot()

    i = 0

    gameStateDF = pd.read_csv('gameStateDF.csv')

    while (current_game_state is None) or (not current_game_state.is_round_over):

        i += 1
        current_game_state = receive(client_socket)
        gameStateDF = pd.concat(
            [
                gameStateDF, 
                pd.DataFrame(
                    [
                        {
                            "timer": current_game_state.timer,
                            "has_round_started": current_game_state.has_round_started, 
                            "is_round_over": current_game_state.is_round_over, 
                            "player_id_1": current_game_state.player2.player_id, 
                            "health_1": current_game_state.player2.health, 
                            "x_coord_1": current_game_state.player2.x_coord,
                            "y_coord_1": current_game_state.player2.y_coord, 
                            "is_jumping_1": current_game_state.player2.is_jumping, 
                            "is_crouching_1": current_game_state.player2.is_crouching, 
                            "up_1": current_game_state.player2.player_buttons.up, 
                            "down_1": current_game_state.player2.player_buttons.down, 
                            "right_1": current_game_state.player2.player_buttons.right,
                            "left_1": current_game_state.player2.player_buttons.left, 
                            "select_1": current_game_state.player2.player_buttons.select, 
                            "start_1": current_game_state.player2.player_buttons.start, 
                            "Y_1": current_game_state.player2.player_buttons.Y, 
                            "B_1": current_game_state.player2.player_buttons.B, 
                            "X_1": current_game_state.player2.player_buttons.X,
                            "A_1": current_game_state.player2.player_buttons.A, 
                            "L_1": current_game_state.player2.player_buttons.L, 
                            "R_1": current_game_state.player2.player_buttons.R, 
                            "is_player_in_move_1": current_game_state.player2.is_player_in_move, 
                            "move_id_1": current_game_state.player2.move_id,
                            "player_id_2": current_game_state.player1.player_id, 
                            "health_2": current_game_state.player1.health, 
                            "x_coord_2": current_game_state.player1.x_coord,
                            "y_coord_2": current_game_state.player1.y_coord, 
                            "is_jumping_2": current_game_state.player1.is_jumping, 
                            "is_crouching_2": current_game_state.player1.is_crouching, 
                            "up_2": current_game_state.player1.player_buttons.up, 
                            "down_2": current_game_state.player1.player_buttons.down, 
                            "right_2": current_game_state.player1.player_buttons.right,
                            "left_2": current_game_state.player1.player_buttons.left, 
                            "select_2": current_game_state.player1.player_buttons.select, 
                            "start_2": current_game_state.player1.player_buttons.start, 
                            "Y_2": current_game_state.player1.player_buttons.Y, 
                            "B_2": current_game_state.player1.player_buttons.B, 
                            "X_2": current_game_state.player1.player_buttons.X,
                            "A_2": current_game_state.player1.player_buttons.A, 
                            "L_2": current_game_state.player1.player_buttons.L, 
                            "R_2": current_game_state.player1.player_buttons.R, 
                            "is_player_in_move_2": current_game_state.player1.is_player_in_move, 
                            "move_id_2": current_game_state.player1.move_id,

                            "x_distance": (current_game_state.player1.x_coord - current_game_state.player2.x_coord)
                        }
                    ]
                )
        ], ignore_index = True)
        bot_command = bot.fight(current_game_state,sys.argv[1])
        send(client_socket, bot_command)

    gameStateDF["has_round_started"] = gameStateDF["has_round_started"].astype(int)
    gameStateDF["is_round_over"] = gameStateDF["is_round_over"].astype(int)
    gameStateDF["is_jumping_1"] = gameStateDF["is_jumping_1"].astype(int)
    gameStateDF["is_crouching_1"] = gameStateDF["is_crouching_1"].astype(int)
    gameStateDF["up_1"] = gameStateDF["up_1"].astype(int)
    gameStateDF["down_1"] = gameStateDF["down_1"].astype(int)
    gameStateDF["right_1"] = gameStateDF["right_1"].astype(int)
    gameStateDF["left_1"] = gameStateDF["left_1"].astype(int)
    gameStateDF["select_1"] = gameStateDF["select_1"].astype(int)
    gameStateDF["start_1"] = gameStateDF["start_1"].astype(int)
    gameStateDF["Y_1"] = gameStateDF["Y_1"].astype(int)
    gameStateDF["B_1"] = gameStateDF["B_1"].astype(int)
    gameStateDF["X_1"] = gameStateDF["X_1"].astype(int)
    gameStateDF["A_1"] = gameStateDF["A_1"].astype(int)
    gameStateDF["L_1"] = gameStateDF["L_1"].astype(int)
    gameStateDF["R_1"] = gameStateDF["R_1"].astype(int)
    gameStateDF["is_player_in_move_1"] = gameStateDF["is_player_in_move_1"].astype(int)
    gameStateDF["is_jumping_2"] = gameStateDF["is_jumping_2"].astype(int)
    gameStateDF["is_crouching_2"] = gameStateDF["is_crouching_2"].astype(int)
    gameStateDF["up_2"] = gameStateDF["up_2"].astype(int)
    gameStateDF["down_2"] = gameStateDF["down_2"].astype(int)
    gameStateDF["right_2"] = gameStateDF["right_2"].astype(int)
    gameStateDF["left_2"] = gameStateDF["left_2"].astype(int)
    gameStateDF["select_2"] = gameStateDF["select_2"].astype(int)
    gameStateDF["start_2"] = gameStateDF["start_2"].astype(int)
    gameStateDF["Y_2"] = gameStateDF["Y_2"].astype(int)
    gameStateDF["B_2"] = gameStateDF["B_2"].astype(int)
    gameStateDF["X_2"] = gameStateDF["X_2"].astype(int)
    gameStateDF["A_2"] = gameStateDF["A_2"].astype(int)
    gameStateDF["L_2"] = gameStateDF["L_2"].astype(int)
    gameStateDF["R_2"] = gameStateDF["R_2"].astype(int)
    gameStateDF["is_player_in_move_2"] = gameStateDF["is_player_in_move_2"].astype(int)

    gameStateDF.to_csv('gameStateDF.csv', index=False)

if __name__ == '__main__':
   main()
