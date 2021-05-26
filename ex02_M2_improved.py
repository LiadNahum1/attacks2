import json
import numpy as np


USER = "318841285"
DIFFICULTY = 2
NUMBER_OF_LEAKS = 64
NUMBER_OF_TRACES = 10000
KEY_LENGTH = 16
FILE_NAME = "318841285/traces_318841285_3.txt"
AES_SBOX = [
0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

HW = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 1, 2, 2, 3, 2, 3,
      3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4,
      3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4,
      4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5,
      3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6,
      6, 7, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 3, 4, 4, 5,
      4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8]


def get_traces_and_plaintexts(filename):
    """
    returns the traces and plaintexts as numpy arrays.
    traces is a 2-dimensional array
    """

    with open(filename, 'r') as traces_file:
        leaks_list = traces_file.readlines()
        leaks_list = [json.loads(leak) for leak in leaks_list]
        traces = [leaks_dict['leaks'] for leaks_dict in leaks_list]
        plaintexts = [leaks_dict['plaintext'] for leaks_dict in leaks_list]
        plaintexts = [bytes.fromhex(plaintext) for plaintext in plaintexts]
        plaintexts = [[byte for byte in plaintext] for plaintext in plaintexts]

    return np.array(traces), np.array(plaintexts) #traces 10000X64 , plaintexts 10000X16


def apply_sbox(num):
    return AES_SBOX[num]


def apply_hw(num):
    return HW[num]


traces, plaintexts = get_traces_and_plaintexts(FILE_NAME)
v_apply_sbox = np.vectorize(apply_sbox)
v_apply_hw = np.vectorize(apply_hw)
num_traces = len(plaintexts)
num_of_leaks = np.shape(traces)[1]
important_times_per_byte = []

def byte_process(key_byte, key_array):
    global num_of_leaks, num_traces, plaintexts, v_apply_sbox, v_apply_hw, traces, important_times_per_byte
    correlation_hw_xor = np.zeros(shape=(256, num_of_leaks))
    correlation_hw_sbox = np.zeros(shape=(256, num_of_leaks))

    hw_on_xor = np.zeros(shape=(num_traces, 256))
    hw_on_sbox = np.zeros(shape=(num_traces, 256))

    for byte_guess in range(256):
        # gives an array of the current byte we check xor-ed with the key for each plaintext
        byte_with_key_guesses = np.bitwise_xor(plaintexts[:, key_byte], byte_guess)
        hw_on_xor[:, byte_guess] = v_apply_hw(byte_with_key_guesses) 

        sboxed_bytes = v_apply_sbox(byte_with_key_guesses)
        # put in the place of the current byte guess the hw of all plaintext (on the number of byte we are guessing)
        # after first sbox with the key guess
        hw_on_sbox[:,byte_guess] = v_apply_hw(sboxed_bytes)

        for i in range(num_of_leaks):
            correlation_hw_xor[byte_guess, i] = np.corrcoef(hw_on_xor[:,byte_guess], traces[:, i])[0][1]
            correlation_hw_sbox[byte_guess, i] = np.corrcoef(hw_on_sbox[:,byte_guess], traces[:, i])[0][1]


    print(f'256X64 {correlation_hw_xor}')
    print(f'256X64 {correlation_hw_sbox}')

    #correlation_hw_xor = np.abs(correlation_hw_xor)
    #correlation_hw_sbox = np.abs(correlation_hw_sbox)
    differences = correlation_hw_xor * correlation_hw_sbox
    differences = np.abs(differences)
    # take the byte of where the correlation was most powerful
    key_array[key_byte] = (np.where(differences == np.max(differences))[0][0])
    important_times_per_byte.append((np.where(differences == np.max(differences))[1][0]))



def main():
    print(FILE_NAME)
    key = [0] * KEY_LENGTH
    for key_byte in range(KEY_LENGTH):
        byte_process(key_byte, key)

    key = ''.join(list(map(lambda x: "{:02x}".format(x), key)))
    print(f'{USER},{key},{DIFFICULTY}')
    print(important_times_per_byte)



if __name__ == '__main__':
    main()