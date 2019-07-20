#
#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
""" Display the lottery numbers in a window either generated
    or retrieved from a file
"""

from typing import List

import PySimpleGUI as sg

import constants as C


def results_window(lottery: str, msg: str, results: C.Results) -> None:
    """Display lottery numbers in a window

    :param lottery: the name of the type of lottery
    :param msg: text to display
    :param results: the numbers generated or retrieved from file
    :return: None
    """
    layout: List = [[sg.Text(text=f"{lottery}")]]
    for line, _ in enumerate(results):
        # for line in range(len(results)):
        x_1, x_2 = results[line]
        d_1 = ", ".join(x_1)
        if x_2[0] is None:
            d_2 = ""
        else:
            d_2 = " - " + ", ".join(x_2)
        layout.append([sg.Text(text=f"Line {line+1}: {d_1}{d_2}")])
    layout.append([sg.Text(text=f"{msg or ''}")])
    layout.append([sg.OK()])

    window = sg.Window(
        title="Lottery number Generator Results",
        layout=layout,
        text_justification=C.GUI_JUSTIFY,
        font=(C.GUI_FONT_NAME, C.GUI_FONT_SIZE),
    )

    while True:
        event, _ = window.Read()
        if event == "OK" or event is None:
            window.Close()
            break
