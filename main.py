from PIL import Image, ImageFilter
from multiprocessing import Process
import imagegenerator


class BGCreator(Process):
    def __init__(self, stencil_color_list =(
            '#1c1d1c', '#1f2f3f',
            '#1a7461', '#00a169',
            '#88c591', '#5ec5ed',
            '#99d3db', '#ffde85',
            '#ffe169', '#f8ae61',
            '#ea573c', '#d6174a',
            '#923f3f', '#4b4643',
            '#ededed'), bg_color_list =(
            '#1c1d1c', '#1f2f3f',
            '#5ec5ed', '#99d3db',
            '#923f3f',
            '#4b4643', '#ededed'),
             scale_factor = 1/10,
             logo_filename="castle_black.png",
             prefix="out/castle",
             suffix=".png",
             x_offset=1/4,
             y_offset=1/2,
             img_size=(2560, 1440)):
        Process.__init__(self)
        self.stencil_color_list = stencil_color_list
        self.bg_color_list = bg_color_list
        self.scale_factor = scale_factor
        self.logo_filename = logo_filename
        self.prefix = prefix
        self.suffix = suffix
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.img_size = img_size

    def run(self):
        # open the staple
        staple = Image.open(self.logo_filename)
        # Blur the mask
        if self.scale_factor < .5:
            staple = staple.filter(ImageFilter.GaussianBlur(4))
        # get the staple size
        staple_size = staple.size
        # resize the staple
        staple = staple.resize((int(staple_size[0] * self.scale_factor), int(staple_size[1] * self.scale_factor)))
        # sharpen the mask
        # staple = staple.filter(ImageFilter.SHARPEN)
        # get the staple size
        staple_size = staple.size

        # get the xy offset
        xy_diff = (int((self.img_size[0]*self.x_offset)-(staple_size[0]/2)),
                   int((self.img_size[1]*self.y_offset)-(staple_size[1]/2)))
        print("Image Size: %sx%s" % self.img_size)
        print("Staple Size: %sx%s" % staple_size)
        print("Staple Offset: %sx%s" % xy_diff)

        processes = []
        for bg_color_index, bg_color in enumerate(self.bg_color_list):
            for stencil_color_index, stencil_color in enumerate(self.stencil_color_list):
                if not bg_color == stencil_color:
                    processes.append(imagegenerator.ImageGenerator(bg_color, stencil_color, self.img_size,
                                                                   bg_color_index, stencil_color_index, staple_size,
                                                                   xy_diff, staple, self.prefix, self.suffix))

        print("Starting Processes")
        for i in processes:
            i.start()

        for i in processes:
            i.join()


if __name__ == "__main__":
    # castle
    BGCreator(stencil_color_list =(
            '#1c1d1c', '#1f2f3f',
            '#1a7461', '#00a169',
            '#88c591', '#ffde85',
            '#ffe169', '#f8ae61',
            '#ea573c', '#d6174a',
            '#923f3f', '#4b4643',
            '#ededed'), bg_color_list=(
            '#1c1d1c', '#1f2f3f',
            '#99d3db', '#923f3f',
            '#4b4643', '#ededed'),
             scale_factor=1 / 10,
             logo_filename="castle_black.png",
             prefix="out/castle",
             suffix=".png",
             x_offset=1/4,
             y_offset=1/2,
             img_size=(2560, 1440)).start()
