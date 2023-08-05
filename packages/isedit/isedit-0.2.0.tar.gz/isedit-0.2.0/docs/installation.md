Installation
=======================

Prerequisites:
* Python >=3.7,
* lilypond, portaudio
* numpy, pyaudio, midiutil, ipython, pygame

To install python packages:
```bash
$ pip install numpy
$ pip install pyaudio
$ pip install midiutil
$ pip install ipython
$ pip install pygame
```

Lilypond (https://lilypond.org) and portaudio (http://www.portaudio.com) can be installed from their websites, with brew
```
$ brew install lilypond
$ brew install portaudio
```
or with apt
```
# sudo apt install portaudio19-dev python3-pyaudio
# sudo apt install -y lilypond
```

Ensure that lilypond runs from the command line by running 
```bash
$ lilypond --version
```
