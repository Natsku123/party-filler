from typing import Union
from core.database.models import Player, PlayerShort


def discord_avatar_url(
    player: Union[Player, PlayerShort], support_gifs: bool = False, size: int = None
) -> str:
    """
    Compile Discord avatar url based on Player information

    :param player: Player object
    :param support_gifs: If GIFs are supported
    :param size: Desired size of image, can be any power of two between 16 and 4096
    :return: Player avatar url
    """
    base_url = "https://cdn.discordapp.com"
    return f"{base_url}/{f'avatars/{player.discord_id}' if player.icon else 'embed/avatars'}/{player.icon if player.icon else player.discriminator % 5}.{'gif' if support_gifs and player.icon and player.icon.startswith('a_') else 'png'}{f'?size={size}' if size else ''}"
