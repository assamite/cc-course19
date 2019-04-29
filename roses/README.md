# Roses - Poem generator

Roses is a poem generator written in Python. It uses state-of-the-art methods to generate poems.

## Usage
```console
$ python roses.py -h
usage: roses.py [-h] emotion word_pairs num_poems

positional arguments:
  emotion     Emotion for poem.
  word_pairs  File for word pairs. Json list of lists
  num_poems   Number of poems to output.

optional arguments:
  -h, --help  show this help message and exit

$ python roses.py <emotion> <json with wordpairs as list> <number of poems to generate>

```
for example
```
$ python3 roses.py happy input.json 5
```

```python
from roses import PoemGenerator

poem_creator = PoemCreator()
poems = poem_creator.create('sad', [('human', 'boss'), ('animal', 'legged')], 10)

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Lisence
TBD
