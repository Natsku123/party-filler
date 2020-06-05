import json


class DatabaseStatus:
    """Database status object"""
    def __init__(self, status: bool, message: str = ""):
        self.__status = status
        self.__message = message

    def get_status(self):
        """
        Get status boolean
        :return: True or False
        """
        return self.__status

    def get_message(self):
        """
        Get status message
        :return: String message
        """
        return self.__message


class DatabaseError(DatabaseStatus):
    """Database error object"""
    def __init__(self, message: str = ""):
        super().__init__(False, message)


class DatabaseItem:
    """Generic Database item"""

    def __init__(self, item):
        """
        Generic constructor
        :param item: item object
        """
        self.__id = item.get('id')
        self.__item = item

    def get_id(self):
        """
        Get ID of item
        :return: ID of item integer
        """
        return self.__id

    def to_json(self):
        """
        Return json of object
        :return: json string
        """
        return json.dumps(self.__item)

    def to_dict(self):
        """
        Return dict of object
        :return: dict of object
        """
        return self.__item


class Server(DatabaseItem):
    """Server object"""
    def __init__(self, item):
        """Server constructor"""
        self.__name = item.get('name')
        self.__discord_id = item.get('discord_id')

        super().__init__(item)

    def get_name(self):
        """
        Return server name
        :return: Server name string
        """
        return self.__name

    def get_discord_id(self):
        """
        Return discord id
        :return: discord id string
        """
        return self.__discord_id


class Channel(DatabaseItem):
    """Channel object"""
    def __init__(self, item):
        """
        Channel constructor
        :param item: channel object
        """
        self.__name = item.get('name')
        self.__discord_id = item.get('discord_id')
        self.__server_id = item.get('server_id')

        super().__init__(item)

    def get_name(self):
        """
        Return channel name
        :return:
        """
        return self.__name

    def get_discord_id(self):
        """
        Return discord id
        :return: Discord id string
        """
        return self.__discord_id

    def get_server_id(self):
        """
        Return server id
        :return: Server id int
        """
        return self.__server_id


class Player(DatabaseItem):
    """Player object"""
    def __init__(self, item):
        """
        Player constructor
        :param item: player object
        """
        self.__discord_id = item.get('discord_id')

        super().__init__(item)

    def get_discord_id(self):
        """
        Get Discord ID of player
        :return: Discord ID of player string
        """
        return self.__discord_id


class Role(DatabaseItem):
    """Role object"""
    def __init__(self, item):
        self.__party_id = item.get('party_id')
        self.__name = item.get('name')
        self.__max_players = item.get('max_players')

        super().__init__(item)

    def get_name(self):
        """
        Get name of role
        :return: Role name
        """
        return self.__name

    def get_party_id(self):
        """
        Get party id
        :return: Party ID integer
        """
        return self.__party_id

    def get_max_players(self):
        """
        Get maximum players for a role
        :return: Maximum players integer
        """
        return self.__max_players


class Party(DatabaseItem):
    """Party object"""
    def __init__(self, item):
        """
        Party constructor
        :param item: Party object
        """
        self.__title = item.get('title')
        self.__game = item.get('game')
        self.__max_players = item.get('max_players')
        self.__description = item.get('description')
        self.__notify_channel = item.get('notify_channel')
        self.__players = {}
        self.__roles = []

        super().__init__(item)

    def get_title(self):
        """
        Get title of party
        :return: Title of party string
        """
        return self.__title

    def get_game(self):
        """
        Get game of party
        :return: Game of party string
        """
        return self.__game

    def get_max_players(self):
        """
        Get maximum players of party
        :return: Maximum players of party integer
        """
        return self.__max_players

    def get_description(self):
        """
        Get description of party
        :return: Description of party string
        """
        return self.__description

    def get_notify_channel(self):
        """
        Get notify channel
        :return: Channel ID int
        """
        return self.__notify_channel

    def get_players(self):
        """
        Get players of party
        :return: Dict of player objects and roles
        """
        return self.__players

    def get_roles(self):
        """
        Get roles of party
        :return: List of role objects of party
        """
        return self.__roles

    def add_player(self, player: Player, role: Role = None):
        """
        Add player into party
        :param player: Player object
        :param role: Role object (None if no role)
        :return:
        """
        self.__players[player] = role

    def add_role(self, role: Role):
        """
        Add role into party
        :param role: Role object
        :return:
        """
        self.__roles.append(role)

    def remove_player(self, player: Player):
        """
        Remove player from party
        :param player: Player object
        :return:
        """
        del self.__players[player]

    def remove_role(self, role: Role):
        """
        Remove role into party
        :param role: Role object
        :return:
        """
        self.__roles.remove(role)


