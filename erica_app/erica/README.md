# Steuerlotse Erica service

## Getting started 🛠

### Install Python dependencies

```bash
cd erica_app/
pipenv install
```

### Download ERiC

Erica uses Pyeric, which is a wrapper around ERiC. For this to work you will need to download the latest ERiC 
library and place the required library files in a `lib` folder.

 - Set the environment variable `ERICA_ENV` to `testing`, `development` or similar.
 - Download `ERiC-32.2.4.0-Linux-x86_64.jar` (or a newer version) from the [ELSTER developer portal](https://www.elster.de/elsterweb/infoseite/entwickler).
 - Place the following files into a `lib` folder in _this directory_ such that it matches the given structure:

```bash
pyeric$ tree lib
lib
├── libericapi.so
├── libericxerces.so
├── libeSigner.so
└── plugins2
    ├── libcheckElsterDatenabholung.so
    ├── libcheckESt_2020.so
    ├── libcheckVaSt.so
    └── libcommonData.so
```

_NOTE_: If you use a Mac, get the corresponding `*.dylib` files

### Obtain Certificate

You also need to obtain a test certificate from ELSTER and place it under `erica/instances/blueprint/cert.pfx`.

## Developing 👩‍💻 👨‍💻

```bash
cd erica_app/
export ERICA_ENV=development
python -m erica 
```

## Testing 📃

You can run tests as follows:
```bash
cd erica_app/
pipenv run pytest
```

If you are missing the ERiC library or a suitable certificate then the respective 
tests will be skipped.
