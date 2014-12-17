# ph.sh (photoshell)

Utilities for Managing Photos

## Usage

Before you run `photoshell` you need to be in a virtualenv and install any
dependencies. The following example will create and activate a virtualenv,
then install dependencies from requirements.txt.

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Once your virtualenv is activated and setup, you can run `photoshell` by doing
`python -m photoshell` from the root directory of the project.

## Legacy Usage

Legacy files are located in the `legacy` folder.

ph.sh will copy all CR2 files from a directory into a library directory,
separating out JPEG previews.

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
