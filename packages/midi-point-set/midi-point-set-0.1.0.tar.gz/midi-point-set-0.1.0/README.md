# MIDI to Point Set Converter

This Python library converts MIDI files to point set representation, which
encodes notes as pairs of integers encoding the pitch and time. The output can
be used for machine learning tasks such as music generation.

## Requirements

- Python 3.7 or higher

## Installation

```sh
pip install midi_point_set
```

## Usage

### CLI

```sh
# JSON output

python -m midi-point-set --input-midi K545-1.mid --output-json mozart.json

# Plot
# (requires matplotlib installed)
python -m midi-point-set --input-midi K545-1.mid --output-plot mozart.svg
```

### Library

```py
from midi_point_set import get_point_set

point_set = get_point_set("mozart.midi")
print(point_set[:5])
```
