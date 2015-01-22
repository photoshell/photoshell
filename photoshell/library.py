import os

from photoshell.photo import Photo

from photoshell import raw
from photoshell.selection import Selection
from photoshell.util import hash_file
from photoshell.util import Progress


class Library(object):

    def __init__(self, config):
        super(Library, self).__init__()

        self.library_path = config['library']
        self.import_string = os.path.join(self.library_path,
                                          config['import_path'])
        self.cache_path = os.path.join(self.library_path, '.cache')
        if not os.path.exists(self.library_path):
            os.makedirs(self.library_path)
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
            os.makedirs(os.path.join(self.cache_path, 'tiff'))
            os.makedirs(os.path.join(self.cache_path, 'raw'))
        self.sidecars = []

        raw_path = os.path.join(self.cache_path, 'raw')
        if not os.path.exists(raw_path):
            os.makedirs(raw_path)
        for root, _, files in os.walk(raw_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.sidecars.append(Photo.load(os.path.realpath(file_path)))

    def all(self):
        return self.query(lambda image: True)

    def query(self, match):
        selection = Selection(self.library_path, match)
        for sidecar in self.sidecars:
            if match(sidecar):
                selection.append(sidecar)

        # TODO: in place mutation is terrible
        selection.sort(key=lambda image: image.datetime)
        return selection

    def update(self, selection):
        current = selection.current()
        if current:
            image_path = current.image_path
        new_selection = self.query(selection.query)
        if current:
            new_selection.jump(image_path)
        return new_selection

    def exists(self, photo):
        for sidecar in self.sidecars:
            if photo == sidecar:
                return True
        return False

    def add(self, photo):
        self.sidecars.append(photo)

    def import_path(self, photo):
        file_name, file_ext = os.path.splitext(
            os.path.basename(photo.raw_path))

        import_path = photo.datetime.strftime(self.import_string.format(
            original_filename=file_name,
            file_hash=photo.file_hash,
        )) + file_ext

        # TODO: directory creation should live elsewhere
        import_dir = os.path.dirname(import_path)
        if not os.path.exists(import_dir):
            os.makedirs(import_dir)

        return import_path

    def import_photos(self, path, notify_callback=None, imported_callback=None,
                      copy_photos=True, delete_originals=False):

        photo_count, photo_iterator = self.discover(path)
        progress = Progress(photo_count)

        for photo in photo_iterator():
            if notify_callback:
                notify_callback(os.path.basename(photo.raw_path))

            # Maybe copy the photo
            if copy_photos:
                photo = photo.copy(
                    self.import_path(photo), delete_originals=delete_originals)

            # Develop the photo
            photo = photo.develop(
                write_sidecar=True,
                cache_path=self.cache_path,
            )

            # Add symlink to cache
            symlink_path = os.path.join(
                self.cache_path,
                'raw',
                photo.file_hash,
            )
            os.symlink(photo.raw_path, symlink_path)

            # Add photo to library
            self.add(photo)

            if imported_callback:
                imported_callback(photo.file_hash, progress.advance())

    def discover(self, path):
        photo_list = raw.discover(path)
        new_list = []

        for photo_path in photo_list:
            photo = Photo.load(photo_path, hash_file(photo_path))

            if not self.exists(photo):
                new_list.append(photo)

        def photo_iterator():
            for photo in new_list:
                yield photo

        return len(new_list), photo_iterator
