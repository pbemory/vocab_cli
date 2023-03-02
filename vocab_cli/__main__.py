from vocab_cli import app, __version__
import sys
import argparse

def main(word_bank_path: str):
    """Entry point script for launching vocab_cli."""
    app.launch(word_bank_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'cli tool for building vocab from a word bank.')
    parser.add_argument('-v','--version', action='version', version=f"Version {__version__}")
    parser.add_argument('-wb', help='specify a path to your word_bank.')
    args = parser.parse_args()
    wb_path = "" if args.wb is None else args.wb
    main(wb_path)
