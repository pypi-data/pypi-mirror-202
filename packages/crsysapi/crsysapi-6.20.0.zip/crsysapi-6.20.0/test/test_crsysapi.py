#! python3
# -*- coding: utf-8 -*-

"""Some tests for ``crsysapi.py`` the Python interface to CryptoSys API"""

# test_crsysapi.py: version 6.20.0
# $Date: 2023-04-09 08:37:00 $

# ************************** LICENSE *****************************************
# Copyright (C) 2023 David Ireland, DI Management Services Pty Limited.
# All rights reserved. <www.di-mgt.com.au> <www.cryptosys.net>
# The code in this module is licensed under the terms of the MIT license.
# For a copy, see <http://opensource.org/licenses/MIT>
# ****************************************************************************

import crsysapi
import os
import sys
import pytest
import shutil
from glob import iglob

_MIN_API_VERSION = 62000
do_all = True

print("crsysapi version =", crsysapi.__version__)
# Show some info about the core native DLL
print("API core version =", crsysapi.Gen.version())
print("module_name =", crsysapi.Gen.module_name())
print("compile_time =", crsysapi.Gen.compile_time())
print("platform =", crsysapi.Gen.core_platform())
print("licence_type =", crsysapi.Gen.licence_type())
# print("module_info =", crsysapi.Gen.module_info())
# Show some system values
print("sys.getdefaultencoding()=", sys.getdefaultencoding())
print("sys.getfilesystemencoding()=", sys.getfilesystemencoding())
print("sys.platform()=", sys.platform)
print("cwd =", os.getcwd())

if crsysapi.Gen.version() < _MIN_API_VERSION:
    raise Exception('Require API version ' +
                    str(_MIN_API_VERSION) + ' or greater')


# FILE-RELATED UTILITIES
def read_binary_file(fname):
    with open(fname, "rb") as f:
        return bytearray(f.read())


def write_binary_file(fname, data):
    with open(fname, "wb") as f:
        f.write(data)


def read_text_file(fname, enc='utf8'):
    with open(fname, encoding=enc) as f:
        return f.read()


def write_text_file(fname, s, enc='utf8'):
    with open(fname, "w", encoding=enc) as f:
        f.write(s)


def _print_file(fname):
    """Print contents of text file."""
    s = read_text_file(fname)
    print(s)


def _print_file_hex(fname):
    """Print contents of file encoded in hexadecimal."""
    b = read_binary_file(fname)
    print(crsysapi.Cnv.tohex(b))


def _dump_file(fname):
    """Print contents of text file with filename header and rulers."""
    s = read_text_file(fname)
    ndash = (24 if len(s) > 24 else len(s))
    print("FILE:", fname)
    print("-" * ndash)
    print(s)
    print("-" * ndash)

#############
# THE TESTS #
#############


def test_error_lookup():
    print("\nLOOKUP SOME ERROR CODES...")
    for n in range(13):
        s = crsysapi.Gen.error_lookup(n)
        if (len(s) > 0):
            print("error_lookup(" + str(n) + ")=" + s)


def test_cnv():
    print("\nTEST CNV FUNCTIONS...")

    # hex --> bytes --> base64
    b = crsysapi.Cnv.fromhex("FE DC BA 98 76 54 32 10")
    print("b=0x" + crsysapi.Cnv.tohex(b))
    print("b64(b)=" + crsysapi.Cnv.tobase64(b))
    assert(crsysapi.Cnv.tobase64(b) == "/ty6mHZUMhA=")

    # base64 --> bytes --> hex --> base64
    b = crsysapi.Cnv.frombase64("/ty6mHZUMhA=")
    print("b=0x" + crsysapi.Cnv.tohex(b))
    assert(crsysapi.Cnv.tohex(b) == "FEDCBA9876543210")
    print("b64(b)=" + crsysapi.Cnv.tobase64(b))
    assert(crsysapi.Cnv.tobase64(b) == "/ty6mHZUMhA=")


def test_cipher():
    print("\nTEST BLOCK CIPHER FUNCTIONS...")

    algstr = "Tdea/CBC/PKCS5"
    print(algstr)
    key = bytearray.fromhex('737C791F25EAD0E04629254352F7DC6291E5CB26917ADA32')
    iv = bytearray.fromhex("B36B6BFB6231084E")
    pt = bytearray.fromhex("5468697320736F6D652073616D706520636F6E74656E742E")

    ct = crsysapi.Cipher.encrypt(pt, key, iv, algstr)
    print(crsysapi.Cnv.tohex(ct))
    b = bytearray.fromhex("5468697320736F6D652073616D706520636F6E74656E742E")
    print(b)
    assert(ct == bytearray.fromhex(
        "D76FD1178FBD02F84231F5C1D2A2F74A4159482964F675248254223DAF9AF8E4"))
    p1 = crsysapi.Cipher.decrypt(ct, key, iv, algstr)
    print(p1)
    assert(p1 == pt)

    print("Use default ECB mode (IV is ignored)")
    ct = crsysapi.Cipher.encrypt(pt, key, alg=crsysapi.Cipher.Alg.TDEA)
    print(crsysapi.Cnv.tohex(ct))
    p1 = crsysapi.Cipher.decrypt(ct, key, alg=crsysapi.Cipher.Alg.TDEA)
    print(p1)
    assert(p1 == pt)

    ct = crsysapi.Cipher.encrypt(pt, key, iv, mode=crsysapi.Cipher.Mode.CBC,
                        alg=crsysapi.Cipher.Alg.TDEA)
    print(crsysapi.Cnv.tohex(ct))
    p1 = crsysapi.Cipher.decrypt(ct, key, iv, mode=crsysapi.Cipher.Mode.CBC,
                        alg=crsysapi.Cipher.Alg.TDEA)
    print(p1)
    assert(p1 == pt)

    algstr = "Aes128/CBC/pkcs5"
    print(algstr)
    key = bytearray.fromhex('0123456789ABCDEFF0E1D2C3B4A59687')
    iv = bytearray.fromhex("FEDCBA9876543210FEDCBA9876543210")
    # In Python 3 we must must pass plaintext as bytes; ASCII strings no longer work
    pt = b"Now is the time for all good men to"
    ct = crsysapi.Cipher.encrypt(pt, key, iv, algstr)
    print(crsysapi.Cnv.tohex(ct))
    assert(ct == bytearray.fromhex(
        "C3153108A8DD340C0BCB1DFE8D25D2320EE0E66BD2BB4A313FB75C5638E9E17753C7E8DF5975A36677355F5C6584228B"))
    # Now decrypt using flags instead of alg string
    p1 = crsysapi.Cipher.decrypt(ct, key, iv, alg=crsysapi.Cipher.Alg.AES128,
                        mode=crsysapi.Cipher.Mode.CBC, pad=crsysapi.Cipher.Pad.PKCS5)
    print("P':", p1)
    assert(p1 == pt)

    algstr = "Aes128/ECB/OneAndZeroes"
    print(algstr)
    ct = crsysapi.Cipher.encrypt(pt, key, algmodepad=algstr)
    print("CT:", crsysapi.Cnv.tohex(ct))
    p1 = crsysapi.Cipher.decrypt(ct, key, algmodepad="Aes128/ECB/NoPad")
    print("Pn:", crsysapi.Cnv.tohex(p1))
    p1 = crsysapi.Cipher.decrypt(ct, key, algmodepad=algstr)
    print("P':", crsysapi.Cnv.tohex(p1))
    print("P':", p1)
    assert(p1 == pt)


