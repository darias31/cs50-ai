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

        # mark the cell as a move that has been made
        self.moves_made.add(cell)

        # mark the cell as safe
        self.mark_safe(cell)

        # add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        neighbor_cells = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor_cells.add((i,j))

        #print(f"Neighbor sets: {neighbor_cells}")

        self.knowledge.append(Sentence(neighbor_cells,count))
        
        #mark any additional cells as safe or as mines
        knowledge_length = len(self.knowledge)
        for index1 in range(knowledge_length):

            sentence1 = self.knowledge[index1]

            # check for 100% safes or 100% mines
            if sentence1.known_safes() != None:
                self.safes = self.safes.union(sentence1.cells)    
            elif sentence1.known_mines() != None:
                self.mines = self.mines.union(sentence1.cells)
            else:
                for index2 in range(knowledge_length):

                    sentence2 = self.knowledge[index2]

                    if (sentence2.known_safes() != None) and (sentence2.known_mines() != None):
                        continue
                    elif (not sentence1.cells.isdisjoint(sentence2.cells)) and (sentence1.cells != sentence2.cells):

                        count = sentence2.count - sentence1.count

                        if (count >= 0) and (len(sentence1.cells) > 0 and len(sentence2.cells) > 0):

                            for i in self.knowledge:
                                if (sentence2.cells - sentence1.cells) in i.cells:
                                    print("already in knowledge")
                                    break

                            self.knowledge.append(Sentence(sentence2.cells - sentence1.cells,count))
                            print(f"Added to knowledge: {self.knowledge[-1]}")

                            # do not add empty cells
                            # do not add duplicates

            print(f"known safes: {self.safes}")
            print(f"length of knowledge: {len(self.knowledge)}")
