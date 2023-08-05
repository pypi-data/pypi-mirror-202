Examples
=======================

## Basic setings 
<br>

Notes are quarter notes by default
```python
import isedit
Piece = isedit.Piece
p1 = Piece(120)
p1.addVoice("c c c c")
p1.play()
p1.getScore()
```

<br>

Octaves are set with the `,` and `'` symbols 
```python
Piece = isedit.Piece
p1 = Piece(120)
p1.addVoice("c, c c' c''")
p1.play()
p1.getScore()
```
<br>


We can change the time signature
```python
p1 = isedit.Piece(120, "3/4")
p1.addVoice("c' d' e'")
p1.play()
p1.getScore()
```

<br>


We can add flats by adding `es` and sharps by adding `is` to the ends of notes
```python
p1 = isedit.Piece(120, "3/4")
p1.addVoice("c' d' ees'")
p1.play()
p1.getScore()
```
<br>


## Changing note lengths
We can change note lengths; 
2 is a half note, 4 is a quartner note, 8 is and 8th note, and so on
```python
p1 = isedit.Piece(120, "3/4")
p1.addVoice("c'4 d'8 dis'8 f'4")
p1.play()
p1.getScore()
```

<br>

And can add dotted notes
```python
p1 = isedit.Piece(120, "3/4")
p1.addVoice("c'4 d'8 ees'4.")
p1.play()
p1.getScore()
```
<br>


## Multiple voices
We can also add multiple voices

```python
p1 = isedit.Piece(120, "3/4")
p1.addVoice("c'4 d'8 ees'8 f'4")
p1.addVoice("g2.")
p1.play()
p1.getScore()
```




