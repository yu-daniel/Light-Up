import pygame
import random

class Board:
    def __init__(self):
        """
        Initializes the puzzle board.
        """
        self.board = [[''] * 9 for i in range(9)]
        self.squares = {}
        self.black = []
        self.certificate = {}
        self.message, self.message2, self.message3 = '', '', ''

    def get_board(self):
        """Returns the puzzle board."""
        return self.board

    def get_square(self, coordinates):
        """
        Returns the square at the specified location.
        """
        return self.squares[coordinates]

    def get_certificate(self):
        """Returns the certificate."""
        return self.certificate

    def get_message(self):
        """Returns all the messages (1, 2, and 3)."""
        return self.message, self.message2, self.message3

    def set_board(self, x, y, square):
        """
        Places the square at the specified location on the board.
        """
        self.board[x][y] = square
        self.squares[(x, y)] = square

    def set_message(self, message, message2, message3):
        """Sets warning messages for the player."""
        self.message = message
        self.message2 = message2
        self.message3 = message3

    def generate_white_squares(self):
        """
        Generate white squares throughout the board.
        """
        for i in range(9):
            for j in range(9):
                if i == 0 or i == 8 or j == 0 or j == 8:
                    self.set_board(i, j, '-')
                else:
                    if self.board[i][j] == '':
                        square = White(i, j)
                        self.board[i][j] = square
                        self.squares[(i, j)] = square

    def generate_black_squares(self):
        """
        Randomly generate between 8-12 black squares throughout the board.
        """
        coordinates = []

        sq_num = random.randrange(8, 12)
        while len(coordinates) != sq_num:
            x, y = random.randrange(1, 8), random.randrange(1, 8)
            if (x, y) not in coordinates:
                coordinates.append((x, y))
                sq = Black(x, y)
                self.set_board(x, y, sq)
                self.black.append(sq)

    def generate_edges(self):
        """
        Add neighbors (i.e. adjacent squares) for each square.
        """

        # traverse the Board, for each row and column,
        for i in range(1, 8):
            for j in range(1, 8):

                # specify the adjacent directions
                top = self.board[i - 1][j]
                left = self.board[i][j - 1]
                right = self.board[i][j + 1]
                bottom = self.board[i + 1][j]

                # add each neighbor found in the adjacent directions to a list
                neighbors = [top, left, right, bottom]

                # visit each neighbor and add edges between current square and the neighbor
                for p in neighbors:
                    if p != '-':
                        curr = self.board[i][j]
                        curr.add_neighbors(p)

    def assign_number(self):
        """
        Assign a number between 0-4 for each black square.
        """

        for j in range(len(self.black)):
            sq = self.black[j]
            location = sq.get_location()
            x, y = location[0], location[1]
            needed_bulbs = 0

            # point to the current square's adjacent side
            top = self.get_board()[x - 1][y]
            left = self.get_board()[x][y - 1]
            right = self.get_board()[x][y + 1]
            bottom = self.get_board()[x + 1][y]
            neighbors = [top, left, right, bottom]

            # for each side (i.e. neighbor),
            for p in neighbors:
                if p != '-':
                    # increment light bulb count, if neighbor has a light bulb
                    if p.get_tag() == '@':
                        needed_bulbs += 1

            # update the Black square's current # of adjacent light bulbs
            if needed_bulbs > 0:
                sq.set_number(str(needed_bulbs))
                sq.set_tag(str(needed_bulbs))

            # give 10% chance to assign 0
            else:
                if random.random() >= 0.9:
                    sq.set_number(str(0))
                    sq.set_tag(str(0))

    def remove_lightbulbs(self):
        """
        Remove all light bulbs on the board.
        """
        for i in self.board:
            for j in i:
                if j != '-':
                    if type(j) == White and j.get_illuminated() is True:
                        j.set_illuminated(False)
                        j.set_visited(False)

    def create_instance(self):
        """
        Traverse the board and randomly place light bulbs to squares
        that are not yet illuminated.
        """

        no_space = False
        while no_space is False:

            not_lit = []
            # for squares in each row and column,
            for i in self.get_board():
                for j in i:
                    if j != '-':
                        # set visited to false and add to not_lit list if it is a White square
                        j.set_visited(False)
                        if j.get_tag() == 'W':
                            not_lit.append(j)

            # return the boolean results, whether all squares are illuminated
            if len(not_lit) == 0:
                no_space = True

            elif len(not_lit) == 1:
                self.generate_lightbulbs(not_lit[0], 0, 'admin')
                no_space = True

            if no_space is False:
                source = self.board[1][1]
                self.BFS('fill_board', source)
                not_lit = []

    def verifier(self, certificate):
        """
        Verifies the player's solution - whether it meets all winning criteria.

        """
        single_bulbs = True

        for i in certificate:
            self.generate_lightbulbs(certificate[i], 0, None)

            single_bulbs = self.generate_light(certificate[i], False, True)
            # if single_bulb is False, then this light bulb is lighting another light bulb
            # then mark this square by setting its overlap attribute as True
            if single_bulbs is False:
                certificate[i].set_overlap(True)

        # check if all white square are illuminated
        all_illu = self.BFS('check_lights', self.board[1][1])

        # check if all Black squares have required # of adjacent light bulbs
        black_sq_ok = self.BFS('check_numbers', self.black[0])

        # give warning message to player if a winning condition is not met
        if all_illu is True and single_bulbs is True and black_sq_ok is True:
            return True
        else:
            if all_illu is False:
                self.message = 'Not all squares are illuminated!'
            if black_sq_ok is False:
                self.message2 = 'Some Black square(s) have wrong # of surrounding light bulbs!'
            if single_bulbs is False:
                self.message3 = 'A light bulb is illuminating another light bulb!'
            return False

    def BFS(self, coordinates, source):
        """
        Breadth-first search traversal to visit each square on the board.

        """
        # for each square, set visited as False to traverse properly
        for i in self.board:
            for j in i:
                if type(j) == White or type(j) == Black:
                    j.set_visited(False)

        # initialize a queue with source square (i.e. vertex)
        # 'group' is the neighboring squares of the current square
        queue = [source]
        group = None

        # continue traversing the board while queue has squares not visited
        while queue:
            # remove first item of queue
            s = queue.pop(0)

            # decide which group of squares to traverse
            if coordinates == 'check_lights':
                group = s.get_neighbors()
            elif coordinates == 'fill_board':
                group = s.get_neighbors()
            elif coordinates == 'check_numbers':
                group = self.black

            # for each square in the group, visit if not visited yet
            for i in group:
                if i.get_visited() is False:
                    i.set_visited(True)

                    # if traversing to randomly assigning light bulbs, and create a 
                    # valid instance, then add light bulb at 40% chance
                    if coordinates == 'fill_board':
                        if type(i) == White and i.get_illuminated(
                        ) is False and i.get_light_bulb() is False:
                            chance = 0.40
                            self.generate_lightbulbs(i, chance, 'admin')

                    # if traversing to check if all (White) squares are
                    # illuminated, return False if one is unlit
                    elif coordinates == 'check_lights' and type(i) == White:
                        if i.get_illuminated() is False:
                            return False

                    # if traversing to count light bulbs around the
                    # black squares, return False if count doesn't match
                    # the number attribute
                    elif coordinates == 'check_numbers' and type(i) == Black:
                        if i.get_number() != 'B':
                            total = 0
                            for x in i.get_neighbors():
                                if type(x) == White and x.get_light_bulb(
                                ) is True:
                                    total += 1
                            if str(total) != i.get_number():
                                return False
                    queue.append(i)

            s.set_visited(True)

        if coordinates == 'check_lights' or coordinates == 'check_numbers':
            return True

    def generate_lightbulbs(self, sq, chance, user):
        """
        Generate a light bulb with a given percent chance.
        """
        if random.random() >= chance and type(sq) == White and sq.get_light_bulb() is False:

            if user == 'admin':
                self.certificate[sq.get_location()] = sq
            status = sq.toggle_light_bulb()

            if status is True:
                self.generate_light(sq, True, False)

    def generate_light(self, square, toggle, verification):
        """
        Takes two parameters,
        curr - the square object that will be the source of the light emission
        toggle - True/False, whether to turn on the light or turn off the light
        """

        # get the current square's location (row, column)
        loc = square.get_location()
        # 'counter' is used to increment each index
        counter = 1

        # point to the square's adjacent sides
        directions = [
            [loc[0], loc[1] + counter],  # right
            [loc[0], loc[1] - counter],  # left
            [loc[0] + counter, loc[1]],  # top
            [loc[0] - counter, loc[1]]   # bottom
        ]

        # for each direction,
        for x in range(4):
            # nex is the following square to visit, starting from the (current) square
            nex = self.get_square((directions[x][0], directions[x][1]))

            while type(nex) == White:
                # if traversing to illuminate or de-illuminate squares, stop when next square is a light bulb
                if verification is False and nex.get_tag() == '@':
                    break

                # traversing to check if the current square (a light bulb) is illuminating some other light bulb(s)
                if verification is True:
                    if nex.get_light_bulb() is True:
                        return False

                # traversing to illuminate/de-illuminate squares, then call set_illuminate for either case
                if verification is False:
                    nex.set_illuminated(toggle)
                counter += 1

                if x == 0:
                    nex = self.get_square((loc[0], loc[1] + counter))
                elif x == 1:
                    nex = self.get_square((loc[0], loc[1] - counter))
                elif x == 2:
                    nex = self.get_square((loc[0] + counter, loc[1]))
                elif x == 3:
                    nex = self.get_square((loc[0] - counter, loc[1]))

            counter = 1

        if verification:
            return True