def test_cipher_hex():
    print("\nTEST CIPHER FUNCTIONS USING HEX-ENCODED PARAMETERS...")
    algstr = "Tdea/CBC/PKCS5"
    print("ALG:", algstr)
    keyhex = '737C791F25EAD0E04629254352F7DC6291E5CB26917ADA32'
    ivhex = "B36B6BFB6231084E"
    pthex = "5468697320736F6D652073616D706520636F6E74656E742E"
    okhex = "D76FD1178FBD02F84231F5C1D2A2F74A4159482964F675248254223DAF9AF8E4"
    print("KY:", keyhex)
    print("IV:", ivhex)
    print("PT:", pthex)
    cthex = crsysapi.Cipher.encrypt_hex(pthex, keyhex, ivhex, algstr)
    print("CT:", cthex)
    print("OK:", okhex)
    assert cthex == okhex, "crsysapi.Cipher.encrypt_hex failed"
    print("About to decrypt...")
    # Decrypt using flags instead of alg string
    p1hex = crsysapi.Cipher.decrypt_hex(cthex, keyhex, ivhex, alg=crsysapi.Cipher.Alg.TDEA, mode=crsysapi.Cipher.Mode.CBC, pad=crsysapi.Cipher.Pad.PKCS5)
    print("P':", p1hex)
    assert p1hex == pthex

    # Another example, this time with the IV prefixed to the ciphertext
    algstr = "Aes128/CBC/OneAndZeroes"
    keyhex = '0123456789ABCDEFF0E1D2C3B4A59687'
    ivhex = "FEDCBA9876543210FEDCBA9876543210"
    pthex = "4E6F77206973207468652074696D6520666F7220616C6C20676F6F64206D656E20746F"
    # IV||CT
    okhex = "FEDCBA9876543210FEDCBA9876543210C3153108A8DD340C0BCB1DFE8D25D2320EE0E66BD2BB4A313FB75C5638E9E1771D4CDA34FBFB7E74B321F9A2CF4EA61B"
    print("KY:", keyhex)
    print("IV:", ivhex)
    print("PT:", pthex)
    cthex = crsysapi.Cipher.encrypt_hex(pthex, keyhex, ivhex, algstr, opts=crsysapi.Cipher.Opts.PREFIXIV)
    print("CT:", cthex)
    print("OK:", okhex)
    assert cthex == okhex, "crsysapi.Cipher.encrypt_hex failed"
    # Decrypt using flags instead of alg string - this time we don't need the IV argument
    p1hex = crsysapi.Cipher.decrypt_hex(cthex, keyhex, None, alg=crsysapi.Cipher.Alg.AES128, mode=crsysapi.Cipher.Mode.CBC, pad=crsysapi.Cipher.Pad.ONEANDZEROES, opts=crsysapi.Cipher.Opts.PREFIXIV)
    print("P':", p1hex)
    assert(p1hex == pthex)


def test_cipher_file():
    print("\nTEST CIPHER FILE FUNCTIONS...")
    file_pt = "hello.txt"
    write_text_file(file_pt, "hello world\r\n")
    print(file_pt + ":",)
    _print_file_hex(file_pt)
    key = crsysapi.Cnv.fromhex("fedcba9876543210fedcba9876543210")
    iv = crsysapi.Rng.bytestring(crsysapi.Cipher.blockbytes(crsysapi.Cipher.Alg.AES128))
    print("IV:", crsysapi.Cnv.tohex(iv))
    file_ct = "hello.aes128.enc.dat"
    n = crsysapi.Cipher.file_encrypt(file_ct, file_pt, key, iv, "aes128-ctr", opts=crsysapi.Cipher.Opts.PREFIXIV)
    assert(n == 0)
    print(file_ct + ":",)
    _print_file_hex(file_ct)

    file_chk = "hello.aes128.chk.txt"
    n = crsysapi.Cipher.file_decrypt(file_chk, file_ct, key, iv, "aes128-ctr", opts=crsysapi.Cipher.Opts.PREFIXIV)
    assert(n == 0)
    print(file_chk + ":",)
    _print_file_hex(file_chk)
    # check files are equal
    assert(read_binary_file(file_pt) == read_binary_file(file_chk))


def test_cipher_pad():
    print("\nTEST CIPHER PAD....")

    data = crsysapi.Cnv.fromhex('FFFFFFFFFF')
    print("Input data :", crsysapi.Cnv.tohex(data))
    padded = crsysapi.Cipher.pad(data, crsysapi.Cipher.Alg.TDEA)
    print("Padded data:", crsysapi.Cnv.tohex(padded))
    unpadded = crsysapi.Cipher.unpad(padded, crsysapi.Cipher.Alg.TDEA)
    print("Unpadded   :", crsysapi.Cnv.tohex(unpadded))
    padded = crsysapi.Cipher.pad(data, crsysapi.Cipher.Alg.TDEA,
                        crsysapi.Cipher.Pad.ONEANDZEROES)
    print("Padded data:", crsysapi.Cnv.tohex(padded))
    unpadded = crsysapi.Cipher.unpad(padded, crsysapi.Cipher.Alg.TDEA,
                            crsysapi.Cipher.Pad.ONEANDZEROES)
    print("Unpadded   :", crsysapi.Cnv.tohex(unpadded))

    # Pad the empty string
    data = crsysapi.Cnv.fromhex('')
    print("Input data :", crsysapi.Cnv.tohex(data))
    padded = crsysapi.Cipher.pad(data, crsysapi.Cipher.Alg.AES128)
    print("Padded data:", crsysapi.Cnv.tohex(padded))
    unpadded = crsysapi.Cipher.unpad(padded, crsysapi.Cipher.Alg.AES128)
    print("Unpadded   :", crsysapi.Cnv.tohex(unpadded))
    # Pass data as hex strings
    datahex = 'aaaaaa'
    print("Input data :", datahex)
    paddedhex = crsysapi.Cipher.pad_hex(datahex, crsysapi.Cipher.Alg.TDEA)
    print("Padded data:", paddedhex)
    unpaddedhex = crsysapi.Cipher.unpad_hex(paddedhex, crsysapi.Cipher.Alg.TDEA)
    print("Unpadded   :", unpaddedhex)
    paddedhex = crsysapi.Cipher.pad_hex(
        datahex, crsysapi.Cipher.Alg.TDEA, crsysapi.Cipher.Pad.ONEANDZEROES)
    print("Padded data:", paddedhex)
    unpaddedhex = crsysapi.Cipher.unpad_hex(
        paddedhex, crsysapi.Cipher.Alg.TDEA, crsysapi.Cipher.Pad.ONEANDZEROES)
    print("Unpadded   :", unpaddedhex)


