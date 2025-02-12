"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: a unique integer identifier for this location.
        - brief_description: a string short description of the location.
        - long_description: a long description of the location.
        - available_commands: A mapping of commands (e.g., "go north") to descriptions or destinations.
        - items: a list of items present in this location.
        - visited: a boolean indicating whether the player has previously visited this location.

    Representation Invariants:
        -self.id_num > 0
        -brief_description != ""
        -long_description != ""
        -len(available_commands) > 0
    """
    id_num: int
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited: bool


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: string representing the name of the item.
        - description: a string describing the item.
        - start_position: an integer representing the starting location ID of the item.
        - target_position:an integer represnting the target location ID of the item( where it will be delivered to).
        - target_points: an integer showing how many points a player will be awarded when item reaches target_position.

    Representation Invariants:
        - name != ''
        - description != ''
        - start_position > 0
        - target_position > 0
        - target_points > 0
    """

    name: str
    description: str
    start_position: int
    target_position: int
    target_points: int


@dataclass
class Puzzle:
    """
    A puzzle in our text adventure game.

    Instance Attributes:
        - prompt: string representing prompt of the puzzle.
        - loc: location id that the puzzle is located
        - win: text shown when puzzle is won.
        - next_loc: the next location this puzzle leads to.
        - lose: string for text shown when game is lost.
        - answer: a list representing the answer to the game.
        - dialogue: string representing a dialogue in the puzzle

    Representation Invariants:
        - loc > 0
        - next_loc > 0

    """

    prompt: str
    loc: int
    win: str
    next_loc: int
    lose: str
    answer: list
    dialogue: str


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
