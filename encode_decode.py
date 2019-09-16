#! /usr/bin/env python
# encoding: utf-8

# Copyright Steinwurf ApS 2015.
# Distributed under the "STEINWURF EVALUATION LICENSE 1.0".
# See accompanying file LICENSE.rst or
# http://www.steinwurf.com/licensing

import os
import sys

import kodo

import datetime

str1 = "dafddddddddddddddddddddddddddddddddddddddfsdfadfsadfasdfssfsfsdfsdafsdfsdfsdfsdgfdgfdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdffsdfsdfsdfsdfsdfsdfsdfsdfsdfssdfsddafddddddddddddddddddddddddddddddddddddddfsdfadfsadfasdfssfsfsdfsdafsdfsdfsdfsdgfdgfdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdffsdfsdfsdfsdfsdfsdfsdfsdfsdfssdfsddafddddddddddddddddddddddddddddddddddddddfsdfadfsadfasdfssfsfsdfsdafsdfsdfsdfsdgfdgfdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdffsdfsdfsdfsdfsdfsdfsdfsdfsdfssdfsddafddddddddddddddddddddddddddddddddddddddfsdfadfsadfasdfssfsfsdfsdafsdfsdfsdfsdgfdgfdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdffsdfsdfsdfsdfsdfsdfsdfsdfsdfssdfsddafddddddddddddddddddddddddddddddddddddddfsdfadfsadfasdfssfsfsdfsdafsdfsdfsdfsdgfdgfdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdffsdfsdfsdfsdfsdfsdfsdfsdfsdfssdfsddafddddddddddddddddddddddddddddddddddddddfsdfadfsadfasdfssfsfsdfsdafsdfsdfsdfsdgfdgfdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdffsdfsdfsdfsdfsdfsdfsdfsdfsdfssdfsddafddddddddddddddddddddddddddddddddddddddfsdfadfsadfasdfssfsfsdfsdafsdfsdfsdfsdgfdgfdfsdklhlhkjlkjldfsadfa"

str1 = str1 * 1024

str1 = str1 * 125


def main():
    """Simple example showing how to encode and decode a block of memory."""
    # Choose the finite field, the number of symbols (i.e. generation size)
    # and the symbol size in bytes
    field = kodo.field.binary16
    symbols = 125
    symbol_size = 1024 * 1024

    # Create an encoder/decoder factory that are used to build the
    # actual encoders/decoders
    encoder_factory = kodo.RLNCEncoderFactory(field, symbols, symbol_size)
    encoder = encoder_factory.build()

    decoder_factory = kodo.RLNCDecoderFactory(field, symbols, symbol_size)
    decoder = decoder_factory.build()
    print("2")

    # Generate some random data to encode. We create a bytearray of the same
    # size as the encoder's block size and assign it to the encoder.
    # This bytearray must not go out of scope while the encoder exists!
    data_in = bytearray(str1)
    print("3")
    # data_in = bytearray(os.urandom(encoder.block_size()))
    encoder.set_const_symbols(data_in)

    print("1")

    # Define the data_out bytearray where the symbols should be decoded
    # This bytearray must not go out of scope while the encoder exists!
    # data_out = bytearray(decoder.block_size())
    data_out = bytearray(decoder.block_size())

    print("size:", decoder.block_size())
    decoder.set_mutable_symbols(data_out)

    packet_number = 0
    x = datetime.timedelta(0)
    y = datetime.timedelta(0)
    while not decoder.is_complete():
        starttime = datetime.datetime.now()

        # Generate an encoded packet
        packet = encoder.write_payload()
        # print("Packet {} encoded!".format(packet_number))

        endtime = datetime.datetime.now()
        x = x + (endtime - starttime)
        # print("encode time:",(endtime - starttime))

        # Pass that packet to the decoder
        decoder.read_payload(packet)
        # print("Packet {} decoded!".format(packet_number))
        packet_number += 1
        # print("rank: {}/{}".format(decoder.rank(), decoder.symbols()))

        endtime1 = datetime.datetime.now()
        y = y + (endtime1 - endtime)
        # print("decode time:",(endtime1 - endtime))

    print("Coding finished")
    print(x)
    print(y)

    # The decoder is complete, the decoded symbols are now available in
    # the data_out buffer: check if it matches the data_in buffer
    print("Checking results...")
    if data_out == data_in:
        print("Data decoded correctly")
    else:
        print("Unable to decode please file a bug report :)")
        sys.exit(1)


if __name__ == "__main__":
    main()
