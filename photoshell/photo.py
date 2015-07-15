from collections import namedtuple
import os
import shutil

from rawkit.raw import Raw


_Photo = namedtuple('Photo', [
    'raw_path',
    'developed_path',
    'file_hash',
])


class Photo(_Photo):

    @classmethod
    def create(cls, raw_path, developed_path, file_hash):
        return cls(
            raw_path=raw_path,
            developed_path=developed_path,
            file_hash=file_hash,
        )

    @property
    def metadata(self):
        with Raw(filename=self.raw_path) as raw:
            metadata = raw.metadata

        return metadata

    def copy(self, new_path, delete_originals=False):
        # copy photo
        existing_photo_path = self.raw_path
        shutil.copyfile(existing_photo_path, new_path)
        # TODO: Make sure the file copied w/o errors first?
        if delete_originals:
            os.unlink(existing_photo_path)

        # copy metadata
        existing_meta_path = self.raw_path + '.yaml'
        if os.path.exists(existing_meta_path):
            shutil.copyfile(existing_meta_path, new_path + '.yaml')
            # TODO: Make sure the file copied w/o errors first?
            if delete_originals:
                os.unlink(existing_meta_path)

        return Photo.create(
            raw_path=new_path,
            developed_path=self.developed_path,
            file_hash=self.file_hash
        )

    def develop(self, cache_path=None):
        # develop photo
        developed_name = '{file_hash}.{extension}'.format(
            file_hash=self.file_hash,
            extension='ppm',
        )

        developed_path = os.path.join(
            cache_path,
            'ppm',
            developed_name,
        )

        if not os.path.isfile(developed_path):
            with Raw(filename=self.raw_path) as raw:
                raw.options.half_size = True
                raw.save(filename=developed_path)

        photo = Photo.create(
            raw_path=self.raw_path,
            developed_path=developed_path,
            file_hash=self.file_hash
        )

        return photo

    def __eq__(self, other):
        return self.file_hash == other.file_hash
