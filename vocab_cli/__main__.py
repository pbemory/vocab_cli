from vocab_cli import app
import sys

def main():
    args = sys.argv[1:]
    app.launch(args)

if __name__ == '__main__':
    main()
