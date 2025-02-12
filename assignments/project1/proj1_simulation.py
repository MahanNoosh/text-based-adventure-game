"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str | bool]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)
        loc = self._game.get_location()
        e = Event(loc.id_num, loc.long_description)
        self._events.add_event(e)
        self.generate_events(commands, loc)

    def generate_events(self, commands: list[str | bool], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        for command in commands:
            if command in ("look", "inventory", "score", "undo", "log", "quit", "hit", "stand"):
                continue
            if command in ("4169784500", "goose alone fox goose beans alone goose", "62759709", "3843",
                           "get 10 extra moves", "y", "n"):
                puzzle = self._game.get_puzzle(current_location.id_num)
                loc = self._game.get_location(puzzle.next_loc)
            else:
                loc = self._game.get_location(current_location.available_commands[command])
            e = Event(loc.id_num, loc.long_description)
            self._events.add_event(e, command)
            current_location = loc

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('game_data.json', 7, ["go south"])
        >>> sim.get_id_log()
        [7, 13]

        >>> sim = AdventureGameSimulation('game_data.json', 4, ["unlock the computer", "62759709", "go west"])
        >>> sim.get_id_log()
        [4, 4, 4, 3]

        >>> sim = AdventureGameSimulation('game_data.json', 2, ["use back door", "3843", "go south"])
        >>> sim.get_id_log()
        [2, 2, 1, 7]
        """

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    win_walkthrough = ["pickup cellphone", "go south", "go south", "call reciption", "4169784500", "go south",
                       "go east", "go east", "go north", "go north", "go east", "go north", "go east", "go east",
                       "go south", "face social anxiety and enter", "goose alone fox goose beans alone goose",
                       "pickup laptop charger", "go north", "go north", "go west", "go west", "go north",
                       "unlock the computer", "62759709", "go west", "go west", "use back door", "3843", "go south",
                       "submit project"]
    expected_log = [7, 7, 13, 19, 19, 19, 25, 26, 27, 21, 15, 16, 10, 11, 12,
                    18, 18, 24, 24, 18, 12, 11, 10, 4, 4, 4, 3, 2, 2, 1, 7, 7]

    sim = AdventureGameSimulation('game_data.json', 7, win_walkthrough)
    assert expected_log == sim.get_id_log()

    lose_demo = ["pickup cellphone", "go south", "go north", "go south", "go south", "call reciption", "4169784500",
                 "go south",
                 "go east", "go east", "go north", "go north", "go east", "go north", "go east", "go east",
                 "go south", "face social anxiety and enter", "goose alone fox goose beans alone goose",
                 "pickup laptop charger", "go north", "go north", "go west", "go west", "go north",
                 "unlock the computer", "62759709", "go south", "go south", "go west", "go south", "go south",
                 "go west"]
    expected_log = [7, 7, 13, 7, 13, 19, 19, 19, 25, 26, 27, 21, 15, 16, 10, 11, 12, 18,
                    18, 24, 24, 18, 12, 11, 10, 4, 4, 4, 10, 16, 15, 21, 27, 26]
    sim = AdventureGameSimulation('game_data.json', 7, lose_demo)
    assert expected_log == sim.get_id_log()

    inventory_demo = ["inventory", "pickup cellphone", "inventory", "undo", "inventory"]
    expected_log = [7, 7]
    sim = AdventureGameSimulation('game_data.json', 7, inventory_demo)
    assert expected_log == sim.get_id_log()

    scores_demo = ["score", "pickup cellphone", "go south", "go south", "call reciption", "4169784500", "score"]
    expected_log = [7, 7, 13, 19, 19, 19]
    sim = AdventureGameSimulation('game_data.json', 7, scores_demo)
    assert expected_log == sim.get_id_log()

    enhancement1_demo = ["pickup cellphone", "go south", "go south", "call reciption", "4169784500"]
    expected_log = [7, 7, 13, 19, 19, 19]
    sim = AdventureGameSimulation('game_data.json', 7, enhancement1_demo)
    assert expected_log == sim.get_id_log()

    enhancement2_demo = ["go south", "go south", "go south", "go east", "go east", "go north", "go north", "go east",
                         "go north", "go north", "unlock the computer", "62759709"]
    expected_log = [7, 13, 19, 25, 26, 27, 21, 15, 16, 10, 4, 4, 4]
    sim = AdventureGameSimulation('game_data.json', 7, enhancement2_demo)
    assert expected_log == sim.get_id_log()

    enhancement3_demo = ["go south", "go south", "go south", "go east", "go east", "go north", "go north", "go east",
                         "go north", "go east", "go east", "go south", "face social anxiety and enter",
                         "goose alone fox goose beans alone goose"]
    expected_log = [7, 13, 19, 25, 26, 27, 21, 15, 16, 10, 11, 12, 18, 18, 24]
    sim = AdventureGameSimulation('game_data.json', 7, enhancement3_demo)
    assert expected_log == sim.get_id_log()

    enhancement4_demo = ["go south", "go south", "go south", "go east", "go east", "go north", "go north", "go east",
                         "go north", "go east", "go east", "go south", "face social anxiety and enter",
                         "goose alone fox goose beans alone goose", "play with them", "hit", "stand", "n",
                         "get 10 extra moves"]
    expected_log = [7, 13, 19, 25, 26, 27, 21, 15, 16, 10, 11, 12, 18, 18, 24, 24, 30, 24]
    sim = AdventureGameSimulation('game_data.json', 7, enhancement4_demo)
    assert expected_log == sim.get_id_log()
    # Note: You can add more code below for your own testing purposes
