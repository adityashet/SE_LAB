import random

DEFAULT_ROWS = 6
DEFAULT_COLS = 6
DEFAULT_MINES = 6


class Board:
    def __init__(self, rows=DEFAULT_ROWS, cols=DEFAULT_COLS, mines=DEFAULT_MINES):
        self.rows = rows
        self.cols = cols
        self.mine_total = mines
        self.mines = self._build_mines()
        self.revealed = set()
        self.flags = set()
        self.last_revealed_count = 0

    @classmethod
    def from_difficulty(cls, mode):
        modes = {
            "easy": (8, 8, 10),
            "medium": (12, 12, 25),
            "hard": (16, 16, 40),
        }
        config = modes.get(str(mode).lower(), (8, 8, 10))
        return cls(*config)

    def _build_mines(self):
        cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        return set(random.sample(cells, self.mine_total))

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if self.in_bounds(nr, nc):
                    yield nr, nc

    def adjacent_mines(self, r, c):
        return sum(pos in self.mines for pos in self.neighbors(r, c))

    def reveal(self, start):
        if not self.in_bounds(*start):
            self.last_revealed_count = 0
            return False
        before_count = len(self.revealed)
        stack = [start]
        hit_mine = False
        while stack:
            pos = stack.pop()
            if pos in self.revealed or pos in self.flags:
                continue
            r, c = pos
            self.revealed.add(pos)
            if pos in self.mines:
                hit_mine = True
                continue
            if self.adjacent_mines(r, c) == 0:
                stack.extend(n for n in self.neighbors(r, c) if n not in self.revealed)
        self.last_revealed_count = len(self.revealed) - before_count
        return hit_mine


    def toggle_flag(self, pos):
        if not self.in_bounds(*pos):
            return False
        if pos in self.revealed:
            return False
        if pos in self.flags:
            self.flags.remove(pos)
        else:
            self.flags.add(pos)
        return True

    def won(self):
        non_mines = {(r, c) for r in range(self.rows) for c in range(self.cols)} - self.mines
        return self.revealed == non_mines

