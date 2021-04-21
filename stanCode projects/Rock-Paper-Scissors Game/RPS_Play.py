import torch
import torchvision.transforms as T
import cv2
import time
from random import choice
from PIL import Image

CLASS_MAP = {
    0: "blur",
    1: "four",
    2: "middle_finger",
    3: "none",
    4: 'one',
    5: 'paper',
    6: 'rock',
    7: 'scissors',
    8: 'six',
    9: 'three',
    10: 'thumb'
}

NONE = ["blur", "four", "none", 'one', 'six', 'three']
VALID = ['rock', 'paper', 'scissors']

def mapper(val):
    return CLASS_MAP[val]


def calculate_winner(move1, move2):
    if move1 == move2:
        return "Tie"

    if move1 == "rock":
        if move2 == "scissors":
            return "You"
        if move2 == "paper":
            return "Computer"

    if move1 == "paper":
        if move2 == "rock":
            return "You"
        if move2 == "scissors":
            return "Computer"

    if move1 == "scissors":
        if move2 == "paper":
            return "You"
        if move2 == "rock":
            return "Computer"

    if move1 == "middle_finger" or move1 == "thumb":
        return move1




# Load tht model 
model = torch.load('RPS_model_resnet.pt', map_location='cpu')
model.eval()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 2500)
cap.set(4, 1580)

