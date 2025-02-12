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
        -self.id_num >= 0 #TODO
    """

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    def __init__(self, location_id, brief_description, long_description, available_commands, items,
                 visited=False) -> None:
        """Initialize a new location.

        """

        self.id_num = location_id
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items
        self.visited = visited


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: string representing the name of the item.
        - description: a string describing the item.
        - start_position: an integer representing the starting location ID of the item.
        - target_position:an integer represnting the target location ID of the item( where it will be delivered to).
        - target_points: an integer represinting how many points a player will be awarded when item reaches target_position.

    Representation Invariants:
        - name != ''
        - description != ''
        - start_position >=0 #TODO
        - target_position >=0
        - target_points >=0
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

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
        - name: string representing the name of the puzzle.
        - prompt: string representing prompt of the puzzle.
        - win: set for text shown when game is won.
        -lose: string for text shown when game is lost.
        -answer: a list representing the answer to the game.
        -dialogue: string representing a dialogue in the puzzle

    Representation Invariants:
        - name=!""

    """

    name: str
    prompt: str
    win: set[str, str]
    lose: str
    answer: list
    dialogue: str


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
