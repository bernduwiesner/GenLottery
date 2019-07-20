#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
"""Useful PySimpleGUI functions

"""

import PySimpleGUI as sg


def popup_window(title: str = "Error", text: str = "") -> None:
    """

    :param title: the window title defaults to 'Error'
    :param text:  A message to display in the window
    :return: None
    """
    sg.Popup(title + ": " + text, title=title, font=("Helvetica", 16, "italic"))
