# Gaphor on Windows

## Development Environment

To setup a development environment in Windows:
1) Install Git for Windows from https://gitforwindows.org
1) Go to http://www.msys2.org/ and download the x86_64 installer
1) Follow the instructions on the page for setting up the basic environment
1) Run `C:\msys64\mingw64.exe` - a terminal window should pop up

```bash
$ pacman -Suy
$ pacman -S mingw-w64-x86_64-gcc \
    mingw-w64-x86_64-gtk3 \
    mingw-w64-x86_64-pkg-config \
    mingw-w64-x86_64-cairo \
    mingw-w64-x86_64-gobject-introspection \
    mingw-w64-x86_64-python \
    mingw-w64-x86_64-python-gobject \
    mingw-w64-x86_64-python-cairo \
    mingw-w64-x86_64-python-pip \
    mingw-w64-x86_64-python-setuptools \
    mingw-w64-x86_64-python-wheel
$ echo 'export PATH="/c/Program Files/Git/bin:$PATH"' >> ~/.bash_profile
```

Restart your terminal.

Install Poetry:

```bash
$ pip install poetry
```

[Clone the
repository](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

Create and activate a virtual environment in which Gaphor can be installed.
```bash
$ cd gaphor
$ python -m venv .venv
$ source .venv/bin/activate
```

Install Gaphor and give it a try:

```bash
$ poetry install
$ poetry run gaphor
```

## Packaging for Windows

In order to create an exe installation package for Windows, we utilize
[PyInstaller](https://pyinstaller.org) which analyzes Gaphor to find all the
dependencies and bundle them in to a single folder. We then use a custom bash
script that creates a Windows installer using
[NSIS](https://nsis.sourceforge.io/Main_Page) and a portable installer using
[7-Zip](https://www.7-zip.org).

1. Follow the instructions for settings up a development environment above
1. Run ``C:\msys64\mingw64.exe`` - a terminal window should pop up
```bash
$ cd packaging/windows
$ ./build-installer.sh
```