def test_cipher_block():
    print("\nTEST CIPHER FUNCTIONS WITH EXACT BLOCK LENGTHS...")
    key = crsysapi.Cnv.fromhex("0123456789ABCDEFF0E1D2C3B4A59687")
    iv = crsysapi.Cnv.fromhex("FEDCBA9876543210FEDCBA9876543210")
    print("KY:", crsysapi.Cnv.tohex(key))
    print("IV:", crsysapi.Cnv.tohex(iv))
    # In Python 3 plaintext must be bytes, not ASCII string
    pt = b"Now is the time for all good men"
    print("PT:", pt)
    print("PT:", crsysapi.Cnv.tohex(pt))
    okhex = "C3153108A8DD340C0BCB1DFE8D25D2320EE0E66BD2BB4A313FB75C5638E9E177"
    ct = crsysapi.Cipher.encrypt_block(
        pt, key, iv, alg=crsysapi.Cipher.Alg.AES128, mode=crsysapi.Cipher.Mode.CBC)
    print("CT:", crsysapi.Cnv.tohex(ct))
    print("OK:", okhex)
    assert(okhex.upper() == crsysapi.Cnv.tohex(ct))
    p1 = crsysapi.Cipher.decrypt_block(
        ct, key, iv, alg=crsysapi.Cipher.Alg.AES128, mode=crsysapi.Cipher.Mode.CBC)
    print("P1:", crsysapi.Cnv.tohex(p1))
    print("P1:", p1)

    # Using defaults (TDEA/ECB)
    key = crsysapi.Rng.bytestring(crsysapi.Cipher.keybytes(crsysapi.Cipher.Alg.TDEA))
    print("KY:", crsysapi.Cnv.tohex(key))
    ct = crsysapi.Cipher.encrypt_block(pt, key, iv)
    print("CT:", crsysapi.Cnv.tohex(ct))
    p1 = crsysapi.Cipher.decrypt_block(ct, key, iv)
    print("P1:", crsysapi.Cnv.tohex(p1))
    print("P1:", p1)


def test_blowfish():
    print("\nTEST BLOWFISH CIPHER...")
    key = crsysapi.Cnv.fromhex("0123456789ABCDEFF0E1D2C3B4A59687")
    iv = crsysapi.Cnv.fromhex("FEDCBA9876543210")
    print("KY:", crsysapi.Cnv.tohex(key))
    print("IV:", crsysapi.Cnv.tohex(iv))
    pt = crsysapi.Cnv.fromhex("37363534333231204E6F77206973207468652074696D6520666F722000000000")
    print("PT:", crsysapi.Cnv.tohex(pt))
    okhex = "6B77B4D63006DEE605B156E27403979358DEB9E7154616D959F1652BD5FF92CC"
    ct = crsysapi.Blowfish.encrypt_block(pt, key, "CBC", iv)
    print("CT:", crsysapi.Cnv.tohex(ct))
    print("OK:", okhex)
    assert(okhex.upper() == crsysapi.Cnv.tohex(ct))
    p1 = crsysapi.Blowfish.decrypt_block(ct, key, "CBC", iv)
    print("P1:", crsysapi.Cnv.tohex(p1))
    print("P1:", bytes(p1))
    assert(p1 == pt)

    # Using default ECB mode
    key = crsysapi.Cnv.fromhex("FEDCBA9876543210")
    print("KY:", crsysapi.Cnv.tohex(key))
    pt = crsysapi.Cnv.fromhex("0123456789ABCDEF0123456789ABCDEF")
    print("PT:", crsysapi.Cnv.tohex(pt))
    okhex = "0ACEAB0FC6A0A28D0ACEAB0FC6A0A28D"
    ct = crsysapi.Blowfish.encrypt_block(pt, key)
    print("CT:", crsysapi.Cnv.tohex(ct))
    print("OK:", okhex)
    assert(okhex.upper() == crsysapi.Cnv.tohex(ct))
    p1 = crsysapi.Blowfish.decrypt_block(ct, key)
    print("P1:", crsysapi.Cnv.tohex(p1))
    assert(p1 == pt)


def test_aead():
    print("\nTEST AEAD ENCRYPTION....")

    # GCM Test Case #03 (AES-128)
    key = crsysapi.Cnv.fromhex("feffe9928665731c6d6a8f9467308308")
    iv = crsysapi.Cnv.fromhex("cafebabefacedbaddecaf888")
    pt = crsysapi.Cnv.fromhex("d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a721c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b391aafd255")
    okhex = "42831ec2217774244b7221b784d0d49ce3aa212f2c02a4e035c17e2329aca12e21d514b25466931c7d8f6a5aac84aa051ba30b396a0aac973d58e091473f59854d5c2af327cd64a62cf35abd2ba6fab4"
    print("KY =", crsysapi.Cnv.tohex(key))
    print("IV =", crsysapi.Cnv.tohex(iv))
    print("PT =", crsysapi.Cnv.tohex(pt))
    # Do the business
    ct = crsysapi.Aead.encrypt_with_tag(pt, key, iv, crsysapi.Aead.AeadAlg.AES_128_GCM)
    print("CT =", crsysapi.Cnv.tohex(ct))
    print("OK =", okhex)
    assert (okhex.lower() == crsysapi.Cnv.tohex(ct).lower())

    # Decrypt, passing IV as an argument
    dt = crsysapi.Aead.decrypt_with_tag(ct, key, iv, crsysapi.Aead.AeadAlg.AES_128_GCM)
    print("DT =", crsysapi.Cnv.tohex(dt))
    assert (crsysapi.Cnv.tohex(pt) == crsysapi.Cnv.tohex(dt))

    print("Repeat but prepend IV to output..")
    ct = crsysapi.Aead.encrypt_with_tag(pt, key, iv, crsysapi.Aead.AeadAlg.AES_128_GCM, opts=crsysapi.Aead.Opts.PREFIXIV)
    print("IV|CT =", crsysapi.Cnv.tohex(ct))
    # Decrypt, IV is prepended to ciphertext
    dt = crsysapi.Aead.decrypt_with_tag(ct, key, None, crsysapi.Aead.AeadAlg.AES_128_GCM, opts=crsysapi.Aead.Opts.PREFIXIV)
    print("DT =", crsysapi.Cnv.tohex(dt))
    assert (crsysapi.Cnv.tohex(pt) == crsysapi.Cnv.tohex(dt))

    print("RFC7739 ChaCha20_Poly1305 Sunscreen test with AAD")
    key = crsysapi.Cnv.fromhex("808182838485868788898A8B8C8D8E8F909192939495969798999A9B9C9D9E9F")
    iv = crsysapi.Cnv.fromhex("070000004041424344454647")
    aad = crsysapi.Cnv.fromhex("50515253C0C1C2C3C4C5C6C7")
    pt = crsysapi.Cnv.fromhex("4C616469657320616E642047656E746C656D656E206F662074686520636C617373206F66202739393A204966204920636F756C64206F6666657220796F75206F6E6C79206F6E652074697020666F7220746865206675747572652C2073756E73637265656E20776F756C642062652069742E")
    okhex = "d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d63dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b3692ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc3ff4def08e4b7a9de576d26586cec64b61161ae10b594f09e26a7e902ecbd0600691"
    print("KY =", crsysapi.Cnv.tohex(key))
    print("IV =", crsysapi.Cnv.tohex(iv))
    print("AD =", crsysapi.Cnv.tohex(aad))
    print("PT =", crsysapi.Cnv.tohex(pt))
    # Do the business
    ct = crsysapi.Aead.encrypt_with_tag(pt, key, iv, crsysapi.Aead.AeadAlg.CHACHA20_POLY1305, aad=aad)
    print("CT =", crsysapi.Cnv.tohex(ct))
    print("OK =", okhex)
    assert (okhex.lower() == crsysapi.Cnv.tohex(ct).lower())
    dt = crsysapi.Aead.decrypt_with_tag(ct, key, iv, crsysapi.Aead.AeadAlg.CHACHA20_POLY1305, aad=aad)
    print("DT =", crsysapi.Cnv.tohex(dt))
    print(f"DT ='{dt}'")
    assert (crsysapi.Cnv.tohex(pt) == crsysapi.Cnv.tohex(dt))


