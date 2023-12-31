'''Modules for calculations and computer visualization'''
import numpy as np
import cv2


TILE_SIZE = 32

MARKET = """
##################
##..............##
##..y#..d#..f#..##
##..y#..d#..f#..##
##..y#..d#..f#..##
##..s#..d#..f#..##
##..s#..d#..f#..##
##...............#
##..C#..C#..C#...G
##..##..##..##...G
##...............#
######xx##########
""".strip()

class Customer:
    
    def __init__(self, supermarket, avatar, row, col):
        """ 
        supermarket: A SuperMarketMap object
        avatar : a numpy array containing a 32x32 tile image
        row: the starting row
        col: the starting column
        """

        self.supermarket = supermarket
        self.avatar = avatar
        self.row = row
        self.col = col

    
    def __repr__(self):
        return f'<Customer is at {self.state}>'

    def draw(self, frame):
        x = self.col * TILE_SIZE
        y = self.row * TILE_SIZE
        frame[y:y+TILE_SIZE, x:x+TILE_SIZE] = self.avatar

    def move(self, direction):
        new_row = self.row
        new_col = self.col

        if direction == 'up':
            new_row -= 1
        elif direction == 'down':
            new_row += 1
        elif direction == 'left':
            new_col -= 1
        elif direction == 'right':
            new_col += 1

        if self.supermarket.contents[new_row][new_col] == '.':
            self.col = new_col
            self.row = new_row    


class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tiles   : a numpy array containing all the tile images
        """
        self.tiles = tiles
        # split the layout string into a two dimensional matrix
        self.contents = [list(row) for row in layout.split("\n")]
        self.ncols = len(self.contents[0])
        self.nrows = len(self.contents)
        self.image = np.zeros(
            (self.nrows*TILE_SIZE, self.ncols*TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()

    def extract_tile(self, row, col):
        """extract a tile array from the tiles image"""
        y = row*TILE_SIZE
        x = col*TILE_SIZE
        return self.tiles[y:y+TILE_SIZE, x:x+TILE_SIZE]

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.extract_tile(0, 0)
        elif char == "G":
            return self.extract_tile(1, 1)
        elif char == "C":  #checkout
            return self.extract_tile(7, 3)
        elif char == "x":  #exit
            return self.extract_tile(0, 2)
        elif char == "e": #entry
            return self.extract_tile(1, 1)
        elif char == "f": #fruit
            return self.extract_tile(1, 4)
        elif char == "s": #spices
            return self.extract_tile(5, 7)
        elif char == "y": #dairy
            return self.extract_tile(7, 11)
        elif char == "d":  #drink
            return self.extract_tile(3, 13)
        else:
            return self.extract_tile(1, 2)

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):
            for col, char in enumerate(line):
                bm = self.get_tile(char)
                y = row*TILE_SIZE
                x = col*TILE_SIZE
                self.image[y:y+TILE_SIZE, x:x+TILE_SIZE] = bm

    def draw(self, frame):
        """
        draws the image into a frame
        """
        frame[0:self.image.shape[0], 0:self.image.shape[1]] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)


if __name__ == "__main__":

    background = np.zeros((500, 700, 3), np.uint8)
    tiles = cv2.imread("tiles.png")
    print("test before")
    market = SupermarketMap(MARKET, tiles)
    print("test after")
    supermarket = cv2.imread("supermarket.png")
    avatar = market.extract_tile(row=8, col=1)
    customer = Customer(supermarket = supermarket, avatar = avatar, row = 11, col=15)   
    

    while True:
        frame = background.copy()
        market.draw(frame)
        customer.draw(frame)

        # https://www.ascii-code.com/
        key = cv2.waitKey(1)
       
        if key == 113: # 'q' key
            break

        cv2.imshow("frame", frame)


    cv2.destroyAllWindows()

    market.write_image("supermarket.png")