class Squares:
    # Represents a square that is on the puzzle Board.
    def __init__(self, x, y):
        """
        Initializes the square's attributes.
        """
        self.neighbors = []
        self.tag = ''
        self.visited = False
        self.location = (x, y)

    def get_neighbors(self):
        """Returns the Square's list of adjacent neighbors."""
        return self.neighbors

    def get_tag(self):
        """Returns the Square's tag attribute ('W', 'B', or '@')."""
        return self.tag

    def get_visited(self):
        """Returns the Square's visited attribute (True or False)."""
        return self.visited

    def get_location(self):
        """Returns the Square's coordinate position on the board as a tuple (row, column)."""
        return self.location

    def set_tag(self, tag):
        """Sets the Square's tag attribute ('W', 'B', or '@')."""
        self.tag = tag

    def set_visited(self, status):
        """Sets the Square's visited attribute to the parameter (either as True or as False)."""
        self.visited = status

    def add_neighbors(self, square):
        """Adds 'square' as the current Square's neighbor"""
        self.neighbors.append(square)


class Black(Squares):
    # Represents a Black square on the Board.
    def __init__(self, x, y):
        """
        Initializes a black square's characteristics.
        """
        super().__init__(x, y)
        self.edges = []
        self.number = 'B'
        self.tag = 'B'

    def __str__(self):
        """Returns the square's number attribute rather than the object for the print method."""
        return '{self.number}'.format(self=self)

    def get_number(self):
        """Returns the square's number attribute (i.e. B, 0, 1 , 2, 3, or 4)."""
        return self.number

    def set_number(self, num):
        """Sets the square's number attribute (i.e. B, 0, 1, 2, 3 or 4)."""
        self.number = num

