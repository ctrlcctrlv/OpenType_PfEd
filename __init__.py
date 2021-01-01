# © 2020 Fredrick R. Brennan                   #
# -------------------------------------------- #
# OpenType `PfEd` table: Python implementation #

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ctypes
import struct
import sys
import warnings
import pprint

# Python (C) `struct` format characters
UINT32 = '>I'
UINT32_LEN = struct.calcsize(UINT32)
INT16 = '>h'
INT16_LEN = struct.calcsize(INT16)
UINT16 = '>H'
UINT16_LEN = struct.calcsize(UINT16)
TYPEFLAG = '>BB'
TYPEFLAG_LEN = struct.calcsize(TYPEFLAG)
COLOR = '>BBBB'
COLOR_LEN = struct.calcsize(COLOR)
TAG = '>ssss'
TAG_LEN = struct.calcsize(TAG)

class PfEdBuffer(object):
    def __init__(self, buf):
        self.buf = buf
        self.offset = 0

    def __len__(self):
        return len(self.buf)

    def get_utf8_string(self):
        ret = bytearray()
        while self.buf[self.offset] != 0:
            ret.append(self.buf[self.offset])
            self.offset += 1
        if self.buf[self.offset] == 0:
            self.offset += 1
        return ret.decode('utf8')

    def parse(self, fmt):
        value = struct.unpack_from(fmt, self.buf, offset=self.offset)
        self.offset += struct.calcsize(fmt)
        return value

class DuplicatedPfEdSubtableWarning(UserWarning):
    pass

