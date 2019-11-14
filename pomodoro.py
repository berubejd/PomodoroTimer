#!/usr/bin/env python3.8

import argparse
import time

from progressbar import progress_bar

def setup_arguments():
    # Setup command line argument parsing
    parser = argparse.ArgumentParser()
    parser.version = '1.1'

    parser.add_argument('-n', '--name', action='store', type=str, default='My Pomodoro Task', metavar='text', help="The name to assign to this task")
    parser.add_argument('-p', '--pomodoro', action='store', type=int, default=25, metavar='minutes', help="The length of each pomodoro in minutes")
    parser.add_argument('-c', '--count', action='store', type=int, default=4, metavar='number', help="The number of pomodoros to complete")
    parser.add_argument('-s', '--short-break-duration', action='store', type=int, default=5, metavar='minutes', help="The length of each short break in minutes")
    parser.add_argument('-l', '--long-break-duration', action='store', type=int, default=15, metavar='minutes', help="The length of each long break in minutes")
    parser.add_argument('-v', '--version', action='version', help="Show the version number and exit")
    parser.add_argument('-d', '--debug', action='store_true', help="Sets low timers for testing")

    args = parser.parse_args()

    # Reset timers if debug option was used
    if args.debug:
        args.pomodoro = .5
        args.short_break_duration = .1
        args.long_break_duration = .2

    return args

def wait_input(suppress: bool = False) -> None:
    """ Simple function to draw the users attention and request input in order to continue or quit.
        Set 'suppress' in order to keep from adding an additional line after input.
    """
    response = input("\aPress ENTER to continue or type 'Quit' to exit... ")

    if response.lower() == 'quit':
        exit()

    if not suppress:
        print()

def timer(seconds: int, prefix: str) -> None:
    """ Simplify usage of progress_bar since many of the options are going to be the same throughout"""
    remaining = seconds

    while True:
        progress = remaining / seconds * 100
            
        progress_bar(progress = progress, length = 20, complete = 0, msg_complete = 'Time is up!', msg_prefix = prefix + f' ({time.strftime("%M:%S", time.gmtime(remaining))} remaining): ', suppress_nl = True)
        time.sleep(1)
            
        remaining -= 1

        if remaining < 0:
            break

def schedule_break(break_type: str, break_duration: int) -> None:
    """Schedule a 'short' or 'long' break for a set number of minutes"""
    wait_input() if break_type == 'long' else test_input(True)

    duration = break_duration * 60
    prefix = f"{break_type.capitalize()} Break{' ' if break_type == 'long' else ''}"

    timer(duration, prefix)

def display_header(args) -> None:
    # Output to user the parameters for the coming Pomodoro Timer
    print()
    print(f'{args.name}')
    print(f'{"-" * len(args.name)}')
    print(f'Starting "{args.name}" with {args.count} pomodoros of {args.pomodoro} minutes each.  There will be a {args.short_break_duration} minute break between each pomodoro and a {args.long_break_duration} minute break after every 4 pomodoros.')
    print()

    wait_input()

def main(args) -> None:
    # Display initial message
    display_header(args)

    # Start the timer process
    for count, interval in enumerate(range(1, args.count + 1), 1):

        # Set up and generate the Pomodoro timer
        duration = args.pomodoro * 60
        prefix = f'Pomodoro {count} '

        timer(duration, prefix)

        if not count == args.count:

            if interval % 4 == 0:
                # Time for long break
                schedule_break('long', args.long_break_duration)
            else:
                # Time for short break
                schedule_break('short', args.short_break_duration)

            # Alert that it is time for the next pomodoro
            print('\a', end='')

        else:
            print(f'\a\n\nCongratulations!  You have just completed the "{args.name}" pomodoro!\n')

if __name__ == '__main__':
    args = setup_arguments()
    main(args)
