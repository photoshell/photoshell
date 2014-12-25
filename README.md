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

You will also need to create a config file for `photoshell`. A basic example
just defines where the `photoshell` library will live.

```
echo 'library: /home/cameron/Pictures/photoshell_library' > ~/.photoshell.yaml
```

Once your virtualenv is setup and activated, and you have a config file, you
can run the `photoshell` image viewer by doing `python -m photoshell` from the
project root.
