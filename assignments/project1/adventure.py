"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
import json
import random
from typing import Optional


from game_entities import Location, Item, Puzzle
from proj1_event_logger import Event, EventList


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: the id of location we are currently at.
        - ongoing: saves if the game is running.
        - inventory: alist of items the player has in game
        - score: score of player in game
    Representation Invariants:
        - len(_locations) > 0
        - len(_items) > 0
        - score >= 0
    """
    # Private Instance Attributes:
    #   - _locations: a mapping from location id to Location object. This represents all the locations in the game.
    #   - _items: a dictionary of Item objects, mapping item name to items in the game.

    _locations: dict[int, Location]
    _items: dict[str, Item]
    _puzzles: dict[int, Puzzle]
    inventory: list[Item]
    score: int
    current_location_id: int
    ongoing: bool

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """
        self._locations, self._items, self._puzzles = self._load_game_data(game_data_file)
        self.current_location_id = initial_location_id
        self.ongoing = True
        self.inventory = []
        self.score = 0

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], dict[str, Item], dict[int, Puzzle]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'], False)
            locations[loc_data['id']] = location_obj

        items = {}
        for item_data in data['items']:  # Go through each element associated with the 'items' key in the file
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'],
                            item_data['target_position'], item_data['target_points'])
            items[item_data['name']] = item_obj
        puzzles = {}
        for puzzle_data in data['puzzles']:  # Go through each element associated with the 'puzzles' key in the file
            puzzle_obj = Puzzle(puzzle_data['prompt'], puzzle_data['loc'], puzzle_data['win'],
                                puzzle_data['next_loc'], puzzle_data['lose'], puzzle_data['answer'],
                                puzzle_data['dialogue'])
            puzzles[puzzle_data['loc']] = puzzle_obj
        return locations, items, puzzles

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        if loc_id is None:
            return self._locations[self.current_location_id]
        return self._locations[loc_id]

    def get_item(self, item_name: str) -> Item | None:
        """Return Item object associated with the provided Item name.
                """

        if item_name in self._items:
            return self._items[item_name]
        return None

    def get_puzzle(self, puzzle_id: int) -> Puzzle | None:
        """
         Return the puzzle with the given loc id from the list of available puzzles.
        """

        if puzzle_id in self._puzzles:
            return self._puzzles[puzzle_id]
        return None

    def pickup_item(self, new_item: Item) -> bool:
        """
        adds item to player inventory if it doesn't already exist
        """

        if new_item not in self.inventory:
            self.inventory.append(new_item)
            return True
        return False

    def inventory_has(self, item_name: str) -> bool:
        """
        checks if inventory contains Item with name item_name
        """

        return self._items[item_name] in self.inventory

    def update_score(self) -> None:
        """
        updates score of player based on items in inventory
        """
        sc = 0
        for item_in in self.inventory:
            sc += item_in.target_points
        self.score = sc


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 7)  # load data, setting initial location ID to 7
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    WIN_SCORE = 20
    MAX_MOVES = 25
    moves_remaining = MAX_MOVES
    claimed_bonus = False
    choice = None
    picked = True           # if on commands that adds item we were successful

    def submit_project() -> None:
        """
        helper for submit project event
        """
        puzzle = game.get_puzzle(game.current_location_id)
        if game.score == WIN_SCORE:
            print(puzzle.win)
            game.ongoing = False
        else:
            print(puzzle.lose)

    def call_recepton() -> bool:
        """
        helper for call reception event.
        """
        puzzle = game.get_puzzle(game.current_location_id)
        if game.inventory_has("cellphone"):
            number = input(puzzle.prompt).strip().replace("-", "")
            if number in puzzle.answer:
                print(puzzle.win)
                return game.pickup_item(game.get_item(location.items[0]))
            else:
                print(puzzle.lose)
        else:
            print(puzzle.dialogue)
        return False

    def unlock_computer() -> bool:
        """
        helper for unlock computer event.
        """
        puzzle = game.get_puzzle(game.current_location_id)
        password = input(puzzle.prompt)
        if password in puzzle.answer:
            game.pickup_item(game.get_item(location.items[0]))
            print(puzzle.win)
            return True
        else:
            print(puzzle.lose)
            return False

    def social_anxiety() -> None:
        """
        helper method for face social anxiety and enter event
        """
        puzzle = game.get_puzzle(game.current_location_id)
        print(puzzle.dialogue)
        answer = input(puzzle.prompt)
        if answer in puzzle.answer:
            print(puzzle.win)
            game.current_location_id = puzzle.next_loc
        else:
            print(puzzle.lose)

    def random_1_to_10() -> int:
        """
        returns a random number between 1 and 10 inclusive for fake black jack minigame
        """
        return int(1 + (random.random()) * 10)

    def play_with_them() -> None:
        """
        helper for the play with them event (fake blackjack)
        """
        puzzle = game.get_puzzle(game.current_location_id)
        print(puzzle.prompt)
        playing = True
        while playing:
            computer_numbers = [random_1_to_10()]
            player_numbers = [random_1_to_10(), random_1_to_10()]
            print(f"you have {player_numbers} which adds up to {sum(player_numbers)}\n"
                  f"your new friend first number is {computer_numbers}")
            while True:
                pick = input('if you wanna add another number say "hit" if not say "stand": ')
                if helper_choice(computer_numbers, player_numbers, pick):
                    break
                if sum(player_numbers) > 21 and pick == "hit":
                    print(f"your friend won!\nyou had {player_numbers} ({sum(player_numbers)})")
                    break
                elif sum(player_numbers) == 21 and pick == "hit":
                    print(f"you won!\nyou had {player_numbers} (21)")
                    break
            while True:
                again = input("Play again? y/n: ")
                if again == "y":
                    break
                elif again == "n":
                    playing = False
                    break
        print(puzzle.dialogue)
        game.current_location_id = puzzle.next_loc

    def helper_choice(computer_numbers: list[int], player_numbers: list[int], pick: str) -> bool:
        """
        helper for play_with_them function choice
        """
        if pick == "hit":
            player_numbers.append(random_1_to_10())
            print(f"you have {player_numbers} which adds up to {sum(player_numbers)}")
        elif pick == "stand":
            computer_numbers.append(random_1_to_10())
            while sum(computer_numbers) <= 16:
                computer_numbers.append(random_1_to_10())
            if sum(computer_numbers) > 21 or sum(player_numbers) >= sum(computer_numbers):
                print(
                    f"you won!\n"
                    f"they had {computer_numbers} ({sum(computer_numbers)}), and you had {player_numbers} "
                    f"({sum(player_numbers)})")
                return True
            else:
                print(
                    f"your friend won!\n"
                    f"they had {computer_numbers} ({sum(computer_numbers)}), and you had {player_numbers} "
                    f"({sum(player_numbers)})")
                return True
        return False

    def backdoor() -> None:
        """
        helper for the use backdoor event
        """
        puzzle = game.get_puzzle(game.current_location_id)
        print(puzzle.dialogue)
        code = input(puzzle.prompt)
        if code in puzzle.answer:
            print(puzzle.win)
            game.current_location_id = puzzle.next_loc
        else:
            print(puzzle.lose)

    def extra_moves(already_claimed_bonus: bool, moves: int) -> tuple[bool, int]:
        """
        adds 10 extra moves to player moves after doing some puzzles in game
        """
        puzzle = game.get_puzzle(game.current_location_id)
        if not already_claimed_bonus:
            moves += 10
            already_claimed_bonus = True
            game.current_location_id = puzzle.next_loc
        else:
            print(puzzle.lose)
        return already_claimed_bonus, moves

    while game.ongoing:
        game.update_score()
        if moves_remaining == 0:
            print("You lose :(")
            game.ongoing = False
            break
        location = game.get_location()

        if choice not in menu and picked:
            e = Event(location.id_num, location.long_description)
            game_log.add_event(e, choice)

        if (game_log.last.prev and game_log.last.prev.id_num != game_log.last.id_num and picked
                and choice not in ("get 10 extra moves", "play with them") and choice not in menu):
            moves_remaining -= 1

        if location.visited:
            location_description = location.brief_description
        else:
            location_description = location.long_description
            location.visited = True

        print(location_description)

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input(f"\nEnter action (you have {moves_remaining} moves remaining): ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()
        print("========")
        print("You decided to:", choice)
        print()
        picked = True
        if choice in menu:
            if choice == "log":
                game_log.display_events()
            elif choice == "look":
                location.visited = False
            elif choice == "score":
                print(f"- You currently have {game.score}/{WIN_SCORE} score")
            elif choice == "quit":
                game.ongoing = False
            elif choice == "inventory":
                if len(game.inventory) == 0:
                    print("- You have no item in your inventory")
                for item in game.inventory:
                    print(f"- {item.name}:\t\t{item.description}")
            elif choice == "undo":
                if game_log.last.prev is None:
                    break
                if game_log.last.prev and game_log.last.id_num != game_log.last.prev.id_num:
                    moves_remaining += 1
                if game.inventory and game_log.last.prev.next_command[:6] in ["pickup", "unlock", "call r"]:
                    game.inventory.pop()
                game_log.remove_last_event()
                game.current_location_id = game_log.last.id_num

        else:
            result = location.available_commands[choice]
            game.current_location_id = result
            if choice[:6] == "pickup":
                picked = game.pickup_item(game.get_item(location.items[0]))
                if not picked:
                    print("You have already pickedup this!")
            elif choice == "submit project":
                submit_project()
            elif choice == "call reciption":
                if not game.inventory_has("lucky mug"):
                    picked = call_recepton()
                else:
                    print("You have already called them!")
                    picked = False

            elif choice == "unlock the computer":
                if not game.inventory_has("USB drive"):
                    picked = unlock_computer()
                else:
                    print("Computer had been unlocked before")
                    picked = False

            elif choice == "knock on robarts back door":
                print(
                    "The backdoor is locked. You knocked, but no one answered. Try entering through the front "
                    "door on St. George.\n")
            elif choice == "face social anxiety and enter":
                social_anxiety()
            elif choice == "play with them":
                play_with_them()
            elif choice == "get 10 extra moves":
                updates = extra_moves(claimed_bonus, moves_remaining)
                claimed_bonus = updates[0]
                moves_remaining = updates[1]
            elif choice == "use back door":
                backdoor()