def test_crc():
    print("\nTEST CRC FUNCTIONS...")

    crc = crsysapi.Crc.bytes(b"123456789")
    print(f"crc={crc}=0x{crc:08x}")
    crc = 0
    fname = "1-9.txt"
    write_text_file(fname, "123456789")
    crc = crsysapi.Crc.file(fname)
    print(f"crc={crc}=0x{crc:08x}")


def test_rng():
    print("\nTESTING RANDOM NUMBER GENERATOR...")

    # Initialize from seed file. File is created if it does not exist.
    # Optional but recommended for extra security
    seedfile = 'myseedfile.dat'
    n = crsysapi.Rng.initialize(seedfile)
    assert(0 == n)
    print('crsysapi.Rng.initialize() returns', n, ". Contents of seed file:")
    sd = read_binary_file(seedfile)
    print(crsysapi.Cnv.tohex(sd))
    assert(len(sd) == crsysapi.Rng.SEED_BYTES)

    print("5 random byte arrays")
    for i in range(5):
        b = crsysapi.Rng.bytestring((i + 2) * 2)
        print(crsysapi.Cnv.tohex(b).lower())

    print("5 random numbers in the range [-1 million, +1 million]")
    for i in range(5):
        r = crsysapi.Rng.number(-1000000, 1000000)
        print(r)
        assert(-1000000 <= r <= 1000000)

    print("5 random octet values")
    s = ""  # fudge to do in one line
    for i in range(5):
        r = crsysapi.Rng.octet()
        assert(0 <= r <= 255)
        s += str(r) + " "
    print(s)

    # Update seedfile
    n = crsysapi.Rng.update_seedfile(seedfile)
    assert(0 == n)
    print('crsysapi.Rng.update_seedfile() returns', n, ". Contents of seed file:")
    sd = read_binary_file(seedfile)
    print(crsysapi.Cnv.tohex(sd))
    assert(len(sd) == crsysapi.Rng.SEED_BYTES)


def test_hash():
    print("\nTESTING Hash...")
    # write a file containing the 3 bytes 'abc'
    write_text_file('abc.txt', 'abc')
    _dump_file('abc.txt')
    abc_hex = crsysapi.Cnv.tohex(b'abc')
    print("'abc' in hex:", abc_hex)

    # Use default SHA-1 algorithm
    print("Using default SHA-1...")
    b = crsysapi.Hash.data(b'abc')
    print("crsysapi.Hash.data('abc'):", crsysapi.Cnv.tohex(b))
    h = crsysapi.Hash.hex_from_data(b'abc')
    print("crsysapi.Hash.hex_from_data('abc'):", h)
    h = crsysapi.Hash.hex_from_data(bytearray.fromhex('616263'))
    print("crsysapi.Hash.hex_from_data('abc'):", h)
    h = crsysapi.Hash.hex_from_hex(abc_hex)
    print("crsysapi.Hash.hex_from_hex(abc_hex):", h)
    b = crsysapi.Hash.file('abc.txt')
    print("crsysapi.Hash.file('abc.txt'):", crsysapi.Cnv.tohex(b))
    h = crsysapi.Hash.hex_from_file('abc.txt')
    print("crsysapi.Hash.hex_from_file('abc.txt'):", h)

    print("Using SHA-256...")
    b = crsysapi.Hash.data(b'abc', crsysapi.Hash.Alg.SHA256)
    print("crsysapi.Hash.data('abc'):", crsysapi.Cnv.tohex(b))
    h = crsysapi.Hash.hex_from_hex(abc_hex, crsysapi.Hash.Alg.SHA256)
    print("crsysapi.Hash.hex_from_hex(abc_hex):", h)
    b = crsysapi.Hash.file('abc.txt', crsysapi.Hash.Alg.SHA256)
    print("crsysapi.Hash.file('abc.txt'):", crsysapi.Cnv.tohex(b))
    h = crsysapi.Hash.hex_from_file('abc.txt', crsysapi.Hash.Alg.SHA256)
    print("crsysapi.Hash.hex_from_file('abc.txt'):", h)

    # write a file containing the 3 bytes 'abc'
    write_text_file('abc.txt', 'abc')
    _dump_file('abc.txt')
    abc_hex = crsysapi.Cnv.tohex(b'abc')
    print("'abc' in hex:", abc_hex)

    b = crsysapi.Hash.data(b'abc', crsysapi.Hash.Alg.SHA3_224)
    print("crsysapi.Hash.data('abc'):", crsysapi.Cnv.tohex(b))
    assert(b == crsysapi.Cnv.fromhex('e642824c3f8cf24ad09234ee7d3c766fc9a3a5168d0c94ad73b46fdf'))
    h = crsysapi.Hash.hex_from_hex(abc_hex, crsysapi.Hash.Alg.SHA3_256)
    print("crsysapi.Hash.hex_from_hex(abc_hex):", h)
    assert(crsysapi.Cnv.fromhex(h) == crsysapi.Cnv.fromhex('3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532'))
    b = crsysapi.Hash.file('abc.txt', crsysapi.Hash.Alg.SHA3_384)
    print("crsysapi.Hash.file('abc.txt'):", crsysapi.Cnv.tohex(b))
    assert(b == crsysapi.Cnv.fromhex('ec01498288516fc926459f58e2c6ad8df9b473cb0fc08c2596da7cf0e49be4b298d88cea927ac7f539f1edf228376d25'))
    h = crsysapi.Hash.hex_from_file('abc.txt', crsysapi.Hash.Alg.SHA3_512)
    print("crsysapi.Hash.hex_from_file('abc.txt'):", h)
    assert(crsysapi.Cnv.fromhex(h) == crsysapi.Cnv.fromhex('b751850b1a57168a5693cd924b6b096e08f621827444f70d884f5d0240d2712e10e116e9192af3c91a7ec57647e3934057340b4cf408d5a56592f8274eec53f0'))