prev_move = None
move_step = 0
start = 0
you_win = 0
com_win = 0
prev_time = time.time()


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        continue

    # rectangle for user to play
    cv2.rectangle(frame, (180, 100), (580, 500), (255, 255, 255), 2)
    # rectangle for computer to play
    cv2.rectangle(frame, (870, 100), (1270, 500), (255, 255, 255), 2)

    # extract the region of image within the user rectangle
    img = frame[100:500, 180:580]

    # Here tell how to run the code by using pytorch - focus on the type of image and how to write the prediction in pytorch

    # the type of image is numpy.ndarray but we need PIL Image (import PIL) to input into our model
    # (the type of image that captured from opencv is "numpy.ndarray",
    # but we need to convert the type into "Image" in order to input
    # to our model / import PIL)                                
    img = Image.fromarray(img, mode="RGB")  # array -> Image
    transform = T.Compose([T.Resize((128, 128)),
                           T.ToTensor()
                           ])
    # Convert Image to To Tensor
    img = transform(img)  # Tensorflow -> img=resize(img, (64, 64))  -> still numpy
    # Make sure the dimension is right (not sure about this part?)                       
    img = img.unsqueeze(0)

    # Predict the move made
    # must be tensor
    pred = model(img)

    # Turn back into numpy and do the argmax to know which class 
    move_code = pred.detach().numpy().argmax()
    user_move_name = mapper(move_code)
    # predict the winner (human vs computer)
    now = time.time()
    if prev_move != user_move_name or now - prev_time >= 1:
        prev_time = time.time()
        move_step = 0
        if user_move_name not in NONE:
            if user_move_name in VALID:
                computer_move_name = choice(VALID)
            else:
                computer_move_name = user_move_name
        else:
            computer_move_name = "none"
        winner = calculate_winner(user_move_name, computer_move_name)
    else:
        if user_move_name in ['rock', 'paper', 'scissors']:
            move_step += 1
    prev_move = user_move_name

    # display the information
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Your Move: " + user_move_name,
                (200, 50), font, 1.2, (255, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Computer's Move: " + computer_move_name,
                (800, 50), font, 1.2, (255, 0, 255), 2, cv2.LINE_AA)

    if computer_move_name != "none":
        icon = cv2.imread("images/{}.png".format(computer_move_name))
        icon = cv2.resize(icon, (400, 400))
        frame[100:500, 870:1270] = icon

    if start == 0:
        cv2.putText(frame, 'DEMO mode',
                    (350, 600), font, 3, (100, 100, 100), 5, cv2.LINE_AA)
        cv2.putText(frame, 'press s to start a game against computer and q to quit!',
                    (250, 700), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

    if move_step >= 10 and start != 0:
        if user_move_name in VALID:
            if winner == "Tie":
                cv2.putText(frame, 'Tie! play one more time!',
                            (300, 700), font, 2, (0, 0, 255), 4, cv2.LINE_AA)
                if start == 1:
                    cv2.putText(frame, 'you:' + str(you_win),
                                (300, 580), font, 2, (255, 0, 255), 4, cv2.LINE_AA)
                    cv2.putText(frame, 'com:' + str(com_win),
                                (950, 580), font, 2, (255, 0, 255), 4, cv2.LINE_AA)
            else:
                if winner == 'You':
                    you_win += 1
                    cv2.putText(frame, winner + ' win !',
                                (500, 700), font, 2, (0, 0, 255), 4, cv2.LINE_AA)
                elif winner == 'Computer':
                    com_win += 1
                    cv2.putText(frame, winner + ' win !',
                                (400, 700), font, 2, (0, 0, 255), 4, cv2.LINE_AA)
                if start == 1:
                    cv2.putText(frame, 'you:' + str(you_win),
                                (300, 580), font, 2, (255, 0, 255), 4, cv2.LINE_AA)
                    cv2.putText(frame, 'com:' + str(com_win),
                                (950, 580), font, 2, (255, 0, 255), 4, cv2.LINE_AA)
            cv2.imshow("Rock Paper Scissors", frame)
            move_step = 0
            start_time = time.time()
            while True:
                frame = frame
                end_time = time.time()
                if end_time - start_time >= 2:
                    break

                if cv2.waitKey(1) & 0xFF == ord('s'):
                    if start == 0:
                        start = 1
                    else:
                        start = 0
                        you_win = 0
                        com_win = 0
                    break

    if com_win == 3 or you_win == 3:
        for r in range(3):
            for i in range(256):
                if winner == 'You':
                    cv2.waitKey(1)
                    cv2.putText(frame, winner + ' win !',
                                (500, 700), font, 2, (i, 0, 255 - i), 5, cv2.LINE_AA)
                elif winner == 'Computer':
                    cv2.waitKey(1)
                    cv2.putText(frame, winner + ' win !',
                                (400, 700), font, 2, (i, 0, 255-i), 5, cv2.LINE_AA)
                cv2.imshow("Rock Paper Scissors", frame)
            for i in range(256):
                if winner == 'You':
                    cv2.waitKey(1)
                    cv2.putText(frame, winner + ' win !',
                                (500, 700), font, 2, (255-i, i, 0), 5, cv2.LINE_AA)
                elif winner == 'Computer':
                    cv2.waitKey(1)
                    cv2.putText(frame, winner + ' win !',
                                (400, 700), font, 2, (255-i, i, 0), 5, cv2.LINE_AA)
                cv2.imshow("Rock Paper Scissors", frame)
            for i in range(256):
                if winner == 'You':
                    cv2.waitKey(1)
                    cv2.putText(frame, winner + ' win !',
                                (500, 700), font, 2, (0, 255 - i, i), 5, cv2.LINE_AA)
                elif winner == 'Computer':
                    cv2.waitKey(1)
                    cv2.putText(frame, winner + ' win !',
                                (400, 700), font, 2, (0, 255-i, i), 5, cv2.LINE_AA)
                cv2.imshow("Rock Paper Scissors", frame)

        start = 0
        you_win = 0
        com_win = 0

    if start == 1:
        cv2.putText(frame, 'you:' + str(you_win),
                    (300, 580), font, 2, (255, 0, 255), 4, cv2.LINE_AA)
        cv2.putText(frame, 'com:' + str(com_win),
                    (950, 580), font, 2, (255, 0, 255), 4, cv2.LINE_AA)
    cv2.imshow("Rock Paper Scissors", frame)

    control = cv2.waitKey(10)

    # start gaming mode
    if control & 0xFF == ord('s'):
        if start == 0:
            start = 1
            move_step = 0
        else:
            start = 0
            you_win = 0
            com_win = 0

    # quit game
    if control & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
