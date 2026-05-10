# hellbox-subset

A [hellbox](https://github.com/hellboxpy/hellbox) plugin that subsets fonts by unicode range or glyph name using [fonttools](https://github.com/fonttools/fonttools).

## Usage

```python
from hellbox import Hellbox
from hellbox.jobs.subset import Subset

with Hellbox("subset") as task:
    task.read("build/*.ttf") >> Subset("U+0000-U+007F", "U+00A0-U+00FF") >> task.write("subset")
```

Glyph names can be specified alongside or instead of unicode ranges:

```python
Subset("U+0000-U+007F", glyphs=["space", "nbspace"])
```

## Installation

```sh
hell add hellbox-subset
```

## Development

```sh
uv sync
uv run pytest
```
