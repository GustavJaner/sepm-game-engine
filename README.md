# Game Engine

_Project within Software Engineering and Project Management, Uppsala University - Group B_

## Project info

A game engine developed in Python3. The game engine is one out of three components for a simple game.

### Development merge flow

feature branch -> master-staging -> master

### File structure

```
├── game-engine
│   ├── board
│   │   ├── board_ui.py
│   ├── game_platform
│   │   ├── data.py
│   │   ├── game_platform.py
│   │   ├── piece.py
│   │   └── rules.py
│   ├── main.py
│   ├── modes
│   │   ├── local_game.py
│   │   ├── player.py
│   └── screens
│       ├── general.py
│       ├── local_game.py
└── README.md
```

### Start the game engine

`python3 game-engine/main.py`
