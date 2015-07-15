

class Selection(object):

    def __init__(self, query):
        super(Selection, self).__init__()

        self.query = query
        self.photos = []
        self.current_image = 0

    def append(self, sidecar):
        self.photos.append(sidecar)

    def current_photo(self):
        if len(self.photos):
            return self.photos[self.current_image]
        else:
            return None

    def next_photo(self):
        l = len(self.photos)
        if l > 1:
            self.current_image = (self.current_image + 1) % l
        return self.current_photo()

    def prev_photo(self):
        l = len(self.photos)
        if l > 1:
            self.current_image = (self.current_image - 1) % l
        return self.current_photo()

    def each_photo(self):
        for photo in self.photos:
            yield photo

    def sort(self, key):
        self.photos = sorted(self.photos, key=key)
