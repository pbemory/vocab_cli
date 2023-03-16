import argparse
from vocab_cli import app, __version__


def parse_args():
    """Parse args with argparse."""
    parser = argparse.ArgumentParser(description = 'cli tool for building vocab from a word bank.')
    parser.add_argument('-v','--version', action='version', version=f"Version {__version__}")
    parser.add_argument('-wb', help='specify a path to your word_bank.')
    args = parser.parse_args()
    return args


def main():
    """Launch app with args."""
    args = parse_args()
    app.launch(args.wb)


if __name__ == '__main__':
    main()
