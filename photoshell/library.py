import os

raw_formats = ['CR2']
thumbnail_formats = ['JPG', 'jpg']


class Library(object):

    def __init__(self, library_path):
        super(Library, self).__init__()

        self.library_path = library_path
        self.hashes = []

        for root, _, files in os.walk(os.path.join(library_path, 'thumbnail')):
            for file_name in files:
                if file_name.split('.')[-1] in thumbnail_formats:
                    self.hashes.append(file_name.split('/')[-1].split('.')[0])

    def all(self):
        return self.query(lambda image: True)

    def query(self, match):
        selection = Selection()
        for hash_code in self.hashes:
            image = Image(self.library_path, hash_code)
            if match(image):
                selection.append(image)

        return selection


class Image(object):

    def __init__(self, library_path, hash_code):
        # TODO: refactor this to not need a library_path
        super(Image, self).__init__()
        self.thumbnail = os.path.join(
            library_path, 'thumbnail', hash_code + '.JPG')


class Selection(object):

    def __init__(self):
        super(Selection, self).__init__()
        self.images = []
        self.current_image = 0

    def append(self, image):
        self.images.append(image)

    def current(self):
        return self.images[self.current_image]

    def next(self):
        self.current_image = (self.current_image + 1) % len(self.images)
        return self.current()

    def prev(self):
        self.current_image = (self.current_image - 1) % len(self.images)
        return self.current()
