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

    gameStateDF = pd.DataFrame(
        columns = [
            "timer", "has_round_started", "is_round_over",
            "player_id_1", "health_1", "x_coord_1", "y_coord_1", "is_jumping_1",
            "is_crouching_1", "up_1", "down_1", "right_1", "left_1", "select_1",
            "start_1", "Y_1", "B_1", "X_1", "A_1", "L_1", "R_1", "is_player_in_move_1",
            "move_id_1", "player_id_2", "health_2", "x_coord_2", "y_coord_2",
            "is_jumping_2", "is_crouching_2", "up_2", "down_2", "right_2", "left_2",
            "select_2", "start_2", "Y_2", "B_2", "X_2", "A_2", "L_2", "R_2",
            "is_player_in_move_2", "move_id_2", "x_distance", "is_moving_towards_opp",
            "is_moving_away_opp", "next_up", "next_down", "next_right", "next_left",
            "next_Y", "next_B", "next_X", "next_A", "next_L", "next_R"
        ]
    )

    gameStateDF = gameStateDF.astype(
        {
            "has_round_started": bool,
            "is_round_over": bool,
            "is_jumping_1": bool,
            "is_crouching_1": bool,
            "up_1": bool,
            "down_1": bool,
            "right_1": bool,
            "left_1": bool,
            "select_1": bool,
            "start_1": bool,
            "Y_1": bool,
            "B_1": bool,
            "X_1": bool,
            "A_1": bool,
            "L_1": bool,
            "R_1": bool,
            "is_player_in_move_1": bool,
            "is_jumping_2": bool,
            "is_crouching_2": bool,
            "up_2": bool,
            "down_2": bool,
            "right_2": bool,
            "left_2": bool,
            "select_2": bool,
            "start_2": bool,
            "Y_2": bool,
            "B_2": bool,
            "X_2": bool,
            "A_2": bool,
            "L_2": bool,
            "R_2": bool,
            "is_player_in_move_2": bool,
            "is_moving_towards_opp": bool,
            "is_moving_away_opp": bool,
            "next_up": bool, 
            "next_down": bool, 
            "next_right": bool,
            "next_left": bool, 
            "next_Y": bool, 
            "next_B": bool, 
            "next_X": bool,
            "next_A": bool, 
            "next_L": bool, 
            "next_R": bool
        }
    )

    is_moving_towards_opp = False
    is_moving_away_opp = False

    while (current_game_state is None) or (not current_game_state.is_round_over):

        current_game_state = receive(client_socket)
        bot_command = bot.fight(current_game_state,sys.argv[1])

        left = bot_command.player_buttons.left
        right = bot_command.player_buttons.right
        x_distance = current_game_state.player2.x_coord - current_game_state.player1.x_coord

        #both left and right pressed
        if (left and right):
            is_moving_towards_opp = False
            is_moving_away_opp = False
        #only right pressed
        elif (right):
            if (x_distance >= 0):
                is_moving_towards_opp = True
                is_moving_away_opp = False
            else:
                is_moving_towards_opp = False
                is_moving_away_opp = True
        #only left pressed
        elif (left):
            if (x_distance >= 0):
                is_moving_towards_opp = False
                is_moving_away_opp = True
            else:
                is_moving_towards_opp = True
                is_moving_away_opp = False
        #neither left nor right pressed
        else:
            is_moving_towards_opp = False
            is_moving_away_opp = False  

        gameStateDF = pd.concat(
            [
                gameStateDF, 
                pd.DataFrame(
                    [
                        {
                            "timer": current_game_state.timer,
                            "has_round_started": current_game_state.has_round_started, 
                            "is_round_over": current_game_state.is_round_over, 
                            "player_id_1": current_game_state.player1.player_id, 
                            "health_1": current_game_state.player1.health, 
                            "x_coord_1": current_game_state.player1.x_coord,
                            "y_coord_1": current_game_state.player1.y_coord, 
                            "is_jumping_1": current_game_state.player1.is_jumping, 
                            "is_crouching_1": current_game_state.player1.is_crouching, 
                            "up_1": current_game_state.player1.player_buttons.up, 
                            "down_1": current_game_state.player1.player_buttons.down, 
                            "right_1": current_game_state.player1.player_buttons.right,
                            "left_1": current_game_state.player1.player_buttons.left,
                            "select_1": current_game_state.player1.player_buttons.select, 
                            "start_1": current_game_state.player1.player_buttons.start, 
                            "Y_1": current_game_state.player1.player_buttons.Y, 
                            "B_1": current_game_state.player1.player_buttons.B, 
                            "X_1": current_game_state.player1.player_buttons.X,
                            "A_1": current_game_state.player1.player_buttons.A, 
                            "L_1": current_game_state.player1.player_buttons.L, 
                            "R_1": current_game_state.player1.player_buttons.R, 
                            "is_player_in_move_1": current_game_state.player1.is_player_in_move, 
                            "move_id_1": current_game_state.player1.move_id, 
                            "player_id_2": current_game_state.player2.player_id, 
                            "health_2": current_game_state.player2.health, 
                            "x_coord_2": current_game_state.player2.x_coord,
                            "y_coord_2": current_game_state.player2.y_coord, 
                            "is_jumping_2": current_game_state.player2.is_jumping, 
                            "is_crouching_2": current_game_state.player2.is_crouching, 
                            "up_2": current_game_state.player2.player_buttons.up, 
                            "down_2": current_game_state.player2.player_buttons.down, 
                            "right_2": current_game_state.player2.player_buttons.right,
                            "left_2": current_game_state.player2.player_buttons.left, 
                            "select_2": current_game_state.player2.player_buttons.select, 
                            "start_2": current_game_state.player2.player_buttons.start, 
                            "Y_2": current_game_state.player2.player_buttons.Y, 
                            "B_2": current_game_state.player2.player_buttons.B, 
                            "X_2": current_game_state.player2.player_buttons.X,
                            "A_2": current_game_state.player2.player_buttons.A, 
                            "L_2": current_game_state.player2.player_buttons.L, 
                            "R_2": current_game_state.player2.player_buttons.R, 
                            "is_player_in_move_2": current_game_state.player2.is_player_in_move, 
                            "move_id_2": current_game_state.player2.move_id,
                            "x_distance": x_distance,
                            "is_moving_towards_opp": is_moving_towards_opp,
                            "is_moving_away_opp": is_moving_away_opp,
                            "next_up": bot_command.player_buttons.up, 
                            "next_down": bot_command.player_buttons.down, 
                            "next_right": right,
                            "next_left": left, 
                            "next_Y": bot_command.player_buttons.Y, 
                            "next_B": bot_command.player_buttons.B, 
                            "next_X": bot_command.player_buttons.X,
                            "next_A": bot_command.player_buttons.A, 
                            "next_L": bot_command.player_buttons.L, 
                            "next_R": bot_command.player_buttons.R, 
                        }
                    ]
                )
        ], ignore_index = True)

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
    gameStateDF["is_moving_towards_opp"] = gameStateDF["is_moving_towards_opp"].astype(int)
    gameStateDF["is_moving_away_opp"] = gameStateDF["is_moving_away_opp"].astype(int)
    gameStateDF["next_up"] = gameStateDF["next_up"].astype(int)
    gameStateDF["next_down"] = gameStateDF["next_down"].astype(int)
    gameStateDF["next_right"] = gameStateDF["next_right"].astype(int)
    gameStateDF["next_left"] = gameStateDF["next_left"].astype(int)
    gameStateDF["next_Y"] = gameStateDF["next_Y"].astype(int)
    gameStateDF["next_B"] = gameStateDF["next_B"].astype(int)
    gameStateDF["next_X"] = gameStateDF["next_X"].astype(int)
    gameStateDF["next_A"] = gameStateDF["next_A"].astype(int)
    gameStateDF["next_L"] = gameStateDF["next_L"].astype(int)
    gameStateDF["next_R"] = gameStateDF["next_R"].astype(int)

    gameStateDF.to_csv("gameStateDF3.csv", index=False)

if __name__ == "__main__":
   main()