# Old docs: http://pfaedit.org/non-standard.html#PfEd
# New docs: https://fontforge.org/docs/techref/non-standard.html#pfed-the-fontforge-extensions-table
class PfEd(object):
    def __init__(self, pfed_buf):
        self.pfed_buf = pfed_buf

    def header(self):
        (v,) = self.pfed_buf.parse(UINT32)
        (c,) = self.pfed_buf.parse(UINT32)
        log("Got PfEd table version {:x} of length {} subtables (length 0x{:08x} bytes)".format(v,c,len(self.pfed_buf)))
        # The table begins with a table header containing a version number ... (currently 0x00010000)
        # This has never changed
        if v != 0x00010000:
            raise UnimplementedError("Non-standard PfEd table detected")
        self.subtable_len = c

    def toc(self):
        self.subtables = dict()

        for i in range(0, self.subtable_len):
            t = ''.join([c.decode('ascii') for c in self.pfed_buf.parse(TAG)])
            (o,) = self.pfed_buf.parse(UINT32)
            log("Subtable tagged {} starts @ 0x{:08x}".format(t,o))
            if t in self.subtables:
                warnings.warn("Duplicated subtable in PfEd, only one will be parsed", DuplicatedPfEdSubtableWarning)
            else:
                self.subtables[t] = o

    def parse(self):
        self.header()
        self.toc()
        for k, v in self.subtables.items():
            self.subtables[k] = getattr(self, k)(v)
        return self.subtables

    # This is quite a mess, but it's not my fault I don't think ...the data structure is bonkers.
    def GPOS(self, offset):
        buf = PfEdBuffer(self.pfed_buf.buf[offset:])
        tbuf = PfEdBuffer(self.pfed_buf.buf[offset:])
        (v,) = buf.parse(UINT16) # version 0
        (c,) = buf.parse(UINT16) # count of lookups in this table
        lookups = list()

        # Get lookup names
        for i in range(0, c):
            (ln,) = buf.parse(UINT16) # offset to lookup name
            tbuf.offset = ln
            lookup_name = tbuf.get_utf8_string()
            (ls,) = buf.parse(UINT16) # offset to lookup subtable structure
            tbuf.offset = ls
            (subtable_count,) = tbuf.parse(UINT16) # count of lookup subtables in this lookup
            lookups.append((lookup_name, subtable_count))

        subtables = list()

        acn_total = 0

        # Get subtable names and how many anchor classes each subtable has
        for (lookup_name, subtable_count) in lookups:
            lookup_subtables = list()
            (ii,) = buf.parse(UINT16)
            for i in range(0, subtable_count):
                (lsn,) = buf.parse(UINT16) # offset to lookup subtable name
                tbuf.offset = lsn
                subtable_name = tbuf.get_utf8_string()
                (acs,) = buf.parse(UINT16) # offset to anchor class structure
       
                if acs != 0x0:
                    tbuf.offset = acs
                    (acn,) = tbuf.parse(UINT16) # count of anchor classes in this lookupsubtable
                else:
                    acn = 0

                acn_total += acn

                lookup_subtables.append((subtable_name, acn))
            subtables.append(lookup_subtables)
        
        anchors = list()
        
        if acn_total > 0:
            buf.parse(UINT16) == (0x0001,)
    
        # Get all the anchors
        for i in range(0, acn_total):
            (anchor_offset,) = buf.parse(UINT16)
            tbuf.offset = anchor_offset
            anchor_name = tbuf.get_utf8_string()
            anchors.append(anchor_name)

        GPOS = list()

        # Re-insert anchor class names from anchor list into subtables
        for ((ln, lc), lookup_subtables) in zip(lookups, subtables):
            lss = list()
            for (sn, total) in lookup_subtables:
                lss.append((sn, anchors[:total]))

            GPOS.append((ln, lss))

        return GPOS

    def GSUB(self, *args, **kwargs):
        return self.GPOS(*args, **kwargs)

    def guid(self, offset):
        buf = PfEdBuffer(self.pfed_buf.buf[offset:])
        tbuf = PfEdBuffer(self.pfed_buf.buf[offset:])

        (v,) = buf.parse(UINT16); assert v == 1 # version 1
        (vgn,) = buf.parse(UINT16) # number of vertical guidelines
        (hgn,) = buf.parse(UINT16) # number of horizontal guidelines
        _unused_mbz = buf.parse(UINT16) # “For now it is undefined”
        (do,) = buf.parse(UINT16) # offset to description of the guideline layer

        tbuf.offset = do
        guideline_layer_desc = tbuf.get_utf8_string()
        types = (["Vertical"]*vgn)+(["Horizontal"]*hgn)

        guidelines = list()

        for i in range(0, hgn):
            (pos,) = buf.parse(INT16)
            (offset,) = buf.parse(UINT16)
            tbuf.offset = offset
            name = tbuf.get_utf8_string()
            guidelines.append(dict(pos=pos, type=types[i], name=name))

        return dict(version=v, guidelines=guidelines, desc=guideline_layer_desc)

    # TODO: Handle glyph-layer point data
    def layr(self, offset):
        buf = PfEdBuffer(self.pfed_buf.buf[offset:])
        tbuf = PfEdBuffer(self.pfed_buf.buf[offset:])

        (v,) = buf.parse(UINT16); assert v == 1 # version 1
        (c,) = buf.parse(UINT16) # number of layers in this sub-table

        layers = list()
        ranges_total = 0

        tbuf2 = PfEdBuffer(self.pfed_buf.buf[offset:])
        for i in range(0, c):
            (layerflags, layertype) = buf.parse(TYPEFLAG)
            (name_offset,) = buf.parse(UINT16)
            tbuf.offset = name_offset
            name = tbuf.get_utf8_string()
            (data_offset,) = buf.parse(UINT32)
            tbuf.offset = data_offset
            (range_count,) = tbuf.parse(UINT16)

            ranges = list()

            for j in range(0, range_count):
                (start,) = tbuf.parse(UINT16)
                (last,) = tbuf.parse(UINT16)
                (offset,) = tbuf.parse(UINT32) # "offset to an array of offsets"
                tbuf2.offset = offset
                offsets = [tbuf2.parse(UINT32)[0] for k in range(start, last+1)]
                ranges.append(dict(start=start, last=last, offsets=offsets))

            layers.append(dict(type=layertype, name=name, ranges=ranges))

        return layers

    def fcmt(self, offset):
        buf = PfEdBuffer(self.pfed_buf.buf[offset:])
        
        # We only handle UTF8 here...UCS2/v0 was done away with in the long, long ago.
        (v,) = buf.parse(UINT16); assert v == 1 # version 0/1
        (c,) = buf.parse(UINT16)

        return buf.get_utf8_string()

    def flog(self, *args, **kwargs):
        return self.fcmt(*args, **kwargs)

    def cmnt(self, offset):
        buf = PfEdBuffer(self.pfed_buf.buf[offset:])
        tbuf = PfEdBuffer(self.pfed_buf.buf[offset:])

        # We only handle UTF8 here...UCS2/v0 was done away with in the long, long ago.
        (v,) = buf.parse(UINT16); assert v == 1 # version 0/1
        (c,) = buf.parse(UINT16)

        comment_structs = list()

        for i in range(0, c):
            (start,) = buf.parse(UINT16)
            (end,) = buf.parse(UINT16)
            (offset,) = buf.parse(UINT32)
            tbuf.offset = offset
            (offset2,) = tbuf.parse(UINT32)
            tbuf.offset = offset2

            comments = [tbuf.get_utf8_string() for i in range(start,end+1)]

            comment_structs.append((start,end,comments))

        return comment_structs

    def colr(self, offset):
        buf = PfEdBuffer(self.pfed_buf.buf[offset:])

        (v,) = buf.parse(UINT16); assert v == 0 # version 0
        (c,) = buf.parse(UINT16)

        colors = list()

        for i in range(0, c):
            (start,) = buf.parse(UINT16)
            (end,) = buf.parse(UINT16)
            color = buf.parse(COLOR)[1:] # color expressed as a 24bit rgb value

            colors.append((start,end,color))

        return colors

    # FIXME
    def cvtc(self, offset):
        raise UnimplementedError("No idea what this is for. Would love to see an example font; open an issue")

def log(*args, **kwargs):
    print("INFO: ", *args, **kwargs, file=sys.stderr)

if __name__ == "__main__":
    with open("examples/PfEd2", "rb") as f:
        pfed_buf = PfEdBuffer(f.read())
        pfed = PfEd(pfed_buf)
        pfed.parse()
        pprint.pprint(pfed.subtables)
