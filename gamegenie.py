#!/usr/bin/python2

"""Module to encode/decode Game Genie codes.

    The algorithm used to decode was taken from info available at
    http://tuxnes.sourceforge.net/gamegenie.html

    See file LICENSE for license information.
"""
# Mapping and reverse mapping of Game Genie letters to nibbles
code2letter = [ 'A', 'P', 'Z', 'L',
                'G', 'I', 'T', 'Y',
                'E', 'O', 'X', 'U',
                'K', 'S', 'V', 'N' ];

letter2code = dict(  zip( code2letter, range(len(code2letter)) )  );

def decode(ggcode):
    """Decode a Game Genie cheatcode.

    Accepts a string (in either case) that must be a valid Game Genie code,
    and returns a dictionary containing the keys address, data, and comp.
    Their values are respectively: the address to patch (within 0x8000-0xFFF),
    the value to be read at this address (0x00-0xFF) and the compare value
    (0x00-0xFF) or None if the compare function is not used (so the code is 6
    character long).
    """
    if 6 != len(ggcode) != 8:
        raise ValueError(
                    "Game Genie code must be either 6 or 8 characters long"
                    );

    ggcode.upper();

    # Decode to raw code (nibbles)
    rc = None;
    try:
        rc = [ letter2code[i] for i in ggcode ];
    except KeyError:
        raise ValueError(
                    "Invalid Game Genie code (character(s) found not in [" +
                    ''.join(code2letter) + "])"
                    );

    # This is from the resource mentioned in the link at the top of the file
    address = (
              0x8000 |
              ((rc[3] & 7) << 12) |
              ((rc[5] & 7) << 8)  | ((rc[4] & 8) << 8) |
              ((rc[2] & 7) << 4)  | ((rc[1] & 8) << 4) |
               (rc[4] & 7)        |  (rc[3] & 8)
              );

    # Every code I've seen have the MSB set for the 3rd nibble, I don't know if
    # it's mandatory, but I print a warning just in case.
    if not rc[2] & 0x8:
        print ("warning: 3rd character is not one of [" +
               ''.join(code2letter[8:]) + "]");

    data = None;
    comp = None;

    if len(ggcode) == 6:
        # Address patch without compare (6-letter code)
        data = (
                ((rc[1] & 7) << 4) | ((rc[0] & 8) << 4) |
                 (rc[0] & 7)       |  (rc[5] & 8)
               );
    else:
        # Addess patch with compare (8-letter code)
        # (len is 8, because it can only be 6 or 8 because of the precondition
        # test).
        data = (
                ((rc[1] & 7) << 4) | ((rc[0] & 8) << 4) |
                 (rc[0] & 7)       |  (rc[7] & 8)
               );
        comp = (
                ((rc[7] & 7) << 4) | ((rc[6] & 8) << 4) |
                 (rc[6] & 7)       |  (rc[5] & 8)
               );

    return dict(
            address = address,
            data = data,
            comp = comp
           );

def human_readable_patch(address, data, comp = None):
    """Returns a human readable string describing the patching action.
    """

    s = "[0x%04X] returns 0x%02X" % (address, data);

    if comp is not None:
        s += " if read as 0x%02X" % comp;

    return s;

def __boundchecks(name,value,lowerbound,upperbound):
    """(Internal) Boundchecks value, raise an exception if the value is out of
    bounds
    """
    if not lowerbound <= value <= upperbound:
        raise ValueError("'%s' is not within 0x%X--0x%X (%s = 0x%X)" %
                            (name, lowerbound, upperbound, name, value)
                        );

def encode(address, data, comp = None, altcode = False):
    """Create a Game Genie code from address, data and optional compare value.

    Return a string which is a Game Genie code from an address, an overiding
    value and an optional compare value. If altcode is true, return a slightly
    different code where the 3rd char has its MSB cleared; the resulting code
    may or may not work, I don't know; that code, when given to `decode`, will
    give a warning.
    """

    __boundchecks(
            name="address",value=address,lowerbound=0x8000,upperbound=0xFFFF
            );
    __boundchecks(
            name="data",   value=data,   lowerbound=0x00,  upperbound=0xFF
            );
    codes = [0] * 6;

    # Alias to save typing...
    c = codes;

    #address = (
    #          0x8000 |
    #          ((rc[3] & 7) << 12) |
    #          ((rc[5] & 7) << 8)  | ((rc[4] & 8) << 8) |
    #          ((rc[2] & 7) << 4)  | ((rc[1] & 8) << 4) |
    #           (rc[4] & 7)        |  (rc[3] & 8)

    c[5] = ((address >> 8)  & 7);
    c[4] = ((address >> 8)  & 8) | (address & 7);
    c[3] = ((address >> 12) & 7) | (address & 8);
    c[2] = ((address >> 4)  & 7) | (0 if altcode else 8);
    c[1] = ((address >> 4)  & 8) | ((data >> 4) & 7);
    c[0] = ((data >> 4) & 8) | (data & 7);

    if comp is not None:
        __boundchecks(
                name="comp", value=comp, lowerbound=0x00, upperbound=0xFF
                );
        c.extend([0, 0]);
        #data = (
        #        ((rc[1] & 7) << 4) | ((rc[0] & 8) << 4) |
        #         (rc[0] & 7)       |  (rc[7] & 8)
        #       );
        #comp = (
        #        ((rc[7] & 7) << 4) | ((rc[6] & 8) << 4) |
        #         (rc[6] & 7)       |  (rc[5] & 8)
        #       );
        c[5] |= comp & 8;
        c[6]  = ((comp >> 4) & 8) | (comp & 7);
        c[7]  = ((comp >> 4) & 7) | (data & 8);
    else:
        #data = (
        #        ((rc[1] & 7) << 4) | ((rc[0] & 8) << 4) |
        #         (rc[0] & 7)       |  (rc[5] & 8)
        #       );
        c[5] |= data & 8;

    return ''.join(code2letter[i] for i in codes);

