#!/usr/bin/env python3
#
#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
"""Generate random numbers for all current UK lottery games

    Optionally save the numbers

"""

from typing import Any, List, Optional
import argparse
import shelve
import time
import pathlib
import random

import gui_arguments
import gui_results
from gui_utility import popup_window
import constants as C

if __name__ == "__main__":

    def process_arguments() -> argparse.Namespace:
        """Process command line arguments

        :return: args - Namespace containing the key: value pairs of
                        arguments supplied on the command line
        """
        arg_parse = argparse.ArgumentParser(
            description="Script which generates random lottery numbers",
            epilog="NOTE: --delete, --no_save, --print and --version are"
            " mutually exclusive",
        )

        arg_parse.add_argument(
            "-t",
            "--type",
            type=str.upper,
            nargs="?",
            dest="lottery_type",
            default=C.DEFAULT_TYPE,
            action="store",
            choices=C.LOTTERY_TYPES,
            help=f"type is the type of lottery to"
            f" generate numbers for."
            f" default=%(default)s",
        )
        arg_parse.add_argument(
            "-l",
            "--lines",
            type=int,
            nargs="?",
            dest="number_of_lines",
            default=C.DEFAULT_LINES,
            action="store",
            help=f"lines is the number of lottery"
            f" lines to generate."
            f" min={C.MIN_LINES}, max={C.MAX_LINES}"
            f" default=%(default)s",
        )
        arg_parse.add_argument(
            "--text", action="store_true", help="display in the terminal"
        )

        group = arg_parse.add_mutually_exclusive_group(required=False)

        group.add_argument(
            "-d",
            "--delete",
            action="store_true",
            help=f"delete a saved file, use --type"
            f" (default={C.DEFAULT_TYPE}) to"
            f" determine which file to delete"
            f" cannot be used with --no_save or --print",
        )
        group.add_argument(
            "-n",
            "--no_save",
            action="store_true",
            help=f"do NOT save results to a file,"
            f" cannot be used with --delete or --print",
        )
        group.add_argument(
            "-p",
            "--print",
            action="store_true",
            help=f"show previously saved data, use --type"
            f" (default={C.DEFAULT_TYPE}) to choose"
            f" the type of saved file to display,"
            f" cannot be used with --delete or --no_save",
        )

        group.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"{C.VERSION.name}" f" Version: {C.VERSION.version}",
        )

        args: argparse.Namespace = arg_parse.parse_args()

        if args.number_of_lines < C.MIN_LINES or args.number_of_lines > C.MAX_LINES:
            arg_parse.error(
                f" -l (--lines) {args.number_of_lines}"
                f" is invalid."
                f" The valid range is"
                f" {C.MIN_LINES}-{C.MAX_LINES}"
            )
        return args

    def generate_numbers() -> C.Results:
        """Generate several random numbers and optionally save them

        :return: a dictionary containing a line number as a key and a tuple
                 of results as part1 list and part2 list
        """

        def add_leading_zero(values: List) -> List:
            """Add a leading zero to numbers in the list < 10

            :param values: list of numbers
            :return: array containing formatted numbers
            """
            return sorted([f"{v:02d}" for v in values])

        def choose_numbers(maximum: int, quantity: int) -> List[str]:
            """Generate the random numbers required

            :param maximum: the highest number to choose from
            :param quantity: the number of numbers to generate
            :return: a sorted list of generated numbers
            """
            valid_range: range = range(C.RULE_START, maximum)
            return add_leading_zero(random.sample(valid_range, quantity))

        main_max, main_qty, extra_max, extra_qty = C.RULES[OPTIONS.lottery_type]

        shelf = None
        # if --no_save is specified then OPTIONS.no_save will be True
        # if no_save is false, then save
        if OPTIONS.no_save:
            if OPTIONS.text:
                print("These generated numbers have not been saved")
        else:
            directory = pathlib.Path(C.SAVE_FILE_DIR)
            if not directory.exists():
                directory.mkdir(parents=True)
            shelf = shelve.open(filename=SAVED_FILE, protocol=C.SHELF_PROTOCOL)
            shelf[C.SHELF_ARGS["DATE"]] = time.time()
            shelf[C.SHELF_ARGS["TYPE"]] = OPTIONS.lottery_type
            shelf[C.SHELF_ARGS["LINES"]] = OPTIONS.number_of_lines

        # count the actual number of lines generated
        count: int = 0
        res: C.Results = {0: ([""], [""])}
        # generate the required number of lines
        for _ in range(OPTIONS.number_of_lines):
            # x_1 holds the first group of numbers generated
            # main_max is the the highest number to generate plus 1
            # main_qty is the quantity of numbers to generate each line
            x_1: List[str] = choose_numbers(maximum=main_max, quantity=main_qty)
            if OPTIONS.text:
                print(f"{OPTIONS.lottery_type}: {x_1}", end="")

            # x_2 holds the secondary group of numbers generated if
            # any are required
            # extra_max is the the highest number to generate plus 1
            # extra_qty is the quantity of numbers to
            # generate in each line
            x_2: Optional[List[Any]] = [None]
            # only generate the second group of numbers if required
            # if extra_qty > 0
            if extra_qty:
                x_2 = choose_numbers(maximum=extra_max, quantity=extra_qty)
                if OPTIONS.text:
                    print(f"-{x_2}")
            else:
                # stop subsequent printing on the same line
                if OPTIONS.text:
                    print("")
            # If shelf is None it means no_save was specified
            if shelf is not None:
                shelf[C.SHELF_ARGS["PART1"] + str(count)] = x_1
                # Save the extra numbers even if there are none to save
                # will return None on subsequent reading
                shelf[C.SHELF_ARGS["PART2"] + str(count)] = x_2

            res[count] = (x_1, x_2)
            count += 1

        # close the save file if there is one
        if not OPTIONS.no_save and shelf is not None:
            shelf.close()

            if OPTIONS.text:
                print(
                    f"The numbers have"
                    f"{' not' if OPTIONS.no_save else ''}"
                    f" been saved and {count} lines were generated"
                )
        return res

    def delete_saved_file() -> None:
        """Delete a previously saved file

        :return: None
        """
        # add the filename extension
        file_name = SAVED_FILE + C.SAVE_FILE_TYPE
        path = pathlib.Path(file_name)
        file_exists = path.exists()
        if file_exists:
            path.unlink()
        msg = f"File: <{file_name}> was" f" {'deleted' if file_exists else 'not found'}"

        if OPTIONS.text:
            print(msg)

    def show_saved() -> None:
        """Display a previously generated and saved batch of numbers

        :return: None
        """
        # add the filename extension
        path = pathlib.Path(SAVED_FILE + C.SAVE_FILE_TYPE)
        results: C.Results = {0: ([""], [""])}
        if path.exists() and path.is_file():
            x_1: List[str]
            x_2: List[Optional[str]]
            shelf = shelve.open(
                filename=SAVED_FILE, flag=C.SHELF_READONLY, protocol=C.SHELF_PROTOCOL
            )
            save_time = time.localtime(shelf[C.SHELF_ARGS["DATE"]])
            msg: str = f"Saved on {time.strftime(C.DATE_FORMAT, save_time)}"
            if OPTIONS.text:
                print("Displaying a previously saved set")
                print(msg)
            count = 0
            for line in range(shelf[C.SHELF_ARGS["LINES"]]):
                # Don't display second group if none exist
                x_1 = shelf[C.SHELF_ARGS["PART1"] + str(line)]
                x_2 = shelf[C.SHELF_ARGS["PART2"] + str(line)] or [""]
                if OPTIONS.text:
                    print(
                        f"SAVED {shelf[C.SHELF_ARGS['TYPE']]}"
                        f" Line {line + 1}:"
                        f" {x_1[line]}"
                        f" {x_2[line]}"
                    )
                else:
                    results[line] = (x_1, x_2)
            if OPTIONS.text:
                print(f"{count} lines recovered")
            else:
                gui_results.results_window(OPTIONS.lottery_type, msg, results)

            shelf.close()
        else:
            msg = f"{OPTIONS.lottery_type} file <{path}> is missing"
            if OPTIONS.text:
                print(msg)
            else:
                popup_window(text=msg)

    # Main body
    OPTIONS = process_arguments()

    while True:
        # An event returns the key name of the caller
        EVENT = ""
        # only generate a gui interface if not excluded by the --text argument
        if not OPTIONS.text:
            # create the GUI interface and return the event
            # and the chosen options
            EVENT, OPTIONS = gui_arguments.arguments_window(OPTIONS)

        # Do nothing if the user exits without wanting to continue
        if EVENT != "Cancel" and EVENT is not None:
            # This is the save file path name with no extension
            SAVED_FILE = C.SAVE_FILE_DIR + OPTIONS.lottery_type
            if OPTIONS.delete:
                delete_saved_file()
            elif OPTIONS.print:
                show_saved()
            else:
                generated: C.Results = generate_numbers()
                if OPTIONS.text:
                    break
                else:
                    gui_results.results_window(OPTIONS.lottery_type, "", generated)
        else:
            break
