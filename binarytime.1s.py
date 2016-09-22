#!/usr/local/bin/python3

import datetime
import more_itertools

def bits_iter(time=None):
    fract = fraction_of_day(time)
    while True:
        fract *= 2
        if fract >= 1:
            yield True
            fract -= 1
        else:
            yield False

def fraction_of_day(time=None):
    if time is None:
        time = datetime.datetime.now().time()
    return time.hour / 24 + time.minute / 1440 + time.second / 86400 + time.microsecond / 86400000000

def hex(bits):
    for nybble in more_itertools.chunked(bits, 4):
        while len(nybble) < 4:
            nybble.append(False)
        yield 8 * nybble[0] + 4 * nybble[1] + 2 * nybble[2] + 1 * nybble[3]

if __name__ == '__main__':
    print(''.join('{:X}'.format(nybble) for nybble in hex(more_itertools.take(12, bits_iter()))))
