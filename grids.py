from PIL import Image
import numpy as np


class Grid:
    def __init__(self, filepath, start, end):
        occ_img = Image.open(filepath).convert('L')
        occ = np.array(occ_img)/255
        self.bg = occ_img
        self.occupancy_grid = occ
        self.start = start
        self.end = end

class Grids:
    def __init__(self):
        self.grid1 = Grid('grids/occupancy0.png', (1,1), (96,96))
        self.grid2 = Grid('grids/occupancy1.png', (1,1), (5,95))
        self.grid3 = Grid('grids/occupancy2.png', (1,1), (10,85))
        self.grid4 = Grid('grids/occupancy3.png', (1,1), (95,96))
        self.grid5 = Grid('grids/occupancy4.png', (1,1), (95,96))
        self.grid6 = Grid('grids/occupancy5.png', (1,1), (95,96))
