# Roses - Poem generator

Roses is a poem generator written in Python. It uses state-of-the-art methods to generate poems.

## Usage
```bash
python main.py -h

python main.py <emotion> <json with wordpairs as list> <number of poems to generate>

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