# def test_hash_length():
#     print("\nTEST HASH LENGTH...")
#     print("Hash.length(SHA-1) =", crsysapi.Hash.length(crsysapi.Hash.Alg.SHA1))
#     print("Hash.length(SHA-256) =", crsysapi.Hash.length(crsysapi.Hash.Alg.SHA256))
#     print("Hash.length(SHA-512) =", crsysapi.Hash.length(crsysapi.Hash.Alg.SHA512))
#     print("Hash.length(RMD160) =", crsysapi.Hash.length(crsysapi.Hash.Alg.RMD160))


def test_mac():
    print("\nTESTING MAC...")
    print("Test case 4 from RFC 2202 and RFC 4231")
    key = crsysapi.Cnv.fromhex('0102030405060708090a0b0c0d0e0f10111213141516171819')
    print("key: ", crsysapi.Cnv.tohex(key))
    # data = 0xcd repeated 50 times
    data = bytearray([0xcd] * 50)
    print("data:", crsysapi.Cnv.tohex(data))

    b = crsysapi.Mac.data(data, key)
    print("HMAC-SHA-1:  ", crsysapi.Cnv.tohex(b))
    assert(b == crsysapi.Cnv.fromhex('4c9007f4026250c6bc8414f9bf50c86c2d7235da'))

    b = crsysapi.Mac.data(data, key, crsysapi.Mac.Alg.HMAC_MD5)
    print("HMAC-MD5:    ", crsysapi.Cnv.tohex(b))
    assert(b == crsysapi.Cnv.fromhex('697eaf0aca3a3aea3a75164746ffaa79'))

    b = crsysapi.Mac.data(data, key, crsysapi.Mac.Alg.HMAC_SHA256)
    print("HMAC-SHA-256:", crsysapi.Cnv.tohex(b))
    assert(b == crsysapi.Cnv.fromhex(
        '82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b'))

    h = crsysapi.Mac.hex_from_data(data, key, crsysapi.Mac.Alg.HMAC_SHA256)
    print("HMAC-SHA-256:", h)
    assert(h == '82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b')

    b = crsysapi.Mac.data(data, key, crsysapi.Mac.Alg.HMAC_SHA512)
    print("HMAC-SHA-512:", crsysapi.Cnv.tohex(b))
    assert(b == crsysapi.Cnv.fromhex(
        'b0ba465637458c6990e5a8c5f61d4af7 e576d97ff94b872de76f8050361ee3db a91ca5c11aa25eb4d679275cc5788063 a5f19741120c4f2de2adebeb10a298dd'))

    print("Test case 7 from RFC 4231")
    key = bytearray([0xaa] * 131)
    print("key: ", crsysapi.Cnv.tohex(key).lower())
    data = b"This is a test using a larger than block-size key and a larger than block-size data. The key needs to be hashed before being used by the HMAC algorithm."
    print("data:", data)
    b = crsysapi.Mac.data(data, key, crsysapi.Mac.Alg.HMAC_SHA224)
    print("HMAC-SHA-224:", crsysapi.Cnv.tohex(b))
    assert(b == crsysapi.Cnv.fromhex(
        '3a854166ac5d9f023f54d517d0b39dbd946770db9c2b95c9f6f565d1'))

    # HMAC hex <-- hex
    print("Test case 1 from RFC 2202 and RFC 4231")
    keyhex = "0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b"  # (20 bytes)
    datahex = "4869205468657265"    # ("Hi There")
    print("key: ", keyhex)
    print("data:", datahex)
    h = crsysapi.Mac.hex_from_hex(datahex, keyhex)
    print("HMAC-SHA-1:", h)
    assert(h == "b617318655057264e28bc0b6fb378c8ef146be00")
    h = crsysapi.Mac.hex_from_hex(datahex, keyhex, crsysapi.Mac.Alg.HMAC_SHA256)
    print("HMAC-SHA-256:", h)
    assert(h == "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7")

    print("\nTESTING Mac(SHA-3)...")
    print("NIST HMAC_SHA3-256.pdf Sample #1")
    key = crsysapi.Cnv.fromhex('000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F')
    print("key: ", crsysapi.Cnv.tohex(key))
    data = b'Sample message for keylen<blocklen'
    print("data:", data.decode())
    b = crsysapi.Mac.data(data, key, crsysapi.Mac.Alg.HMAC_SHA3_256)
    print("HMAC-SHA-3-256:", crsysapi.Cnv.tohex(b))
    assert(b == crsysapi.Cnv.fromhex('4fe8e202c4f058e8dddc23d8c34e467343e23555e24fc2f025d598f558f67205'))

    print("NIST HMAC_SHA3-512.pdf Sample #3")
    key = crsysapi.Cnv.fromhex("""000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F
202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F
404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F
606162636465666768696A6B6C6D6E6F707172737475767778797A7B7C7D7E7F
8081828384858687""")
    print("key: ", crsysapi.Cnv.tohex(key))
    data = b'Sample message for keylen>blocklen'
    print("data:", data.decode())
    b = crsysapi.Mac.data(data, key, crsysapi.Mac.Alg.HMAC_SHA3_512)
    print("HMAC-SHA-3-512:", crsysapi.Cnv.tohex(b))
    assert(b == crsysapi.Cnv.fromhex('5f464f5e5b7848e3885e49b2c385f0694985d0e38966242dc4a5fe3fea4b37d46b65ceced5dcf59438dd840bab22269f0ba7febdb9fcf74602a35666b2a32915'))

    print("CMAC tests from SP800-38B...")
    # CMAC-AES-128 on the empty string
    keyhex = "2b7e151628aed2a6abf7158809cf4f3c"
    datahex = ""
    h = crsysapi.Mac.hex_from_hex(datahex, keyhex, crsysapi.Mac.Alg.CMAC_AES128)
    print("CMAC-AES-128(K128, '')=", h)
    assert(h == "bb1d6929e95937287fa37d129b756746")
    # CMAC_AES-256 on Example 12: Mlen = 512
    keyhex = "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4"
    datahex = "6bc1bee22e409f96e93d7e117393172a" + \
        "ae2d8a571e03ac9c9eb76fac45af8e51" + \
        "30c81c46a35ce411e5fbc1191a0a52ef" + \
        "f69f2445df4f9b17ad2b417be66c3710"
    h = crsysapi.Mac.hex_from_hex(datahex, keyhex, crsysapi.Mac.Alg.CMAC_AES256)
    print("CMAC-AES-256(K256, M512)=", h)
    assert(h == "e1992190549f6ed5696a2c056c315410")

    # POLY1305 AUTHENTICATION ALGORITHM
    # Ref: Test vector from `RFC 7539` section 2.5.2
    print("Poly1305 tests...")

    keyhex = "85d6be7857556d337f4452fe42d506a80103808afb0db2fd4abff6af4149f51b"
    datahex = crsysapi.Cnv.tohex(b"Cryptographic Forum Research Group")
    print(f"key={keyhex}")
    print(f"msg='{crsysapi.Cnv.fromhex(datahex).decode()}'")
    h = crsysapi.Mac.hex_from_hex(datahex, keyhex, crsysapi.Mac.Alg.MAC_POLY1305)
    print(f"POLY1305={h}")
    assert(h == "a8061dc1305136c6c22b8baf0c0127a9")

    # KMAC
    # Ref: `KMAC_samples.pdf` "Secure Hashing - KMAC-Samples" 2017-02-27
    print("KMAC tests...")
    keyhex = "404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F"
    datahex = "00010203"
    h = crsysapi.Mac.hex_from_hex(datahex, keyhex, crsysapi.Mac.Alg.KMAC_128)
    print("KMAC128=", h)
    assert(h == "e5780b0d3ea6f7d3a429c5706aa43a00fadbd7d49628839e3187243f456ee14e")

    keyhex = "404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F"
    datahex = "000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F606162636465666768696A6B6C6D6E6F707172737475767778797A7B7C7D7E7F808182838485868788898A8B8C8D8E8F909192939495969798999A9B9C9D9E9FA0A1A2A3A4A5A6A7A8A9AAABACADAEAFB0B1B2B3B4B5B6B7B8B9BABBBCBDBEBFC0C1C2C3C4C5C6C7"
    h = crsysapi.Mac.hex_from_hex(datahex, keyhex, crsysapi.Mac.Alg.KMAC_256)
    print("KMAC256=", h)
    assert(h == "75358cf39e41494e949707927cee0af20a3ff553904c86b08f21cc414bcfd691589d27cf5e15369cbbff8b9a4c2eb17800855d0235ff635da82533ec6b759b69")


