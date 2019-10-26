# VegaSoft GameEngine

This is a demonstration for a GameEngine for the UU-GAME developed in the Software Engineering and Project Management course at Uppsala University, during the period Autumn 2019.

## Files description

Here I provide a small description of each one of the files in this repository. For a more detailed guide of how to use the different classes, I'd recommend to read the `test_*` files.

1. The *data* folder contains examples of valid input json files, which are also used by some of the tests.
2. The *src* folder contains the code.

⋅⋅⋅`board.py`: contains both, a representation of the game state and the functions to verify the logic of the game.

⋅⋅⋅`constants.py`: provides two constants used in the project. Despite being variables that could be changed by the configuration file, they are omitted and fallbacl always to these default values.

⋅⋅⋅`coordinates/*`: is a Flyweight factory function to create `coordinates.Coord` objects.

⋅⋅⋅`engine.py`: main function encapsulating the rest of the program.

⋅⋅⋅`ia.py`: strategy pattern for the three types of IA.

⋅⋅⋅`*_strategy.py`: specific strategies.

⋅⋅⋅`*hard_policy.py`: evaluation functions for the minimax algorithm implemented in `hard_strategy.py`.

⋅⋅⋅`*move.py`: small class to store a move: the two coordinates (start and end) and the player making the move.

⋅⋅⋅`*utils.py`: singleton implementation.



## License

This project is licensed to the selling group under the MIT License with permission for using and modifying it in the context of the class, but without permission to share to another group or selled by any virtual or real currency.

## Acknowledgments

* https://github.com/ibratanov/tablut.ai
