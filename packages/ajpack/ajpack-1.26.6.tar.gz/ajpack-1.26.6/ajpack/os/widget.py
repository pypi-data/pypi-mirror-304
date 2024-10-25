import pystray  #type:ignore
from pystray import Icon, Menu, MenuItem  #type:ignore
from PIL import Image
from typing import Callable, Any

def show_status_icon(iconPath: str, title: str, funcArgs: tuple, customExitFunction: Callable[[Any], Any]|None = None, addMenuItems: list[MenuItem] = [], useDefault: bool = True) -> None:
    """
    Show a status icon in the system tray.

    :param iconPath (str): The image path to use as icon.
    :param title (str): The title of the icon.
    :param addMenuItems (list[pystray.MenuItem]): A list of menu items to add to the default list.
    :param useDefault (bool): Whether to use the default menu items or not. (addMenuItems won't be removed)
    """

    # Load the icon image
    image = Image.open(iconPath)

    # Create the icon
    icon = Icon(title, image, title, Menu())

    # Create a menu
    def exit_icon():
        if not customExitFunction:
            icon.stop()
        else:
            customExitFunction(*funcArgs)

    if useDefault:
        menuItems = addMenuItems + [
            MenuItem("EXIT", exit_icon)
        ]
    else:
        menuItems = addMenuItems

    icon.menu = Menu(*menuItems)


    # Run the icon in the background
    icon.run()
