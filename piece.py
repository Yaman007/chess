class Piece:
    def __init__(self, color, name, img, loc=(-1, -1), can_capture=False, move_count=0):
        self.color = color
        self.name = name
        self.img = img
        self.loc = loc
        self.can_capture = can_capture
        self.move_count = 0