def test_prf():
    print("\nTEST PRF FUNCTIONS...")
    # `KMAC_samples.pdf` "Secure Hashing - KMAC-Samples" 2017-02-27
    # Sample #1
    # "standard" KMAC output length KMAC128 => 256 bits, no custom string
    nbytes = 256 // 8
    msg = crsysapi.Cnv.fromhex("00010203")
    key = crsysapi.Cnv.fromhex("404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F")
    okhex = "E5780B0D3EA6F7D3A429C5706AA43A00FADBD7D49628839E3187243F456EE14E"
    kmac = crsysapi.Prf.bytes(nbytes, msg, key, crsysapi.Prf.Alg.KMAC128)
    print("KMAC=", crsysapi.Cnv.tohex(kmac))
    print("OK  =", okhex)
    assert crsysapi.Cnv.tohex(kmac).upper() == okhex, "KMAC failed"

    # "standard" KMAC output length KMAC256 => 512 bits, no custom string
    # Sample #6
    nbytes = 512 // 8
    # Length of data is 1600 bits
    msg = crsysapi.Cnv.fromhex("""000102030405060708090A0B0C0D0E0F
101112131415161718191A1B1C1D1E1F
202122232425262728292A2B2C2D2E2F
303132333435363738393A3B3C3D3E3F
404142434445464748494A4B4C4D4E4F
505152535455565758595A5B5C5D5E5F
606162636465666768696A6B6C6D6E6F
707172737475767778797A7B7C7D7E7F
808182838485868788898A8B8C8D8E8F
909192939495969798999A9B9C9D9E9F
A0A1A2A3A4A5A6A7A8A9AAABACADAEAF
B0B1B2B3B4B5B6B7B8B9BABBBCBDBEBF
C0C1C2C3C4C5C6C7""")
    key = crsysapi.Cnv.fromhex("404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F")
    okhex = "75358CF39E41494E949707927CEE0AF20A3FF553904C86B08F21CC414BCFD691589D27CF5E15369CBBFF8B9A4C2EB17800855D0235FF635DA82533EC6B759B69"
    kmac = crsysapi.Prf.bytes(nbytes, msg, key, crsysapi.Prf.Alg.KMAC256)
    print("KMAC=", crsysapi.Cnv.tohex(kmac))
    print("OK  =", okhex)
    assert crsysapi.Cnv.tohex(kmac).upper() == okhex, "KMAC failed"

    # Sample #2
    # Same as Sample #1 except with custom string
    nbytes = 256 // 8
    msg = crsysapi.Cnv.fromhex("00010203")
    key = crsysapi.Cnv.fromhex("404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F")
    custom = "My Tagged Application"
    okhex = "3B1FBA963CD8B0B59E8C1A6D71888B7143651AF8BA0A7070C0979E2811324AA5"
    kmac = crsysapi.Prf.bytes(nbytes, msg, key, crsysapi.Prf.Alg.KMAC128, custom)
    print("KMAC=", crsysapi.Cnv.tohex(kmac))
    print("OK  =", okhex)
    assert crsysapi.Cnv.tohex(kmac).upper() == okhex, "KMAC failed"

    # Request a lot of output (> single KECCAK block)
    nbytes = 1600 // 8
    msg = crsysapi.Cnv.fromhex("00010203")
    key = crsysapi.Cnv.fromhex("404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F")
    okhex = """38158A1CAE4E1A25D85F2031246ADE69
7B3292FEF88B0923A59A02D1D53B7046
53EE7242662A10796BA20779D300D52D
7432018741233D587252D31DC48BDB82
33285D4A4ACD65848509B051A448D873
649228B6626E5EF817C7AF2DEDC91F12
0F8CA535A1EE301FAE8186FDEDE5A761
81A472A32CFAD1DDD1391E162F124D4A
7572AD8A20076601BCF81E4B0391F3E9
5AEFFA708C33C1217C96BE6A4F02FBBC
2D3B3B6FFAEB5BFD3BE4A2E02B75993F
CC04DA6FAC4BFCB2A9F05792A1A5CC80
CA34186243EFDB31"""
    okhex = okhex.replace("\n", "")
    kmac = crsysapi.Prf.bytes(nbytes, msg, key, crsysapi.Prf.Alg.KMAC128)
    print("KMAC=", crsysapi.Cnv.tohex(kmac))
    print("OK  =", okhex)
    assert crsysapi.Cnv.tohex(kmac).upper() == okhex, "KMAC failed"


