class Game:
    def __init__(self, dm):
        self.__dungeon_master = dm
        self.game_rules = {}

    def get_dm(self):
        return self.__dungeon_master

    def set_dm(self, dm_id):
        self.__dungeon_master = dm_id
