"""
Univeristy project 

Description: A game played between 2 people to see who can get the most points in a square gameboard. Players x and o choose the column they would like their counter to occupy
and the counter falls to the lowest row available. Players gain points from getting 4 counters in a row, whether vertically, diagonally or horizontally.
"""

class GameBoard:
    def __init__(self, size):
        self.size=size
        self.num_entries = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] * 2
        self.finish_check = False #Check to see if player wants to finish game early

    def num_free_positions_in_column(self, column):
        count = 0
        for num in self.items[column]:
            if num == 0:
                count += 1
        return count
    
    def game_over(self):
        if self.finish_check == True:
            return True
        count = 0
        for num in range(self.size):
            if self.num_free_positions_in_column(num) == 0:
                count += 1
        if count == self.size:
            return True
        return False
    
    def finish_early(self):
        #Changes finish check to true so when gameover is called, it will return True
        self.finish_check = True
        return True

    def display(self):
        for num in range(self.size - 1, -1, -1):
            for col in self.items:
                if col[num] == 0:
                    print(" ", end = " ")
                elif col[num] == 1:
                    print("o", end = " ")
                else:
                    print("x", end = " ")
            print()

        print("-" * (self.size * 2 - 1))
        for num in range(self.size):
            print(num, end = " ")
        print()
        print(f"Points player 1: {self.points[0]}")
        print(f"Points player 2: {self.points[1]}")
    
    def num_new_points(self, column, row, player):
        points = 0

        points += self.horizontal(column, row, player)
        points += self.vertical(column, row, player)
        points += self.diagonal(column, row, player)
        points += self.inverse_diagonal(column, row, player)
        return points


    def horizontal(self, column, row, player):
        points = 0
        if column >= 0:
            count = 0
            for i in range(1,4):
                if column-i <= self.size - 1 and row <= self.size - 1 and column - i >= 0:
                    if (self.items[column-i][row]) == player:
                        count += 1
                if column+i <= self.size - 1 and row <= self.size - 1 and column + i >= 0:
                    if (self.items[column+i][row]) == player:
                        count += 1
            if count >= 3:
                points += count // 3 + (count % 3)
        return points
    
    def vertical(self, column, row, player):
        points = 0
        if column >= 0:
            count = 0
            for i in range(1,4):
                if column <= self.size - 1 and row - i <= self.size - 1 and column >= 0:
                    if (self.items[column][row-i]) == player:
                        count += 1
            if count >= 3:
                points += count // 3 + (count % 3)

        return points
    
    def diagonal(self, column, row, player):
        points = 0
        if column >= 0:
            count = 0
            for i in range(1,4):
                if column - i <= self.size - 1 and row - i <= self.size - 1 and column - i >= 0:
                    if (self.items[column-i][row-i]) == player:
                        count += 1
                if column + i <= self.size - 1 and row + i <= self.size - 1 and column + i >= 0:
                    if (self.items[column+i][row+i]) == player:
                        count += 1
            if count >= 3:
                points += count // 3 + (count % 3)
        return points
    
    def inverse_diagonal(self, column, row, player):
        points = 0
        if column >= 0:
            count = 0
            for i in range(1,4):
                if column - i <= self.size - 1 and row + i <= self.size - 1 and column - i >= 0:
                    if (self.items[column-i][row+i]) == player:
                        count += 1
                if column + i <= self.size - 1 and row - i <= self.size - 1 and column + i >= 0:
                    if (self.items[column+i][row-i]) == player:
                        count += 1
            if count >= 3:
                points += count // 3 + (count % 3)

        return points

    def add(self, column, player):
        if self.num_entries[column] >= self.size or column < 0 or column >= self.size:
            return False

        self.items[column][self.num_entries[column]] = player
        self.num_entries[column] += 1

        self.points[player-1] += self.num_new_points(column, self.num_entries[column]-1, player)
        return True

    def free_slots_as_close_to_middle_as_possible(self):
        complete = []
        for n in range(self.size):
            complete.append(n)

        new_list = []
         
        for n in range(len(complete)-1,-1,-1):
            middle = (len(complete)-1)//2
            new_list.append(complete.pop(middle))

        final = []
        for val in new_list:
            if self.num_free_positions_in_column(val) != 0:
                final.append(val)

        return final

    def column_resulting_in_max_points(self, player):
        points = []
        for column in range(self.size):
            if self.num_free_positions_in_column(column) == 0:
                points.append(0)
            else:
                points.append(self.num_new_points(column, self.num_entries[column], player))

        max_point = max(points)

        if max_point == 0:
            return self.free_slots_as_close_to_middle_as_possible()[0], 0

        checked = []
        dup = []
        for val in points:
            if val not in checked:
                checked.append(val)
            else:
                dup.append(val)
        
        if max_point in dup:
            return self.free_slots_as_close_to_middle_as_possible()[0], 0
            
        
        position = points.index(max_point)
        return position, max_point
    
    def reset(self): 
        #Sets the board and points back to the start
        self.num_entries = [0] * self.size
        self.items = [[0] * self.size for i in range(self.size)]
        self.points = [0] * 2


class FourInARow:
    def __init__(self, size):
        self.board=GameBoard(size)
    def play(self):
        print("*****************NEW GAME*****************")
        self.board.display()
        player_number=0
        print()
        while not self.board.game_over():
            print("Input -1 to reset board or -2 to finish game early.")
            print("Player ",player_number+1,": ")
            if player_number==0:
                valid_input = False
                while not valid_input:
                    try:
                        column = int(input("Please input slot: "))
                    except ValueError:
                        print("Input must be an integer in the range 0 to ", self.board.size)
                    else:
                        if column == -1:
                            reset_confirm = input("Would you like to reset? Y/N: ") #Confirms user's choice to reset board
                            if reset_confirm.lower() == "y":
                                self.board.reset() #Resets the board
                                print("Player ",player_number+1,": ") 
                            else:
                                print("Input must be an integer in the range 0 to ", self.board.size) #Error message, continues playing
                        if column<-2 or column>=self.board.size:
                            print("Input must be an integer in the range 0 to ", self.board.size)
                        if column == -2:
                            finish_confirm = input("Would you like to reset? Y/N: ") #Confirms user's choice to finish early
                            if finish_confirm.lower() == "y":
                                valid_input = True
                                self.board.finish_early()
                        else:
                            if self.board.add(column, player_number+1):
                                valid_input = True
                            if self.board.num_free_positions_in_column(column) == 0:
                                print("Column ", column, "is alrady full. Please choose another one.")
            else:
                # Choose move which maximises new points for computer player
                (best_column, max_points)=self.board.column_resulting_in_max_points(2)
                if max_points>0:
                    column=best_column
                else:
                    # if no move adds new points choose move which minimises points opponent player gets
                    (best_column, max_points)=self.board.column_resulting_in_max_points(1)
                    if max_points>0:
                        column=best_column
                    else:
                        # if no opponent move creates new points then choose column as close to middle as possible
                        column = self.board.free_slots_as_close_to_middle_as_possible()[0]
                self.board.add(column, player_number+1)
                print("The AI chooses column ", column)
            self.board.display()   
            player_number=(player_number+1)%2
        if (self.board.points[0]>self.board.points[1]):
            print("Player 1 (circles) wins!")
        elif (self.board.points[0]<self.board.points[1]):    
            print("Player 2 (crosses) wins!")
        else:  
            print("It's a draw!")
            
game = FourInARow(6)
game.play()   
