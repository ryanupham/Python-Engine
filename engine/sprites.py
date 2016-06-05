class Sprite:
    def __init__(self, image, width=-1, height=-1, rotation=0):
        self.image, self.width, self.height, self.angle = image, width, height, rotation

        if width == -1 and image is not None:
            self.width = image.width
        if height == -1 and image is not None:
            self.height = image.height
