from connectfour import winner

boards = [
    [
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", "O", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", "O", " ", " "],
        [" ", " ", " ", " ", "O", " ", " "],
        [" ", " ", " ", " ", "X", "X", "X"],
    ],
]


for board in boards:
    print(winner(board))
