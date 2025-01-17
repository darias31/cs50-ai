import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=96, width=96, mines=16):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        if len(self.cells) == self.count:
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        try:
            self.cells.remove(cell)
            self.count -= 1
        except KeyError:
            pass

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        try:
            self.cells.remove(cell)

        except KeyError: # when it's already been removed
            pass


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        print("\n\n")

        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add new sentence to AI's knowledge base based on value of cell and count

        neighbor_cells = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor_cells.add((i,j))

        new_sentence = Sentence(neighbor_cells - self.safes, count)

        # append only if we don't know for sure it's a safe/mine
        if count > 0:
            self.knowledge.append(new_sentence)
        else:
            for cell_tuple in new_sentence.cells:
                self.mark_safe(cell_tuple)
        
        # to prevent any potental infinite loops
        len_knowledge = len(self.knowledge)

        if len_knowledge > 0: # I'm too scared to remove this line of code
            for i in range(len_knowledge):
                
                if i < len(self.knowledge):
                    sentence1 = self.knowledge[i]

                    print(f"Index {i} of knowledge: {sentence1.cells} & count: {sentence1.count}")

                    for j in range(len_knowledge):


                        if j < len(self.knowledge):
                            sentence2 = self.knowledge[j]

                            if ((i != j) and (sentence1.cells == sentence2.cells)) or (len(sentence2.cells) == 0):
                                self.knowledge.pop(j)
                                print("\tRemoving duplicates and empty sets...")
                                break
                            else:
                                # check for definite mines and definite safes (could use the Sentence class method for this btw)
                                if sentence2.count == 0:

                                    sentence2_cells_list = list(sentence2.cells)

                                    print(f"\tThese are all safes: {sentence2.cells}, {sentence2.count}")

                                    for i in sentence2_cells_list:
                                        self.mark_safe(i)

                                    
                                elif sentence2.count == len(sentence2.cells):
                                    
                                    sentence2_cells_list = list(sentence2.cells)

                                    print(f"\tThese are all mines: {sentence2.cells}, {sentence2.count}")

                                    for i in sentence2_cells_list:
                                        self.mark_mine(i)
                                        
                                # derive new knowledge by finding proper subsets
                                elif (i != j) and (len(sentence1.cells) > 0) and (sentence1.cells.issubset(sentence2.cells)):
                                    print(f"\tSentence1: {sentence1.cells}")
                                    print(f"\tSentence2: {sentence2.cells}")
                                    print("\tCombining the sentences above...")

                                    self.knowledge.append(Sentence(sentence2.cells - sentence1.cells,sentence2.count - sentence1.count))
                                    self.knowledge.pop(j)
                                    print("\tDeriving new knowledge and removing some redundant sets...")
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        safe_moves = self.safes - self.moves_made

        print(f"known mines: {self.mines}")

        if len(safe_moves) == 0:
            return None

        return random.sample(safe_moves, 1)[0]
    
        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        i = random.randrange(self.height)
        j = random.randrange(self.height)

        while ((i, j) in self.mines) or ((i, j) in self.moves_made):
            i = random.randrange(self.height)
            j = random.randrange(self.height)

        return i, j
