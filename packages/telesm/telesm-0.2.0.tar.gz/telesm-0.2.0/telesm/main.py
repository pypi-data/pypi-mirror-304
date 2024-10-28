#!/usr/bin/env python3

import nltk
from nltk.corpus import wordnet as wn
import argparse
import os
import curses
from telesm.db import Database
from telesm.ai import Ai

DB_FILE = os.path.expanduser('~/.telesm.db')
db = Database(DB_FILE)


def format_word_with_definition_and_examples(word, definition, examples=[]):
    if examples:
        formatted_examples = "\n".join(
            f"\t⁃ {example}" for example in examples)
        examples_text = f"\nExamples:\n{formatted_examples}"
    else:
        examples_text = ""

    return f"{word}:\n\t‣ {definition}{examples_text}"


def display_words_with_navigation(saved_words):
    def navigate_words(stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        current_index = 0
        total = len(saved_words)

        while True:
            stdscr.clear()
            word, definition, examples = saved_words[current_index]
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(0, 0, f"{word}:")
            stdscr.addstr(1, 4, f"{definition[:curses.COLS - 1]}")
            if examples:
                stdscr.addstr(2, 0, "Examples:")
                for i, example in enumerate(examples):
                    stdscr.addstr(3+i, 4, f"- {example}")
            stdscr.attroff(curses.color_pair(1))
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(curses.LINES - 3, 0, f"({current_index+1}/{total})")
            stdscr.addstr(curses.LINES - 2, 0,
                          "Press 'J' to move down, 'K' to move up, 'Q' to quit.")
            stdscr.attroff(curses.color_pair(2))
            stdscr.refresh()

            key = stdscr.getch()

            if key == ord('j') and current_index < len(saved_words) - 1:
                current_index += 1
            elif key == ord('k') and current_index > 0:
                current_index -= 1
            elif key == ord('q'):
                break
    curses.wrapper(navigate_words)


def get_word_definition(word, from_ai=False):
    from_database = db.get_by_word(word)
    if from_database:
        (word, definition, examples) = from_database
    else:
        if from_ai:
            try:
                response, examples, status = Ai().get_definition(word)
                if status == 200:
                    return response, examples
                else:
                    return None
            except Exception as e:
                print(e)
                exit(1)
        nltk.download('wordnet', quiet=True)
        synsets = wn.synsets(word)
        if not synsets:
            return False, None
        definition = synsets[0].definition()
        examples = synsets[0].examples()
    return definition, examples


def parse_args():
    parser = argparse.ArgumentParser(
        description='Get the definition of a word')
    parser.add_argument('word', nargs='?', type=str, help='The word to define')
    parser.add_argument('--list', action='store_true',
                        help='List all saved words')
    parser.add_argument('--navigate', action='store_true',
                        help='Navigate through saved words')
    parser.add_argument('--no-save', action='store_true',
                        help='Do not save the searched word in the database')
    parser.add_argument('--random', action='store_true',
                        help='Display a random word from the database')
    parser.add_argument('--delete', type=str,
                        help='Deletes a word', metavar="<string>")
    parser.add_argument(
        '--search', type=str, help='Full-Text search for a keyword in the database, including word, its definition and exampes', metavar='<string>')
    parser.add_argument(
        '--ai', type=str, help='Use OpenAPI to show the definition and etymology of the word (requires internet connection)'
    )
    return parser.parse_args()


def print_considering_navigation(words, should_navigate=True):
    if should_navigate:
        display_words_with_navigation(words)
    else:
        for word, definition, examples in words:
            print(format_word_with_definition_and_examples(
                word, definition, examples))
            print("---")


def main():
    args = parse_args()
    if args.list:
        saved_words = db.list_words()
        if not saved_words:
            print("No words saved yet.")
            exit(0)
        else:
            print_considering_navigation(
                saved_words, should_navigate=args.navigate)
    elif args.word:
        definition, examples = get_word_definition(args.word.strip().lower())
        if definition == False:
            print(f"No definition found for '{args.word}'")
            exit(0)
        print(format_word_with_definition_and_examples(
            args.word, definition, examples))
        if not args.no_save:
            db.save_word(args.word, definition, examples)
    elif args.random:
        random_word = db.get_random_word()
        if not random_word:
            print("No word could be found in the database.")
            exit(0)
        print(format_word_with_definition_and_examples(
            random_word[0], random_word[1], random_word[2]))
    elif args.delete:
        try:
            db.delete_word(args.delete)
            print(f"'{args.delete}' is deleted.")
            exit(0)
        except Exception:
            print("An unexpected error occured. Please try again.")
            exit(1)
    elif args.search:
        words = db.search(args.search)
        if not words:
            print(f"Nothing found for '{args.search}'.")
            exit(0)
        else:
            print_considering_navigation(words, should_navigate=args.navigate)
    elif args.ai:
        definition, examples = get_word_definition(args.ai, from_ai=True)
        if definition:
            print(format_word_with_definition_and_examples(args.ai, definition, examples))
            if not args.no_save:
                db.save_word(args.ai, definition, examples)
            exit(0)
        print("Something went wrong. Please try again later.")
        exit(1)