def test_xof():
    print("\nTEST XOF FUNCTIONS...")
    # Ref: "SHA-3 XOF Test Vectors for Byte-Oriented Output"
    # File `SHAKE256VariableOut.rsp` COUNT = 1244
    nbytes = 2000 // 8
    msg = crsysapi.Cnv.fromhex("6ae23f058f0f2264a18cd609acc26dd4dbc00f5c3ee9e13ecaea2bb5a2f0bb6b")
    okhex = """b9b92544fb25cfe4ec6fe437d8da2bbe
00f7bdaface3de97b8775a44d753c3ad
ca3f7c6f183cc8647e229070439aa953
9ae1f8f13470c9d3527fffdeef6c94f9
f0520ff0c1ba8b16e16014e1af43ac6d
94cb7929188cce9d7b02f81a2746f52b
a16988e5f6d93298d778dfe05ea0ef25
6ae3728643ce3e29c794a0370e9ca6a8
bf3e7a41e86770676ac106f7ae79e670
27ce7b7b38efe27d253a52b5cb54d6eb
4367a87736ed48cb45ef27f42683da14
0ed3295dfc575d3ea38cfc2a3697cc92
864305407369b4abac054e497378dd9f
d0c4b352ea3185ce1178b3dc1599df69
db29259d4735320c8e7d33e8226620c9
a1d22761f1d35bdff79a"""
    okhex = okhex.replace("\n", "")
    xof = crsysapi.Xof.bytes(nbytes, msg, crsysapi.Xof.Alg.SHAKE256)
    print("OUT=", crsysapi.Cnv.tohex(xof))
    print("OK =", okhex)
    assert(crsysapi.Cnv.tohex(xof).lower() == okhex)

# TODO: add MGF-1


def test_compress():
    print("\nTEST COMPRESSION....")
    print("Using zlib...")
    message = b"hello, hello, hello. This is a 'hello world' message for the world, repeat, for the world."
    print("MSG:", message)
    comprdata = crsysapi.Compr.compress(message)
    print("Compressed = (0x)" + crsysapi.Cnv.tohex(comprdata))
    print(f"Compressed {len(message)} bytes to {len(comprdata)}")
    # Now uncompresss (inflate)
    uncomprdata = crsysapi.Compr.uncompress(comprdata)
    print("Uncompressed = '" + str(uncomprdata) + "'")
    assert (uncomprdata == message)
    print("Using Zstandard...")
    comprdata = crsysapi.Compr.compress(message, crsysapi.Compr.Alg.ZSTD)
    print("Compressed = (0x)" + crsysapi.Cnv.tohex(comprdata))
    print(f"Compressed {len(message)} bytes to {len(comprdata)}")
    # Now uncompresss (inflate)
    uncomprdata = crsysapi.Compr.uncompress(comprdata, crsysapi.Compr.Alg.ZSTD)
    print("Uncompressed = '" + str(uncomprdata) + "'")
    assert (uncomprdata == message)


def test_pbe():
    print("\nTESTING PASSWORD-BASED ENCRYPTION (PBE)...")
    password = 'password'
    salt = crsysapi.Cnv.fromhex('78 57 8E 5A 5D 63 CB 06')
    count = 2048
    print("password = '" + password + "'")
    print("salt = 0x" + crsysapi.Cnv.tohex(salt))
    print("count =", count)

    dklen = 24
    print("dklen =", dklen)
    dk = crsysapi.Pbe.kdf2(dklen, password, salt, count)
    print("dk =", crsysapi.Cnv.tohex(dk))
    assert crsysapi.Cnv.tohex(dk) == "BFDE6BE94DF7E11DD409BCE20A0255EC327CB936FFE93643"

    # Same params but derive a longer key (CAUTION: never use the same salt in
    # practice)
    dklen = 64
    print("dklen =", dklen)
    dk = crsysapi.Pbe.kdf2(dklen, password, salt, count)
    print("dk =", crsysapi.Cnv.tohex(dk))
    assert crsysapi.Cnv.tohex(dk) == \
        "BFDE6BE94DF7E11DD409BCE20A0255EC327CB936FFE93643C4B150DEF77511224479994567F2E9B4E3BD0DF7AEDA3022B1F26051D81505C794F8940C04DF1144"

    # Use different HMAC algorithms
    dklen = 24
    dk = crsysapi.Pbe.kdf2(dklen, password, salt, count, prfalg=crsysapi.Pbe.PrfAlg.HMAC_SHA1)
    print("dk(HMAC-SHA-1)   =", crsysapi.Cnv.tohex(dk))
    assert crsysapi.Cnv.tohex(dk) == "BFDE6BE94DF7E11DD409BCE20A0255EC327CB936FFE93643"
    dk = crsysapi.Pbe.kdf2(dklen, password, salt, count, prfalg=crsysapi.Pbe.PrfAlg.HMAC_SHA256)
    print("dk(HMAC-SHA-256) =", crsysapi.Cnv.tohex(dk))
    assert crsysapi.Cnv.tohex(dk) == "97B5A91D35AF542324881315C4F849E327C4707D1BC9D322"
    dk = crsysapi.Pbe.kdf2(dklen, password, salt, count, prfalg=crsysapi.Pbe.PrfAlg.HMAC_SHA224)
    print("dk(HMAC-SHA-224) =", crsysapi.Cnv.tohex(dk))
    assert crsysapi.Cnv.tohex(dk) == "10CFFEDFB13503519969151E466F587028E0720B387F9AEF"

    # Use SCRYPT examples from RFC7914
    dk = crsysapi.Pbe.scrypt(64, b'password', b'NaCl', 1024, 8, 16)
    print("dk(SCRYPT)=", crsysapi.Cnv.tohex(dk))
    assert crsysapi.Cnv.tohex(dk)== 'FDBABE1C9D3472007856E7190D01E9FE7C6AD7CBC8237830E77376634B373162' \
            + '2EAF30D92E22A3886FF109279D9830DAC727AFB94A83EE6D8360CBDFA2CC0640'
    # Pass empty string for both password and salt with (N=16, r=1, p=1)
    dk = crsysapi.Pbe.scrypt(64, b'', b'', 16, 1, 1)
    print("dk(SCRYPT)=", crsysapi.Cnv.tohex(dk))
    assert crsysapi.Cnv.tohex(dk)== '77D6576238657B203B19CA42C18A0497F16B4844E3074AE8DFDFFA3FEDE21442' \
            + 'FCD0069DED0948F8326A753A0FC81F17E8D3E0FB2E0D3628CF35E20C38D18906'


