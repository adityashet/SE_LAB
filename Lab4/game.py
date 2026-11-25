from board import Board


class Minesweeper:
    def __init__(self, board=None):
        self.board = board

    def select_difficulty(self):
        print("Select difficulty:")
        print("1. Easy (8x8, 10 mines)")
        print("2. Medium (12x12, 25 mines)")
        print("3. Hard (16x16, 40 mines)")
        while True:
            choice = input("Choice (1-3 or easy/medium/hard) [1]: ").strip().lower()
            if choice in {"", "1", "easy", "e"}:
                return Board.from_difficulty("easy")
            elif choice in {"2", "medium", "m"}:
                return Board.from_difficulty("medium")
            elif choice in {"3", "hard", "h"}:
                return Board.from_difficulty("hard")
            print("Invalid choice. Please enter 1, 2, or 3.")

    def display(self, reveal_mines=False):
        b = self.board
        print("\n   " + "".join(f"{c + 1:2}" for c in range(b.cols)))
        for r in range(b.rows):
            cells = []
            for c in range(b.cols):
                pos = (r, c)
                if reveal_mines and pos in b.mines:
                    ch = "*"
                elif pos in b.flags:
                    ch = "F"
                elif pos not in b.revealed:
                    ch = "#"
                elif pos in b.mines:
                    ch = "*"
                else:
                    ch = str(b.adjacent_mines(r, c))
                cells.append(ch)
            print(f"{r + 1:2} " + " ".join(cells))

    def run(self):
        print("Minesweeper")
        if self.board is None:
            self.board = self.select_difficulty()
        print("Commands: r row col | f row col | q")
        while True:
            self.display()
            raw = input("> ").strip().lower()
            if raw == "q":
                return
            parts = raw.split()
            if len(parts) != 3 or parts[0] not in {"r", "f"}:
                print("Use r row col or f row col.")
                continue
            try:
                r, c = int(parts[1]) - 1, int(parts[2]) - 1
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not self.board.in_bounds(r, c):
                print("Outside the board.")
                continue

            if parts[0] == "f":
                if self.board.toggle_flag((r, c)):
                    status = "Flagged" if (r, c) in self.board.flags else "Unflagged"
                    print(f"{status} cell ({r + 1}, {c + 1}).")
                else:
                    print(f"Cannot flag revealed cell ({r + 1}, {c + 1}).")
                continue

            if self.board.reveal((r, c)):
                self.display(reveal_mines=True)
                print("BOOM! You hit a mine.")
                return

            count = getattr(self.board, "last_revealed_count", 0)
            if count == 0:
                print(f"Cell ({r + 1}, {c + 1}) is already revealed or flagged.")
            elif count == 1:
                print(f"Revealed 1 cell at ({r + 1}, {c + 1}).")
            else:
                print(f"Revealed {count} cells starting at ({r + 1}, {c + 1}).")

            if self.board.won():
                self.display()
                print("You cleared the board!")
                return

