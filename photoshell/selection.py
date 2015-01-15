

class Selection(object):

    def __init__(self, library_path, query):
        super(Selection, self).__init__()

        self.library_path = library_path
        self.query = query
        self.images = []
        self.current_image = 0

    def append(self, sidecar):
        # hack to prevent image from loading at import time
        # this is because we can't do CI with anything that
        # imports from gi
        from photoshell.image import Image
        image = Image(sidecar.developed_path, sidecar.datetime)
        self.images.append(image)

    def current(self):
        if len(self.images):
            return self.images[self.current_image]
        else:
            return None

    def next(self):
        l = len(self.images)
        if l > 1:
            self.current_image = (self.current_image + 1) % l
        return self.current()

    def prev(self):
        l = len(self.images)
        if l > 1:
            self.current_image = (self.current_image - 1) % l
        return self.current()

    def jump(self, image_path):
        # TODO: there is an idiomatic way to do this
        for i in range(len(self.images)):
            if self.images[i].image_path == image_path:
                self.current_image = i
                break

        return self.current()

    def each(self):
        for image in self.images:
            yield image

    def sort(self, key):
        self.images = sorted(self.images, key=key)
