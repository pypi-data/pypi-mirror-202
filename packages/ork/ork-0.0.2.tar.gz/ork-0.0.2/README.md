# Ork

[![Actions Status](https://github.com/bonnal-enzo/ork/workflows/test/badge.svg)](https://github.com/bonnal-enzo/ork/actions) [![Actions Status](https://github.com/bonnal-enzo/ork/workflows/PyPI/badge.svg)](https://github.com/bonnal-enzo/ork/actions)

## Install

`python -m pip install ork`

## Usage

```python
>>> from ork import 
>>> ng = NameGenerator()
>>> ng.generate(faction="orks", lang="en")
'Snarkrat Wurldkilla'
>>> ng.generate(faction="orks", lang="fr")
"Droknog Botte lé Fess'"
>>> ng.generate(faction="space wolves", lang="en")
'Berek Wyrdfang'
>>> ng.generate(faction="space wolves", lang="fr")
'Leif Le Berserk'
```

## Dev

```bash
python -m venv .venv
source ./.venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest
```