class White(Squares):
    # Represents a White square on the Board.
    def __init__(self, x, y):
        """
        Initializes a white square's characteristics.
        """
        super().__init__(x, y)
        self.illuminated = False
        self.light_bulb = False
        self.tag = 'W'
        self.overlap = False

    def __str__(self):
        """Returns the square's tag rather than the object when it is printed."""
        return '{self.tag}'.format(self=self)

    def get_illuminated(self):
        """Returns the square's illuminated attribute (either True or as False)."""
        return self.illuminated

    def get_light_bulb(self):
        """Returns a boolean, whether the square has a light bulb."""
        return self.light_bulb

    def get_overlap(self):
        """Returns a boolean, whether it illuminates another light bulb."""
        return self.overlap

    def set_illuminated(self, toggle):
        """
        Takes a boolean as a parameter, if True, then set illuminated as True
        and the tag to '*', the display to show it is illuminated
        otherwise, illuminated is set to False and the tag is converted to 'W'.
        """
        # turn the square's light on
        if toggle is True:
            self.illuminated = True
            self.tag = '*'

        # turn the square's light off
        elif toggle is False:
            self.illuminated = False
            self.tag = 'W'
            self.light_bulb = False

    def set_overlap(self, overlap):
        """Set self.over to overlap."""
        self.overlap = overlap

    def toggle_light_bulb(self):
        """
        Returns whether the square is a light bulbs.

        Adds a light bulb to the square and illuminated it if it is currently not
        Otherwise, remove the square's light bulb.
        """
        if self.light_bulb is False:
            self.light_bulb = True
            self.illuminated = True
            self.tag = '@'
        else:
            self.light_bulb = False
        return self.light_bulb

