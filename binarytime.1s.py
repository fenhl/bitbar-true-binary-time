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

def decode_bits(bits):
    fract = 0.0
    exp = 1
    for bit in bits:
        if bit:
            fract += 1 / 2 ** exp
        exp += 1
    return (datetime.datetime(1970, 1, 1) + datetime.timedelta(days=fract)).time()

def decode_hex(hex_string):
    for hex_digit in hex_string:
        nybble = int(hex_digit, 16)
        yield bool(nybble & 0b1000)
        yield bool(nybble & 0b0100)
        yield bool(nybble & 0b0010)
        yield bool(nybble & 0b0001)

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
    now = datetime.datetime.now()
    print(''.join('{:X}'.format(nybble) for nybble in hex(more_itertools.take(12, bits_iter(now.time())))))
    print('---')
    print('{:%H:%M:%S}'.format(now.time()))
    print('w{0[1]}.{0[2]}: {1:%Y-%m-%d}'.format(now.date().isocalendar(), now.date()))
