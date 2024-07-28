# PyCrypt

PyCrypt is a command-line tool for encrypting and decrypting files and folders.

## Features

- **Encrypt Folders**: Compresses and encrypts entire folders.
- **Decrypt Folders**: Decrypts and decompresses ZIP archives back to their original state.
- **Encrypt Files**: Encrypts individual files.
- **Decrypt Files**: Decrypts individual files.

## Requirements

- Python 3.6 or higher
- `cryptography` library

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/carlos-dev-research/pycrypt.git
   cd pycrypt
   ```

2. **Install the required library:**:

    ```sh
    pip install cryptography
    ```

## Usage

### Encrypt a Folder

Encrypts a folder by compressing it into a ZIP file and encrypting the ZIP file.

```sh
python pycrypt.py encrypt /path/to/folder
```

### Decrypt a File

Decrypts an individual encrypted file.

```sh
python pycrypt.py decrypt /path/to/file.encrypted
```

## Acknowledgments

This project uses the following Python libraries:

- [cryptography](https://github.com/pyca/cryptography)