class Pygame:

    def __init__(self):
        """
        Initiate RGB code for color referencing and constants for window settings.
        
        lb.png and lb2.png images are from:
        http://clipart-library.com/clipart/pT5dGE7T9.htm
        http://clipart-library.com/clipart/rcLgLx57i.htm
        """
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 102, 102)
        self.gray = (105, 105, 105)
        self.yellow = (255, 255, 204)
        self.width = 40                                              # the width in pixels for each square
        self.height = 40                                             # the height in pixels for each square
        self.divider_width = 2                                       # size for the borders dividing the Board
        self.windows = [380, 450]                                    # default screen size (width x height)
        self.screen = pygame.display.set_mode(self.windows)          # initiate display when object is created
        self.image = pygame.image.load('lb.png').convert()    # normal light bulb image
        self.image2 = pygame.image.load('lb2.png').convert()  # red light bulb image

    def setup(self):
        """
        Take no parameters; initiate all necessary methods to create
        a playable and solvable instance of Light Up.
        """
        board = Board()                     
        board.generate_white_squares()      
        board.generate_black_squares()      
        board.generate_edges()             
        board.create_instance()             
        board.assign_number()               
        board.remove_lightbulbs()           
        verification = board.verifier(board.get_certificate()) 
        board.remove_lightbulbs()           

        # initiate Pygame and title
        pygame.init()
        pygame.display.set_caption("Light Up")

        # 'save_user_answers' toggles between showing/hiding in-game solution and the player's answers
        # 'solution_mode' indicates whether the Player is currently viewing the in-game solution
        save_user_answers = True
        solution_mode = False
        victory = False

        # store the Player's answers in form of a dictionary
        user_answers = dict()

        # Keep the game's loop running until the Player manually exists or if he/she submits a verified solution
        while True:
            for event in pygame.event.get():

                # get the Player's mouse coordinates when the screen is clicked
                coordinates = pygame.mouse.get_pos()

                submit = 200 <= coordinates[0] <= 200 + 110 and 370 <= coordinates[1] <= 370 + 40
                solution = 55 <= coordinates[0] <= 166 + 115 and 376 <= coordinates[1] <= 370 + 40

                ESC = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                if event.type == pygame.QUIT or ESC:
                    pygame.quit()
                    exit()

                # listen for Player's clicks on the Board
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    column = coordinates[0] // (self.width + self.divider_width)
                    row = coordinates[1] // (self.height + self.divider_width)

                    # reset system messages after Player does an action
                    board.set_message('', '', '')

                    # listen for Player's click on the 'Submit' button for submitting his/her solution
                    # also limit the click area for this function to take effect
                    # 'solution_mode' prevent Player from submitting the in-game solution as their own answer
                    if submit and solution_mode is False:
                        results = board.verifier(user_answers)
                        if results is True:
                            board.set_message('Congratulations! You win!', '', '')
                            victory = True

                    # listen for Player's click on the 'Solution' button for showing the in-game solution
                    elif solution:
                        if save_user_answers is True:
                            board.remove_lightbulbs()
                            board.verifier(board.get_certificate())
                            save_user_answers = False
                            solution_mode = True

                        # if the button is clicked a second time, remove the in-game solution on the Board
                        # and let the Player continue to play the same instance
                        elif save_user_answers is False:
                            board.remove_lightbulbs()
                            solution_mode = False
                            for i in user_answers:
                                square = user_answers[i]
                                board.generate_lightbulbs(square, 0, None)
                            save_user_answers = True

                    elif 44 <= coordinates[0] <= 336 and 44 <= coordinates[1] <= 336:
                        square = board.get_square((row, column))

                        if type(square) == White and solution_mode is False:
                            # if the White square isn't a light bulb and isn't illuminated, then add
                            # a light bulb to this square, and add it to the Player's list of answers
                            if (row, column) not in user_answers:
                                square = board.get_square((row, column))
                                board.generate_lightbulbs(square, 0, None)
                                if square.get_light_bulb() is True:
                                    user_answers[(row, column)] = square

                            # if click is already part of the Player's answers, this indicates he/she
                            # is asking to remove the light bulb, then proceed to remove it from the Board
                            # and from Player's answer list
                            elif (row, column) in user_answers:
                                if square.get_light_bulb() is True:
                                    board.generate_light(square, False, False)
                                    square.set_illuminated(False)
                                    del user_answers[(row, column)]

                                    # While light bulb is removed, also de-illuminate all the squares that were lit up by this
                                    for i in board.get_board():
                                        for j in i:
                                            if type(j) == White and j.get_light_bulb() is True:
                                                board.generate_light(j, True, False)

                    # set the image for light bulbs depending if the Player keeps the mistake
                    # or if he/she has corrected the mistake, then change the image back to non-red.
                    for i in board.get_board():
                        for j in i:
                            if type(j) == White and j.get_light_bulb() is True:
                                overlap = board.generate_light(j, False, True)
                                if overlap is False:
                                    j.set_overlap(True)
                                else:
                                    j.set_overlap(False)

            # Based on the Player's request to update light bulbs above, use the latest Board
            # and update each square's color
            for row in range(1, 8):
                for column in range(1, 8):
                    color = self.black
                    square = board.get_square((row, column))
                    if square.get_tag() == 'W':
                        color = self.white
                    elif square.get_tag() == '@' or square.get_tag() == '*':
                        color = self.yellow

                    # draw the board
                    pygame.draw.rect(self.screen, color, [(self.divider_width + self.width) * column + self.divider_width,
                                (self.divider_width + self.height) * row + self.divider_width, self.width, self.height])

                    # update the square's tag in addition to the square's color that was performed already
                    self.update_square_tags(square, row, column)
                    # add borders to highlight the Board
                    self.draw_borders()

            # draw the 'Solution' and 'Submit' button to the display
            self.add_buttons()
            # draw in-game messages to the Player to the display
            self.update_message(board)
            # check if Player has won the game, if so, give congratulatory message and exit game
            if victory is True:
                self.check_victory(victory, board)
            pygame.display.flip()

    def add_buttons(self):
        """
        Creates the text and rects for the 'Submit' and 'Solution' button, and their location on the display.
        """
        # initiate the font and font size for the button
        font = pygame.font.SysFont('Calibri', 35)
        # draw a rect as background for this button
        pygame.draw.rect(self.screen, self.gray, [200, 370, 100, 40])
        # add the text to the display
        text = font.render('Submit', True, self.black)
        self.screen.blit(text, (200, 370))

        # same procedure below for the 'Solution' button as the 'Submit' button
        pygame.draw.rect(self.screen, self.gray, [50, 370, 115, 40])
        text = font.render('Solution', True, self.black)
        self.screen.blit(text, (50, 370))

    def draw_borders(self):
        """
        Draw the borders that highlight the Board.
        """
        # draw.line(surface, color, (starting column, starting row), (ending column, ending row), thickness)
        pygame.draw.line(self.screen, self.gray, (42, 42), (336, 42), 2)        # top horizontal
        pygame.draw.line(self.screen, self.gray, (42, 336), (336, 336), 2)      # bottom horizontal
        pygame.draw.line(self.screen, self.gray, (42, 42), (42, 336), 2)        # left vertical
        pygame.draw.line(self.screen, self.gray, (336, 42), (336, 337), 2)      # right vertical

    def check_victory(self, victory, board):
        """
        Presents a countdown for the game to exit when the Player's
        solution is verified correct by the verification algorithm.
        """
        if victory is True:
            # Show the congratulatory message for 2 second
            pygame.time.wait(1000)
            pygame.display.flip()

            pygame.time.wait(1000)
            pygame.draw.rect(self.screen, self.black, [1, 1, 375, 35])

            # Change the message that the game ends in 5 seconds for the Player
            board.set_message('Game ends in 5 seconds...', '', '')
            warning_font = pygame.font.SysFont('Calibri', 15)
            warning = warning_font.render(board.get_message()[0], False, self.yellow)
            self.screen.blit(warning, (5, 5))
            pygame.display.flip()

            # Initiate a countdown from 5 to 0
            for i in range(5, -1, -1):
                pygame.time.wait(1000)
                board.set_message(str(i) + '...', '', '')

                warning_font = pygame.font.SysFont('Calibri', 15)
                warning = warning_font.render(board.get_message()[0], False, self.yellow)
                self.screen.blit(warning, (185, 5))
                pygame.display.flip()

                # After displaying each second of the countdown, then erase it for the next number
                pygame.draw.rect(self.screen, self.black, [170, 1, 375, 35])
            pygame.quit()
            exit()

    def update_message(self, board):
        """
        Update the in-game messages that will be displayed to the Player.
        """
        if board.get_message()[0] != '' or board.get_message()[1] != '' or board.get_message()[2] != '':
            # Set the font and position of the first warning message,
            # notifying the Player, the Black squares have wrong # of adjacent light bulbs
            warning_font = pygame.font.SysFont('Calibri', 15)
            warning = warning_font.render(board.get_message()[0], False, self.green)
            self.screen.blit(warning, (5, 5))

            # Update the second warning message, the Player has not yet illuminated all light bulbs
            warning = warning_font.render(board.get_message()[1], False, self.green)
            self.screen.blit(warning, (5, 20))

            warning = warning_font.render(board.get_message()[2], False, self.green)
            self.screen.blit(warning, (60, 345))


        if board.get_message()[0] == '' and board.get_message()[1] == '' and board.get_message()[2] == '':
            pygame.draw.rect(self.screen, self.black, [5, 1, 375, 35])
            pygame.draw.rect(self.screen, self.black, [50, 345, 320, 20])

    def update_square_tags(self, square, row, column):
        """
        Update the display with each square's latest tag attributes.
        """
        # set the font for the tag
        font = pygame.font.SysFont('Arial', 30)
        # for Black squares, draw their assigned number to the display
        if type(square) == Black:
            font = pygame.font.SysFont('Arial', 30)
            text = font.render(square.get_tag(), 1, (100, 255, 55))
            rect = column * (self.divider_width + self.width) + 15, row * (self.divider_width + self.height)
            self.screen.blit(text, rect)

        # for White squares, draw the light bulb image (.png) to the display
        if type(square) == White and square.get_light_bulb() is True:
            text = font.render(square.get_tag(), 1, self.red)
            rect = column * (self.divider_width + self.width) + 12, row * (self.divider_width + self.height) + 3

            if square.get_overlap():
                self.screen.blit(self.image2, rect)
            else:
                self.screen.blit(self.image, rect)

# initiate the Pygame object and also the setup() to get the game running.
game = Pygame()
game.setup()
