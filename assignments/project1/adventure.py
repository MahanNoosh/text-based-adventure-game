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

from game_entities import Location, Item
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - _locations: a mapping from location id to Location object. This represents all the locations in the game.
        - _items: a list of Item objects, representing all items in the game.
        - current_location_id: the id of location we are currently at.
        - ongoing: saves if the game is running.
        #TODO
    Representation Invariants:
        - len(_locations) > 0
        - len(_items) > 0
        #TODO
    """

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        for item_data in data['items']:  # Go through each element associated with the 'items' key in the file
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'],
                            item_data['target_position'], item_data['target_points'])
            items.append(item_obj)

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        if loc_id is None:
            return self._locations[self.current_location_id]
        return self._locations[loc_id]


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
    inventory = []
    score = 0
    moves = 25
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location()

        if choice not in menu:
            e = Event(location.id_num, location.long_description)
            game_log.add_event(e, choice)

        location_description = ""
        if location.visited:
            location_description = location.brief_description
        else:
            location_description = location.long_description

        print(location_description)

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()
        print("========")
        print("You decided to:", choice)


        def submit_project() -> None:
            """
            helper for submit project event
            """
            if "USB drive" in inventory and "laptop charger" in inventory and "lucky mug" in inventory:
                print("Nice, you submitted it with two minutes to spare!")
            else:
                print("You don’t have the required items to submit your project.")


        def call_recepton() -> None:
            """
            helper for call reception event.
            """
            if "cellphone" in inventory:
                number = input("dial phone number: ").replace("-", "")
                if number == "4169784500":
                    print("They said you left it in the bathroom cabinet. OH! "
                          "You use it while brushing your teeth to save water. That makes sense!")
                    inventory.append(location.items[0])
                else:
                    print("Wait, who is this? Sorry, wrong number.")
            else:
                print("You don’t have your phone on you, how can you call them?")


        def unlock_computer() -> None:
            """
            check if the player enters the correct password.
            """
            password = input("Enter the password: ")
            if password == "62759709":
                inventory.append(location.items[0])
                print("Nice! Thank God you found the password!")
            else:
                print("Oh no, the password is wrong!")


        def social_anxiety() -> None:
            """
            helper method for social anxiety event
            """
            print(
                "You don't have the confidence to get in the room! So, let’s make a bet: if you solve this puzzle, "
                "you should knock and go in. After all, it’s a tough one, and you did it!")
            print(
                "You have a fox, a goose, and a bag of beans. You need to cross a river with them, "
                "but the boat can only carry you and one item at a time.\n"
                "If left alone together, the fox will eat the goose, and the goose will eat the beans. "
                "How can you get them all across safely?")
            answer = input(
                "Enter what you take to the other side in order and space seperated (fox, goose, beans, alone): ")
            if (answer == "goose alone fox goose beans alone goose" or answer ==
                    "goose alone beans goose fox alone goose"):
                print("Nice! See? You should be more confident.")
                game.current_location_id = 24
            else:
                print("I don’t think this is working. Did you enter it correctly?")


        def play_with_them() -> None:
            """
            helper for the play with them event
            """
            print("Oh, nice! You really did that?! Looks like you don’t have social anxiety anymore!")
            print(
                "This is a variation of Blackjack. You receive random numbers when you hit. "
                "You win if you reach 21 or if your friend has a lower total than you. Anyone who exceeds 21 loses.")
            playing = True
            while playing:
                computer_numbers = [int(1 + (random.random()) * 9)]
                player_numbers = [int(1 + (random.random()) * 9), int(1 + (random.random()) * 9)]
                print(f"you have {player_numbers} which adds up to {sum(player_numbers)}")
                print(f"your new friend first number is {computer_numbers}")
                while True:
                    action = input('if you wanna add another number say "hit" if not say "stay": ')
                    if action == "hit":
                        player_numbers.append(int(1 + (random.random()) * 9))
                        print(f"you have {player_numbers} which adds up to {sum(player_numbers)}")
                    else:
                        computer_numbers.append(int(1 + (random.random()) * 9))
                        while sum(computer_numbers) <= 16:
                            computer_numbers.append(int(1 + (random.random()) * 9))
                        if sum(computer_numbers) > 21 or sum(player_numbers) >= sum(computer_numbers):
                            print("you won!")
                            print(
                                f"they had {computer_numbers} ({sum(computer_numbers)}), and you had {player_numbers} "
                                f"({sum(player_numbers)})")
                            break
                        else:
                            print("your friend won!")
                            print(
                                f"they had {computer_numbers} ({sum(computer_numbers)}), and you had {player_numbers} "
                                f"({sum(player_numbers)})")
                            break
                    if sum(player_numbers) > 21:
                        print("your friend won")
                        print(f"you had {player_numbers} ({sum(player_numbers)})")
                        break
                    elif sum(player_numbers) == 21:
                        print("you won!")
                        print(f"you had {player_numbers} (21)")
                        break
                while True:
                    again = input("Play again? y/n: ")
                    if again == "y":
                        break
                    elif again == "n":
                        playing = False
                        break
            print(
                "Your friend said you’re a good friend!"
                " They mentioned knowing a secret door in this room and want you to go in for a surprise!")
            game.current_location_id = 30


        def backdoor() -> None:
            """
            helper for the backdoor event
            """
            print(
                "You need to figure out the 4-digit code to unlock the door. The clues written behind the door are:\n"
                "1.The code is made up of four digits.\n"
                "2.The second digit is greater than the first\n"
                "3.The sum of all digits is 18.\n"
                "4.The third digit is half the second digit.\n"
                "5.The fourth digit is one less than the third.")
            code = input("What's the code?")
            if code == "3843":
                print("door unlocked and you ran toward your college.")
                game.current_location_id = 1
            else:
                print("Wrong code!")


        if choice in menu:
            # TODO: Handle each menu command as appropriate
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            if choice == "log":
                game_log.display_events()
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
            elif choice == "look":
                print(location.long_description)
            elif choice == "score":
                print(score)
            elif choice == "quit":
                game.ongoing = False
            elif choice == "inventory":
                print(inventory)
            elif choice == "undo":
                if game_log.last.prev.next_command[:6] == "pickup":
                    inventory.pop()
                game_log.remove_last_event()
                game.current_location_id = game_log.last.id_num

        else:
            # Handle non-menu actions
            result = location.available_commands[choice]
            game.current_location_id = result
            if choice[:6] == "pickup":
                if location.items[0] not in inventory:
                    inventory.append(location.items[0])
            elif choice == "submit project":
                submit_project()
            elif choice == "call reciption":
                call_recepton()
            elif choice == "unlock the computer":
                unlock_computer()
            elif choice == "enter robarts from backdoor":
                print(
                    "The backdoor is locked. You knocked, but no one answered. Try entering through the front door on St. George.")
            elif choice == "face social anxiety and enter":
                social_anxiety()
            elif choice == "play with them":
                play_with_them()
            elif choice == "get 10 extra moves":
                moves += 10
            elif choice == "use back door":
                backdoor()

            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game
