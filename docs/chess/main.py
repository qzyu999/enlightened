import sys
import os

# Add the project root to sys.path to ensure absolute imports work correctly
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from chess.ui.cli import ChessCLI

def main():
    cli = ChessCLI()
    cli.run()

if __name__ == "__main__":
    main()
