"""
Forked from https://github.com/janglin/crypto-pkcs7-example
Refactored suitable for python3 and more pythonic way.
* Changed xrange:
 https://docs.python.org/3.0/whatsnew/3.0.html
 range() now behaves like xrange() used to behave,
 except it works with values of arbitrary size.
 The latter no longer exists.
* StringIO comes from io
"""
import binascii
from io import StringIO


class PKCS7Encoder(object):
    '''
    RFC 2315: PKCS#7 page 21
    Some content-encryption algorithms assume the
    input length is a multiple of k octets, where k > 1, and
    let the application define a method for handling inputs
    whose lengths are not a multiple of k octets. For such
    algorithms, the method shall be to pad the input at the
    trailing end with k - (l mod k) octets all having value k -
    (l mod k), where l is the length of the input. In other
    words, the input is padded at the trailing end with one of
    the following strings:

             01 -- if l mod k = k-1
            02 02 -- if l mod k = k-2
                        .
                        .
                        .
          k k ... k k -- if l mod k = 0

    The padding can be removed unambiguously since all input is
    padded and no padding string is a suffix of another. This
    padding method is well-defined if and only if k < 256;
    methods for larger k are an open issue for further study.
    '''
    def __init__(self, k=16):
        self.k = k

    def decode(self, text):
        '''
        Remove the PKCS#7 padding from a text string
        :param text: The padded text for which the padding is to be removed.
        :exception ValueError: Raised when the input padding is missing or corrupt.
        '''
        length_of_input = len(text)
        last = text[-1]
        if isinstance(last, str):
            last = last.encode('utf-8')
        val = int(binascii.hexlify(last), 16)
        if val > self.k:
            raise ValueError('Input is not padded or padding is corrupt')

        padding_length = length_of_input - val
        return text[:padding_length]

    def encode(self, text):
        '''
        Pad an input string according to PKCS#7
        :param text: The text to encode.
        '''
        length_of_input = len(text)
        output = StringIO()
        val = self.k - (length_of_input % self.k)
        for _ in range(val):
            output.write('%02x' % val)
        return text + binascii.unhexlify(output.getvalue())
