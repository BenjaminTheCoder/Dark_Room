class Item:

    def __init__(self, name: str, description: str = "") -> None:
       self._name = name
       self._description = description 

    def describe(self) -> None:
        print(f"  - {self._name}: {self._description}")


class BassClarinetCase(Item):

    def __init__(self, name: str, description: str = "") -> None:
        super().__init__(name, description) 
        self._is_open = False

    def open(self) -> None:
        self._is_open = True

    def close(self) -> None:
        self._is_open = False

    def describe(self) -> None:
        open_txt = "The case is open." if self._is_open else "The case is closed."
        print(f"  - {self._name}: {self._description} -- {open_txt}")

class RubiksCube(Item):

    def __init__(self, name: str, description: str = "") -> None:
        super().__init__(name, description) 
        self._is_corner_twisted = False

    def twist(self) -> None:
        self._is_corner_twisted = True

    def untwist(self) -> None:
        self._is_corner_twisted = False

    def describe(self) -> None:
        twisted_txt = "The corner is twisted." if self._is_corner_twisted else "The corner is not twisted."
        print(f"  - {self._name}: {self._description} -- {twisted_txt}")



class Room:
    
    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self.items: list[Item] = []

    def add_item(self, item: Item) -> None:
        if item._name not in [i._name for i in self.items]:
            self.items.append(item)

    def describe(self) -> None:
        print(f"{self.name}: {self.description}")
        if len(self.items) > 0:
            print("Items:")
            for item in self.items:
                item.describe()

if __name__ == "__main__":

    bens_room = Room("Ben's room", "Ben's messy room.")
    bass_clarinet_case = BassClarinetCase("Bass Clarinet Case", "A large, heavy, black, and worn case.")
    bass_clarinet_case.open()
    rubiks_cube_1 = RubiksCube("Rubik's Cube 1", "A GAN Rubik's cube.")
    rubiks_cube_1.twist()
    rubiks_cube_2 = RubiksCube("Rubik's Cube 2", "A GAN Rubik's cube.")
    rubiks_cube_2.untwist()    
    bens_room.add_item(bass_clarinet_case)
    bens_room.add_item(rubiks_cube_1)
    bens_room.add_item(rubiks_cube_2)
    bens_room.describe()
