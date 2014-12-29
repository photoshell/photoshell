import hashlib
import os
import shutil
import subprocess

import wand.image

from photoshell.image import Image

raw_formats = ['CR2']
exposed_formats = ['tiff']


class Library(object):

    def __init__(self, config):
        super(Library, self).__init__()

        self.library_path = config['library']
        self.cache_path = os.path.join(self.library_path, '.cache')
        if not os.path.exists(self.library_path):
            os.makedirs(self.library_path)
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        self.hashes = []

        for root, _, files in os.walk(self.cache_path):
            for file_name in files:
                if file_name.split('.')[-1] in exposed_formats:
                    self.hashes.append(file_name.split('/')[-1].split('.')[0])

    def all(self):
        return self.query(lambda image: True)

    def query(self, match):
        selection = Selection(self.library_path, match)
        for hash_code in self.hashes:
            image = Image(hash_code)
            if match(image):
                selection.append(image)

        return selection

    def update(self, selection):
        current = selection.current()
        if current:
            photo_hash = current.hash_code
        new_selection = self.query(selection.query)
        if current:
            new_selection.jump(photo_hash)
        return new_selection

    def import_photos(self, path, notify=None, imported=None):
        file_list = []

        for root, _, files in os.walk(path):
            for file_name in files:
                if file_name.split('.')[-1] in raw_formats:
                    file_path = os.path.join(root, file_name)
                    file_list.append(file_path)

        num_complete = 0

        for file_path in file_list:
            # TODO: skip if already imported

            if notify:
                notify(file_path.split('/')[-1])

            file_hash = self.hash_file(file_path)

            if file_hash not in self.hashes:
                # copy file
                file_name = '{file_hash}.{extension}'.format(
                    file_hash=file_hash,
                    extension=file_path.split('/')[-1].split('.')[-1],
                )
                new_file_path = os.path.join(self.library_path, file_name)
                if file_path != new_file_path:
                    shutil.copyfile(file_path, new_file_path)

                # create metadata

                # generate jpg
                exposed_name = '{file_hash}.{extension}'.format(
                    file_hash=file_hash,
                    extension='tiff',
                )
                exposed_path = os.path.join(
                    self.cache_path,
                    exposed_name
                )

                if not os.path.isfile(exposed_path):
                    # TODO: fail gracefully here (or even at startup)
                    blob = subprocess.check_output(
                        ['dcraw', '-c', '-e', file_path])

                    with wand.image.Image(blob=blob) as image:
                        with image.convert('jpeg') as exposed:
                            exposed.save(filename=exposed_path)

                self.hashes.append(file_hash)

            num_complete += 1

            if imported:
                imported(file_hash, num_complete / len(file_list))

    # TODO: this shouldn't live on self
    def hash_file(self, file_path):
        hash = hashlib.sha1()

        # TODO: probably block size or something, although if your machine
        # can't hold the whole file in memory you probably can't edit it
        # anyway.
        with open(file_path, 'rb') as f:
            data = f.read()

        hash.update(data)
        return hash.hexdigest()


class Selection(object):

    def __init__(self, library_path, query):
        super(Selection, self).__init__()

        self.library_path = library_path
        self.query = query
        self.images = []
        self.current_image = 0

    def append(self, image):
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

    def jump(self, photo_hash):
        # TODO: there is an idiomatic way to do this
        for i in range(len(self.images)):
            if self.images[i].hash_code == photo_hash:
                self.current_image = i
                break

        return self.current()

    def each(self):
        for image in self.images:
            yield image
