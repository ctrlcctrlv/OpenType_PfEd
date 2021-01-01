# OpenType `PfEd` table: Python implementation

This is a Python implementation of the OpenType `PfEd` (PfaEdit) table.

`PfEd` is a quite obscure table, but quite useful. It has some elements, like guidelines and comments , that are worth more widely standardizing in OpenType I think.

For now this is just a reader that is 90% done as of 1 January 2021.

(Not promising to finish this!)

## Input

Input should be all the raw bytes found in the `PfEd` table of an OpenType (or SFNT) font.

There are two examples in `examples/`:

* `examples/PfEd` — `InterestingPfEdTable.otf`, the example font I posted at [fonttools/fonttools#464](https://github.com/fonttools/fonttools/issues/464) on 28 April 2018 which contains all `PfEd` tables except `cvtc`;
* `examples/PfEd2` — [TT2020](https://github.com/ctrlcctrlv/TT2020)'s `PfEd` in the state it was in on my hard drive 1 January 2021.

## Usage

```python3
from OpenType_PfEd import PfEd, PfEdBuffer

with open("OpenType_PfEd/examples/PfEd2", "rb") as f:
	buf = PfEdBuffer(f.read())
pfed = PfEd(buf)
pfed.parse()
import pprint
pprint.pprint(pfed.subtables)
```

Gives us:

```text
INFO:  Got PfEd table version 10000 of length 4 subtables (length 0x000a60e0 bytes)
INFO:  Subtable tagged GSUB starts @ 0x00000028
INFO:  Subtable tagged GPOS starts @ 0x000005c0
INFO:  Subtable tagged guid starts @ 0x00000608
INFO:  Subtable tagged layr starts @ 0x000007a8
{'GPOS': [('mark1', [('mark1-1', ['theclass'])]),
          ('fracq', [('fracq subtable', [])])],
 'GSUB': [('fracf', [('fracf subtable', [])]),
          ('fracs',
           [('fracs contextual 0', []),
            ('fracs contextual 1', []),
            ('fracs contextual 2', [])]),
          ('Single Substitution lookup 2',
           [('Single Substitution lookup 2 subtable', [])]),
          ('Single Substitution lookup 3',
           [('Single Substitution lookup 3 subtable', [])]),
          ('Single Substitution lookup 4',
           [('Single Substitution lookup 4 subtable', [])]),
          ('fracn', [('fracn subtable', [])]),
          ('Single Substitution lookup 6',
           [('Single Substitution lookup 6 subtable', [])]),
          ('fracn3', [('fracn3 subtable', [])]),
          ('Single Substitution lookup 8',
           [('Single Substitution lookup 8 subtable', [])]),
          ('fracn4', [('fracn4 subtable', [])]),
          ('Single Substitution lookup 10',
           [('Single Substitution lookup 10 subtable', [])]),
          ('fracn5', [('fracn5 subtable', [])]),
          ('Single Substitution lookup 12',
           [('Single Substitution lookup 12 subtable', [])]),
          ('fracn6', [('fracn6 subtable', [])]),
          ('Single Substitution lookup 14',
           [('Single Substitution lookup 14 subtable', [])]),
          ('fracn7', [('fracn7 subtable', [])]),
          ('Single Substitution lookup 16',
           [('Single Substitution lookup 16 subtable', [])]),
          ('fracn8', [('fracn8 subtable', [])]),
          ('Single Substitution lookup 18',
           [('Single Substitution lookup 18 subtable', [])]),
          ('fracn9', [('fracn9 subtable', [])]),
          ('Single Substitution lookup 20',
           [('Single Substitution lookup 20 subtable', [])]),
          ('fracn10', [('fracn10 subtable', [])]),
          ('Single Substitution lookup 22',
           [('Single Substitution lookup 22 subtable', [])]),
          ('ligahebrew', [('ligahebrew subtable', [])]),
          ('ligalatin', [('ligalatin subtable', [])])],
 'guid': {'desc': '',
          'guidelines': [{'name': 'Bottom (Cyrl)',
                          'pos': -130,
                          'type': 'Horizontal'},
                         {'name': 'Bottom (Hebr)',
                          'pos': -97,
                          'type': 'Horizontal'},
                         {'name': 'Bottom (yud, Hebr)',
                          'pos': 225,
                          'type': 'Horizontal'},
                         {'name': 'Mid-bar (Armn)',
                          'pos': 259,
                          'type': 'Horizontal'},
                         {'name': 'Mid-bar (Cyrl)',
                          'pos': 292,
                          'type': 'Horizontal'},
                         {'name': 'x-height', 'pos': 404, 'type': 'Horizontal'},
                         {'name': 'Top (Hebr)',
                          'pos': 460,
                          'type': 'Horizontal'},
                         {'name': 'Top (Cyrl)',
                          'pos': 529,
                          'type': 'Horizontal'}],
          'version': 1},
 'layr': [{'name': 'Spiro',
           'ranges': [{'last': 0, 'offsets': [1065], 'start': 0},
                      {'last': 5, 'offsets': [2648], 'start': 5},
                      {'last': 15,
                       'offsets': [5112, 0, 7632, 0, 8084],
                       'start': 11},
                      {'last': 23, 'offsets': [8320], 'start': 23},
                      {'last': 27, 'offsets': [9596, 11016], 'start': 26},
                      {'last': 33, 'offsets': [11482], 'start': 33},
                      {'last': 43,
                       'offsets': [15341, 16338, 18448, 20180, 21789, 0, 23027],
                       'start': 37},
                      {'last': 51,
                       'offsets': [24105, 25387, 27919],
                       'start': 49},
                      {'last': 54, 'offsets': [29394], 'start': 54},
                      {'last': 58, 'offsets': [30342], 'start': 58},
                      {'last': 85,
                       'offsets': [31264,
                                   31680,
                                   33334,
                                   34930,
                                   36480,
                                   0,
                                   38193,
                                   39312,
                                   41769,
                                   0,
                                   43469,
                                   44547,
                                   45969,
                                   46417,
                                   48995,
                                   50389,
                                   51782,
                                   53374,
                                   55164,
                                   56229,
                                   58112],
                       'start': 65},
                      {'last': 90, 'offsets': [59433], 'start': 90},
                      {'last': 98,
                       'offsets': [60908, 0, 61612, 63176],
                       'start': 95},
                      {'last': 101, 'offsets': [64128], 'start': 101},
                      {'last': 104, 'offsets': [66880], 'start': 104},
                      {'last': 112,
                       'offsets': [69223, 0, 71428, 72663, 0, 74195],
                       'start': 107},
                      {'last': 161, 'offsets': [74944], 'start': 161},
                      {'last': 171, 'offsets': [77332], 'start': 171},
                      {'last': 327, 'offsets': [78802, 0, 79272], 'start': 325},
                      {'last': 333, 'offsets': [80116], 'start': 333},
                      {'last': 372, 'offsets': [80748], 'start': 372},
                      {'last': 383, 'offsets': [82352, 0, 84438], 'start': 381},
                      {'last': 396,
                       'offsets': [86524, 88268, 0, 89661],
                       'start': 393},
                      {'last': 410, 'offsets': [91657], 'start': 410},
                      {'last': 420, 'offsets': [93154, 0, 95506], 'start': 418},
                      {'last': 428, 'offsets': [97524], 'start': 428},
                      {'last': 435, 'offsets': [99233], 'start': 435},
                      {'last': 448, 'offsets': [100996], 'start': 448},
                      {'last': 465, 'offsets': [104322], 'start': 465},
                      {'last': 476, 'offsets': [105406, 107848], 'start': 475},
                      {'last': 480, 'offsets': [109282], 'start': 480},
                      {'last': 501, 'offsets': [113931, 115077], 'start': 500},
                      {'last': 540, 'offsets': [116535], 'start': 540},
...[snip]...
```
