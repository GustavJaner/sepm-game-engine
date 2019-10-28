# Game Engine

_Software Engineering and Project Management project - Uppsala University_

## Project info
The simple board game is written in Python3. The game can be played player-vs-player locally on one computer, or P2P using sockets. Also possible to play against an AI with three different levels of difficulties(minimax algorithm).

### File structure

```
├── README.md
└── game-engine
    ├── board
    │   └── board_ui.py
    ├── game_platform
    │   ├── AI
    │   │   ├── AI_component
    │   │   │   ├── README.md
    │   │   │   ├── data
    │   │   │   │   ├── test_end.json
    │   │   │   │   ├── test_end_black.json
    │   │   │   │   └── test_init.json
    │   │   │   └── src
    │   │   │       ├── board.py
    │   │   │       ├── constants.py
    │   │   │       ├── coordinates
    │   │   │       │   ├── coord.py
    │   │   │       │   └── coordinates.py
    │   │   │       ├── engine.py
    │   │   │       ├── hard_policy.py
    │   │   │       ├── hard_strategy.py
    │   │   │       ├── ia.py
    │   │   │       ├── medium_strategy.py
    │   │   │       ├── move.py
    │   │   │       ├── soft_strategy.py
    │   │   │       ├── test_board.py
    │   │   │       ├── test_coordinates.py
    │   │   │       ├── test_engine.py
    │   │   │       ├── test_strategy.py
    │   │   │       └── utils.py
    │   │   └── serialize.py
    │   ├── board.py
    │   ├── data.py
    │   ├── game_platform.py
    │   ├── online_game_platform.py
    │   ├── piece.py
    │   └── rules.py
    ├── main.py
    ├── modes
    │   ├── client_game.py
    │   ├── client_socket.py
    │   ├── host_game.py
    │   ├── host_socket.py
    │   ├── local_game.py
    │   ├── player.py
    │   └── tournament.py
    └── screens
        ├── general.py
        ├── host_game.py
        ├── join_game.py
        ├── local_game.py
        ├── online_game.py
        └── tournament.py
```

### Development merge flow
feature branch -> master-staging -> master

### Start the game

`python3 game-engine/main.py`
