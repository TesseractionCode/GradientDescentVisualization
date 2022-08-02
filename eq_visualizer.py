from pydoc import visiblename
from PIL import Image
import pygame.image
import os


class ViewFrame:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class EqVisualizer:

    img_dir = "eq_visuals"

    def __init__(self, viewFrame: ViewFrame, plottingFunction,
                 minViewHeight=-10, maxViewHeight=10,
                 viewPosX=0, viewPosY=0, unitPerPixel=1):
        self.viewFrame = viewFrame
        self.plottingFunction = plottingFunction
        self.minViewHeight = minViewHeight
        self.maxViewHeight = maxViewHeight
        self.viewPosX = viewPosX
        self.viewPosY = viewPosY
        self.unitPerPixel = unitPerPixel
        self.__visual = None

    @staticmethod
    def __clamp(value, minVal, maxVal):
        '''Clamp a number between a min and a max.'''
        return min(max(value, minVal), maxVal)

    @staticmethod
    def __ensureImageDirectory():
        '''Make sure the folder that stores images exists.'''
        if not os.path.exists(EqVisualizer.img_dir):
            os.makedirs(EqVisualizer.img_dir)

    @staticmethod
    def __getNextVisualName():
        '''Get the file name of the next visualization.'''
        dir_path = EqVisualizer.img_dir
        numVisuals = len([entry for entry in os.listdir(
            dir_path) if os.path.isfile(os.path.join(dir_path, entry))])
        return "visual_" + str(numVisuals) + ".png"

    def screenPosToVal(self, screen_x, screen_y):
        x, y = self.screenPosToCartesianPos(screen_x, screen_y)
        return self.plottingFunction(x, y)

    def screenPosToCartesianPos(self, screen_x, screen_y):
        x = (screen_x - self.viewFrame.x -
             self.viewFrame.width/2) * self.unitPerPixel
        y = (screen_y - self.viewFrame.y -
             self.viewFrame.height/2) * self.unitPerPixel
        return x, y

    def cartesianPosToScreenPos(self, x, y):
        screen_x = self.viewFrame.x + self.viewFrame.width/2 + x / self.unitPerPixel
        screen_y = self.viewFrame.y + self.viewFrame.height/2 + y / self.unitPerPixel
        return screen_x, screen_y

    def genImage(self, useNewImage=True):
        '''Generate an image from the function and save it as a file.'''
        self.__ensureImageDirectory()

        image_dir = os.path.join(EqVisualizer.img_dir,
                                 self.__getNextVisualName())
        image = Image.new("RGB", (self.viewFrame.width, self.viewFrame.height))

        # Get the cartesian space coords for the top left of the viewframe.
        topleft_x = self.viewPosX - self.unitPerPixel * image.width/2
        topleft_y = self.viewPosY + self.unitPerPixel * image.height/2

        # Go through every pixel and draw its function-defined color to the screen.
        for pix_x in range(image.width):
            for pix_y in range(image.height):
                # Calculate cartesian coordinate values

                x = topleft_x + self.unitPerPixel * pix_x
                y = topleft_y - self.unitPerPixel * pix_y
                z = self.plottingFunction(x, y)
                # Convert Z coordinate into color
                clamped_z = self.__clamp(
                    z, self.minViewHeight, self.maxViewHeight)
                z_ratio = (clamped_z - self.minViewHeight) / \
                    (self.maxViewHeight - self.minViewHeight)
                c = int(z_ratio * 255)
                color = (c, 0, 0)

                image.putpixel((pix_x, pix_y), color)

        image.save(image_dir)

        if useNewImage:
            self.__visual = pygame.image.load(image_dir)

    def draw(self, screen):
        screen.blit(self.__visual, (self.viewFrame.x, self.viewFrame.y))
