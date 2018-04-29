from PIL import Image
from multiprocessing import Process


class ImageGenerator(Process):
    def __init__(self, bg_color, stencil_color, bg_size, bg_color_index, stencil_color_index, staple_size, xy_diff, staple, prefix, suffix):
        Process.__init__(self)
        self.bg_color = bg_color
        self.bg_color_index = bg_color_index
        self.bg_size = bg_size
        self.stencil_color = stencil_color
        self.stencil_color_index = stencil_color_index
        self.staple_size = staple_size
        self.xy_diff = xy_diff
        self.staple = staple
        self.prefix = prefix
        self.suffix = suffix

    def run(self):
        bg = Image.new('RGB', self.bg_size, self.bg_color)
        bg.paste(Image.new('RGB', self.staple_size, self.stencil_color), self.xy_diff, self.staple)
        bg.save("%s%s-%s%s" % (self.prefix, self.bg_color_index, self.stencil_color_index, self.suffix))
        print("Finished (%i, %i), (%s, %s)" % (self.bg_color_index, self.stencil_color_index,
                                               self.bg_color, self.stencil_color))
