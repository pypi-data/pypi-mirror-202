import glob
from PIL import Image, ImageOps


class GifConverter:
    def __init__(self, img_path=None, gif_path=None, resize=(320,240), duration=500):
        """
        Initialize GifConverter with the following parameters:
        
        Args:
            - img_path (str): The path to the images to convert, using a glob pattern (e.g. 'images/*.png').
            - gif_path (str): The path where the output GIF file will be saved (e.g. 'output/filename.gif').
            - resize (Tuple[int, int]): The target size to resize the images, expressed as a tuple of (width, height) in pixels.
            - duration (int): The target duration for each image transition in the GIF, in milliseconds.
        
        Returns:
            - None
        """
        self.img_path = img_path or './*.png'
        self.gif_path = gif_path or './output.gif'
        self.resize = resize
        self.duration = duration
        
    def convert(self):
        """
        Convert images to GIF
        
        Returns:
            - None
        """
        img, *imgs = [ImageOps.fit(Image.open(f), self.resize, Image.LANCZOS) for f in sorted(glob.glob(self.img_path))]
        
        try:
            img.save(
                fp = self.gif_path,
                format = 'GIF',
                append_images = imgs,
                save_all = True,
                duration = self.duration,  # milliseconds
                loop = 0  # 0 means that it will loop forever. By default, the image will not loop.
            )
        except IOError:
            print("Error: file not found or could not be opened.")
        
        print(
            '- img_path: ', self.img_path,
            '\n- gif_path: ', self.gif_path,
            '\n- resize: ', self.resize,
            '\n- duration: ', self.duration,
            '\nSucceded saving GIF file.'
        )

if __name__ == '__main__':
    c = GifConverter('./images/*.png', './output/output.gif', (320, 240))
    c.convert_gif()