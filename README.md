# ph.sh

Shell scripts for managing photos

## Usage

ph.sh will copy all CR2 files from a directory into a library directory, separating out JPEG previews.

```
echo '/my/library/directory' > ~/.ph.sh
./ph.sh -i /folder/containing/raws
```

ph.py will convert all the CR2 files in your library to TIFFs.

```
virtualenv venv
source venv/bin/activate

pip install numpy
pip install imageio
pip install rawpy

./ph.py
```
