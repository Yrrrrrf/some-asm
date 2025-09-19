# Global Settings for the application

# ? Imports -------------------------------------------------------------------------------------

from enum import Enum

# ? Globals -------------------------------------------------------------------------------------


class Config(Enum):
    """
    Project Config
    """

    # App info
    NAME = "Some Assembly"
    VERSION = "v0.1.0"
    AUTHOR = "Yrrrrrf"

    # App settings
    WIDTH = 1080
    HEIGHT = 720
    # FPS = 60  # frames per second
    TILE_SIZE = 32  # tile size in pixels
    ANIMATION_SPEED = 8  # seconds


class Assets(Enum):
    """
    Assets paths
    """

    # todo: Check if this works properly on a UNIX system (Linux, MacOS, etc.)
    # * Probably not because of the backslash. It should be a forward slash
    # * So, I'll have to change it to a forward slash
    ICONS = "resources/img/static/"
    ASM_DOCS = "resources/asm/"
    THEMES = "resources/themes/"
    COLOR_SCHEMA = "resources/colors/"

    # todo: Check why using `str` as the type of the last enum value is causing an error
    # COLOR_SCHEMA: str = "resources/color_schemes/"
    # Fonts
    # Sounds
    # Music
    # Videos
    # Animations
    # Other
    # ...


# @dataclass
# class Theme(Enum):
#     LIGHT = ("Light Theme", (255, 255, 255), (191, 191, 191), (255, 0, 0), "assets/fonts/Roboto-Regular.ttf")
#     DARK = ("Dark Theme", (0, 0, 0), (63, 63, 63), (255, 0, 0), "assets/fonts/Roboto-Regular.ttf")
#     DARK_PLUS = ("Dark+ Theme", (0, 0, 0), (31, 31, 31), (255, 0, 0), "assets/fonts/Roboto-Regular.ttf")
#     DEBUG = ("Debug Theme", (255, 0, 0), (0, 0, 0), (255, 0, 0), "Consolas")


#     # title: str
#     main_color: tuple
#     secondary_color: tuple
#     highlight_color: tuple
#     font: str


#     def __init__(self, main_color, secondary_color, highlight_color, font):
#         # use the name of the enum as the title but in title case
#         self.title = self.name.title()
#         self.main_color = main_color
#         self.secondary_color = secondary_color
#         self.highlight_color = highlight_color
#         self.font = font
