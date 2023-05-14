import socket
import json
from game_state import GameState
import sys
import torch
from buttons import Buttons
from command import Command
from model import Model1, Model2, Model3, Model4
    
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
    print("initiating connection...")
    if (sys.argv[1]=='1'):
        client_socket = connect(9999)

    elif (sys.argv[1]=='2'):
        client_socket = connect(10000)

    current_game_state = None

    upKeyModel = torch.load("models/up.pt")
    upKeyModel.eval()

    downKeyModel = torch.load("models/down.pt")
    downKeyModel.eval()

    leftKeyModel = torch.load("models/left.pt")
    leftKeyModel.eval()

    rightKeyModel = torch.load("models/right.pt")
    rightKeyModel.eval()

    yKeyModel = torch.load("models/Y.pt")
    yKeyModel.eval()

    bKeyModel = torch.load("models/B.pt")
    bKeyModel.eval()

    rKeyModel = torch.load("models/R.pt")
    rKeyModel.eval()

    keys = Buttons()
    commands = Command()

    is_moving_towards_opp = False
    is_moving_away_opp = False

    up = False
    down = False
    left = False
    right = False
    Y = False
    B = False
    R = False

    while (current_game_state is None) or (not current_game_state.is_round_over):

        # based on features extracted from current game state,
        # make predictions using all key models
        # set predictions in keys object
        # set keys in commands object
        # pass commands object to send() function

        current_game_state = receive(client_socket)

        left = current_game_state.player1.player_buttons.left
        right = current_game_state.player1.player_buttons.right
        x_distance = current_game_state.player2.x_coord - current_game_state.player1.x_coord
        y_distance = current_game_state.player2.y_coord - current_game_state.player1.y_coord

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

        input_features_woY = [

            (current_game_state.timer/153),
            (current_game_state.player1.x_coord/500),
            ((current_game_state.player1.y_coord-50)/150),
            (current_game_state.player2.x_coord/500),
            ((current_game_state.player2.y_coord-50)/150),
            int(current_game_state.player1.is_jumping),
            int(current_game_state.player1.is_crouching),
            keys.up,
            keys.down,
            keys.right,
            keys.left,
            keys.Y,
            keys.B,
            int(current_game_state.player1.player_buttons.X),
            int(current_game_state.player1.player_buttons.A),
            int(current_game_state.player1.player_buttons.L),
            keys.R,
            # int(current_game_state.player1.player_buttons.up),
            # int(current_game_state.player1.player_buttons.down),
            # int(right),
            # int(left),
            # int(current_game_state.player1.player_buttons.Y),
            # int(current_game_state.player1.player_buttons.B),
            # int(current_game_state.player1.player_buttons.R),
            int(current_game_state.player1.is_player_in_move),
            int(current_game_state.player2.is_jumping),
            int(current_game_state.player2.is_crouching),
            int(current_game_state.player2.is_player_in_move),
            int(is_moving_towards_opp),
            int(is_moving_away_opp),
            ((x_distance+250)/500)
        ]

        input_features_wY = [

            (current_game_state.timer/153),
            (current_game_state.player1.x_coord/500),
            ((current_game_state.player1.y_coord-50)/150),
            (current_game_state.player2.x_coord/500),
            ((current_game_state.player2.y_coord-50)/150),
            int(current_game_state.player1.is_jumping),
            int(current_game_state.player1.is_crouching),
            keys.up,
            keys.down,
            keys.right,
            keys.left,
            keys.Y,
            keys.B,
            int(current_game_state.player1.player_buttons.X),
            int(current_game_state.player1.player_buttons.A),
            int(current_game_state.player1.player_buttons.L),
            keys.R,
            # int(current_game_state.player1.player_buttons.up),
            # int(current_game_state.player1.player_buttons.down),
            # int(right),
            # int(left),
            # int(current_game_state.player1.player_buttons.Y),
            # int(current_game_state.player1.player_buttons.B),
            # int(current_game_state.player1.player_buttons.R),
            int(current_game_state.player1.is_player_in_move),
            int(current_game_state.player2.is_jumping),
            int(current_game_state.player2.is_crouching),
            int(current_game_state.player2.is_player_in_move),
            int(is_moving_towards_opp),
            int(is_moving_away_opp),
            ((x_distance+250)/500),
            ((y_distance+150)/300)
        ]

        input_tensor_woY = torch.tensor([input_features_woY]).float()
        input_features_wY = torch.tensor([input_features_wY]).float()

        upKey = (upKeyModel(input_features_wY)).round()
        
        downKey = (downKeyModel(input_features_wY)).round()
    
        leftKey = (leftKeyModel(input_features_wY)).round()

        rightKey = (rightKeyModel(input_features_wY)).round()

        yKey = (yKeyModel(input_features_wY)).round()

        bKey = (bKeyModel(input_tensor_woY)).round()

        rKey = (rKeyModel(input_tensor_woY)).round()

        keys.up = False if (input_features_wY[0][7] == 1) else bool((upKey.detach().numpy())[0][0])
        keys.down = False if (input_features_wY[0][8] == 1) else bool((downKey.detach().numpy())[0][0])
        keys.left = False if (input_features_wY[0][10] == 1) else bool((leftKey.detach().numpy())[0][0])
        keys.right = False if (input_features_wY[0][9] == 1) else bool((rightKey.detach().numpy())[0][0])
        keys.Y = False if (input_features_wY[0][11] == 1) else bool((yKey.detach().numpy())[0][0])
        keys.B = False if (input_features_wY[0][12] == 1) else bool((bKey.detach().numpy())[0][0])
        keys.R = False if (input_features_wY[0][16] == 1) else bool((rKey.detach().numpy())[0][0])

        # up = bool((upKey.detach().numpy())[0][0])
        # down = bool((downKey.detach().numpy())[0][0])
        # left = bool((leftKey.detach().numpy())[0][0])
        # right = bool((rightKey.detach().numpy())[0][0])
        # Y = bool((yKey.detach().numpy())[0][0])
        # B = bool((bKey.detach().numpy())[0][0])
        # R = bool((rKey.detach().numpy())[0][0])

        # keys.up = up
        # keys.down = down
        # keys.left = left
        # keys.right = right
        # keys.Y = Y
        # keys.B = B
        # keys.R = R

        if (keys.left):
            print("left")
        elif (keys.right):
            print("right")

        # print(
        #     keys.up,
        #     keys.down,
        #     keys.left,
        #     keys.right,
        #     keys.Y,
        #     keys.B,
        #     keys.R
        # )

        commands.player_buttons = keys

        nn_command = commands

        send(client_socket, nn_command)

if __name__ == '__main__':
   main()
