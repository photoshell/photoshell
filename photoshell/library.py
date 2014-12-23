import hashlib
import os
import shutil
import subprocess

import wand.image

from photoshell.image import Image

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
                new_file_path = os.path.join(
                    self.library_path, 'raw', file_name)
                if file_path != new_file_path:
                    shutil.copyfile(file_path, new_file_path)

                # generate jpg
                thumbnail_name = '{file_hash}.{extension}'.format(
                    file_hash=file_hash,
                    extension='jpg',
                )
                new_thumbnail_path = os.path.join(
                    self.library_path, 'thumbnail', thumbnail_name)

                # TODO: fail gracefully here (or even at startup)
                blob = subprocess.check_output(
                    ['dcraw', '-c', '-e', file_path])

                with wand.image.Image(blob=blob) as image:
                    with image.convert('jpeg') as thumbnail:
                        thumbnail.save(filename=new_thumbnail_path)

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
        self.current_image = (self.current_image + 1) % len(self.images)
        return self.current()

    def prev(self):
        self.current_image = (self.current_image - 1) % len(self.images)
        return self.current()

    def jump(self, photo_hash):
        # TODO: there is an idiomatic way to do this
        for i in range(len(self.images)):
            if self.images[i].hash_code == photo_hash:
                self.current_image = i
                break

        return self.current()