def test_wipe():
    print("\nTESTING Wipe...")

    print("Note that Wipe.data() just zeroizes the data, it does not change the length")

    b = crsysapi.Cnv.fromhex('3a854166ac5d9f023f54d517d0b39dbd946770db9c2b95c9f6f565d1')
    print("BEFORE b=", crsysapi.Cnv.tohex(b))
    crsysapi.Wipe.data(b)
    print("AFTER Wipe.data() b=", crsysapi.Cnv.tohex(b))
    print("AFTER Wipe.data()", str(b))
    print([c for c in b])
    assert all([c == 0 for c in b])

    # works with a bytes type but not with an immutable string type
    s = b"a string"
    print("BEFORE s='" + str(s) + "'")
    print([c for c in s])
    crsysapi.Wipe.data(s)
    print("AFTER Wipe.data()", str(s))
    print([c for c in s])
    assert all([c == 0 for c in s])

    # write a file containing some text
    fname = 'tobedeleted.txt'
    write_text_file(fname, 'Some secret text in this file.')
    _dump_file(fname)
    assert(os.path.isfile(fname))
    crsysapi.Wipe.file(fname)
    print("After Wipe.file(), isfile() returns",  os.path.isfile(fname))
    assert(not os.path.isfile(fname))


def test_cipherstream():
    print("\nTESTING CipherStream...")
    print("Using ARCFOUR...")
    key = crsysapi.Cnv.fromhex("0123456789abcdef")
    pt = crsysapi.Cnv.fromhex("0123456789abcdef")
    okhex = "75b7878099e0c596"
    print("KY =", crsysapi.Cnv.tohex(key))
    print("PT =", crsysapi.Cnv.tohex(pt))
    # Do the business
    ct = crsysapi.CipherStream.bytes(pt, key, None, crsysapi.CipherStream.Alg.ARCFOUR)
    print("CT =", crsysapi.Cnv.tohex(ct))
    print("OK =", okhex)
    assert (okhex.lower() == crsysapi.Cnv.tohex(ct).lower())
    # Repeat to decrypt
    dt = crsysapi.CipherStream.bytes(ct, key, None, crsysapi.CipherStream.Alg.ARCFOUR)
    print("DT =", crsysapi.Cnv.tohex(dt))
    assert (pt == dt)

    print("Using Salsa20...")
    # Set 6, vector#  0:
    key = crsysapi.Cnv.fromhex("0053A6F94C9FF24598EB3E91E4378ADD")
    iv = crsysapi.Cnv.fromhex("0D74DB42A91077DE")
    pt = b'\x00' * 64
    okhex = "05E1E7BEB697D999656BF37C1B978806735D0B903A6007BD329927EFBE1B0E2A8137C1AE291493AA83A821755BEE0B06CD14855A67E46703EBF8F3114B584CBA"
    print("KY =", crsysapi.Cnv.tohex(key))
    print("IV =", crsysapi.Cnv.tohex(iv))
    print("PT =", crsysapi.Cnv.tohex(pt))
    # Do the business
    ct = crsysapi.CipherStream.bytes(pt, key, iv, crsysapi.CipherStream.Alg.SALSA20)
    print("CT =", crsysapi.Cnv.tohex(ct))
    print("OK =", okhex)
    assert (okhex.lower() == crsysapi.Cnv.tohex(ct).lower())
    # Repeat to decrypt
    dt = crsysapi.CipherStream.bytes(ct, key, iv, crsysapi.CipherStream.Alg.SALSA20)
    print("DT =", crsysapi.Cnv.tohex(dt))
    assert (pt == dt)

    print("Using ChaCha20 with counter=1...")
    key = crsysapi.Cnv.fromhex("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")
    iv = crsysapi.Cnv.fromhex("000000000000004a00000000")
    pt = b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, sunscreen would be it."
    okhex = "6E2E359A2568F98041BA0728DD0D6981E97E7AEC1D4360C20A27AFCCFD9FAE0BF91B65C5524733AB8F593DABCD62B3571639D624E65152AB8F530C359F0861D807CA0DBF500D6A6156A38E088A22B65E52BC514D16CCF806818CE91AB77937365AF90BBF74A35BE6B40B8EEDF2785E42874D"
    print("KY =", crsysapi.Cnv.tohex(key))
    print("IV =", crsysapi.Cnv.tohex(iv))
    print("PT =", crsysapi.Cnv.tohex(pt))
    print(f"PT = {pt}")
    # Do the business
    ct = crsysapi.CipherStream.bytes(pt, key, iv, crsysapi.CipherStream.Alg.CHACHA20, counter=1)
    print("CT =", crsysapi.Cnv.tohex(ct))
    print("OK =", okhex)
    assert (okhex.lower() == crsysapi.Cnv.tohex(ct).lower())
    # Repeat to decrypt
    dt = crsysapi.CipherStream.bytes(ct, key, iv, crsysapi.CipherStream.Alg.CHACHA20, counter=1)
    print("DT =", crsysapi.Cnv.tohex(dt))
    assert (pt == dt)


def quick_version():
    print("\nDETAILS OF CORE DLL...")
    print("DLL Version=" + str(crsysapi.Gen.version())
          + " [" + crsysapi.Gen.core_platform() + "] Lic="
          + crsysapi.Gen.licence_type()
          + " Compiled=["
          + crsysapi.Gen.compile_time() + "]")
    print("[" + crsysapi.Gen.module_name() + "]")


def main():
    # TODO:
    # for arg in sys.argv:
    #     global delete_tmp_dir
    #     if (arg == 'nodelete'):
    #         delete_tmp_dir = False
    #     elif (arg == 'some'):
    #         do_all = False
    # setup_temp_dir()

    # DO THE TESTS - EITHER SOME OR ALL
    if (do_all):
        test_error_lookup()
        test_cnv()
        test_cipher()
        test_cipher_hex()
        test_cipher_file()
        test_cipher_block()
        test_cipher_pad()
        test_crc()
        test_rng()
        test_hash()
        test_mac()
        test_prf()
        test_xof()
        test_wipe()
        test_compress()
        test_blowfish()
        test_pbe()
        test_aead()
        test_cipherstream()

    else:   # just do some tests: comment out as necessary
        # test_error_lookup()
        # test_cnv()
        # test_cipher()
        # test_cipher_hex()
        # test_cipher_block()
        # test_cipher_file()
        test_cipher_pad()
        # test_crc()
        # test_rng()
        # test_hash()
        # test_mac()
        # test_prf()
        # test_xof()
        # test_wipe()
        # test_compress()
        # test_blowfish()
        # test_pbe()
        # test_aead()
        # test_cipherstream()

        # ## reset_start_dir()
    quick_version()
    print("crsysapi.__version__=", crsysapi.__version__)
    print("ALL DONE.")


if __name__ == "__main__":
    main()
