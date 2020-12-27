# gdrive-folder-copy
Tool to copy a full gdrive folder to another location on gdrive using gdrive api v3.

## Requirements
Requires python 3.7 and the ability to install via pip from pypi.

## Installation

Clone the repository and then use to install gdfc (gdrive-folder-copy) and its dependencies:
```bash
pip install .
```

## Usage

It requires a `token.pickle` or a `credentials.json` file to manage api access, as described in 
[the authentication page](https://developers.google.com/drive/api/v3/quickstart/python#step_1_turn_on_the) 
(step 1 only).

One can optionally change the path of the folder to look for authentication files.
Run `gdfc --help` for a detailed help. Main arguments are the name of the source folder, the name of the target folder
and as an option, the name of the new folder (if it must be changed). Full example:
```bash
gdfc "source folder name" "target parent folder name" --target-folder-name "new folder name" --auth-folder-path ./
```

### Know limitations
- doesn't work when multiple folders have the same name
