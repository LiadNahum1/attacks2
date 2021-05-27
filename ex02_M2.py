import sys
import requests
import os
import json
import numpy as np
import matplotlib.pyplot as plt

CORRECT_NUMBER_OF_ARGUMENTS = 2
NOT_FOUND_ERROR_CODE = 404

NUMBER_OF_TRACES = 10000
KEY_LENGTH = 16
KEY_BYTE_POSSIBILITIES = 256
CORRECT_PASSWORDS = {'318841285': '7e680f4a466e17b864e561013eeac270', '207434044': '713ba1f9173aa51729cc8086e1f02b06',
                     '319082681': '5b717730f422759b720dc31cec0f0ce1'}

AES_SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

HW = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 1, 2, 2, 3, 2, 3,
      3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4,
      3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4,
      4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5,
      3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6,
      6, 7, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 3, 4, 4, 5,
      4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8]


def download_power_traces(filename, server_url, number_of_power_traces):
    """
    This function downloads `number_of_power_traces` traces from a remote server
    and write those traces to a local file
    :param filename: the name of the file witch will contain the traces
    :param server_url: the remote server url to dwonload the traces from
    :param number_of_power_traces: the number of traces to dwonload
    :return: this function does not return a value, it writes the traces to a file
    """
    leaks_list = []
    for i in range(number_of_power_traces):
        response = requests.get(server_url)
        if response.status_code == NOT_FOUND_ERROR_CODE:
            print(f'something wrong with the server, recived code: {response.status_code}, exiting...')
            sys.exit()
        response_as_json = response.json()
        leaks_list.append(f'{json.dumps(response_as_json)}\n')
    with open(filename, 'w') as traces_file:
        traces_file.writelines(leaks_list)


def get_traces_and_plaintexts(filename):
    """
    This function returns the traces and plaintexts as numpy arrays.
    :param filename: the name of the file which contains the traces
    """
    with open(filename, 'r') as traces_file:
        leaks_list = traces_file.readlines()
        leaks_list = [json.loads(leak) for leak in leaks_list]
        traces = [leaks_dict['leaks'] for leaks_dict in leaks_list]
        plaintexts = [leaks_dict['plaintext'] for leaks_dict in leaks_list]
        plaintexts = [bytes.fromhex(plaintext) for plaintext in plaintexts]
        plaintexts = [[byte for byte in plaintext] for plaintext in plaintexts]
    return np.array(traces), np.array(plaintexts)


def apply_sbox(num):
    return AES_SBOX[num]


def apply_hw(num):
    return HW[num]


def byte_process(traces, plaintexts, key_byte):
    """
   This function searches for the correct byte of the key.
   :param traces: traces of power consumptions
   :param plaintexts: plaintext for each trace,  as an array of bytes. Each plaintext is 16 bytes
   :param key_byte: the index of the key byte that the function searches
   :return: the function finds the cell with the highest correlation and returns the correct byte (row index of the cell)
   with the correct time point (column index of the cell).
    """
    num_traces = len(plaintexts)
    num_of_leaks = np.shape(traces)[1]

    # make apply_sbox and apply_hw function work on vectors
    v_apply_sbox = np.vectorize(apply_sbox)
    v_apply_hw = np.vectorize(apply_hw)

    differences = np.zeros(shape=(KEY_BYTE_POSSIBILITIES, num_of_leaks))  # contains the correlations
    hw_matrix = np.zeros(shape=(num_traces, KEY_BYTE_POSSIBILITIES))  # contains hw(sbox(p_i xor k_i))

    for byte_guess in range(KEY_BYTE_POSSIBILITIES):
        # xor each plaintext with the guessed byte
        xor_plaintext_with_key_byte = np.bitwise_xor(plaintexts[:, key_byte], byte_guess)
        # apply sbox on each xor result
        sboxed_bytes = v_apply_sbox(xor_plaintext_with_key_byte)
        # apply hw on each sbox result. put this vector as a column in hw_matrix at column index byte_guess
        hw_matrix[:, byte_guess] = v_apply_hw(sboxed_bytes)

        # for each time point and byte guess save a correlation
        for i in range(num_of_leaks):
            differences[byte_guess, i] = np.corrcoef(hw_matrix[:, byte_guess], traces[:, i])[0][1]

    differences = np.abs(differences)
    # find the cell with the highest correlation.
    # returns the byte and the time point
    correct_key_byte = np.where(differences == np.max(differences))[0][0]
    correct_time = np.where(differences == np.max(differences))[1][0]
    return correct_key_byte, correct_time


def get_correct_key(traces, plaintexts, number_of_traces=NUMBER_OF_TRACES):
    """
       :param traces: traces of power consumptions
       :param plaintexts: plaintext for each trace,  as an array of bytes. Each plaintext is 16 bytes
       :param number_of_traces: a number specifies how many traces the function can use in order to
       find the key.
       :return the function returns the key and the important time points it found. 
    """
    key = [0] * KEY_LENGTH
    important_times_per_byte = []
    for key_byte in range(KEY_LENGTH):
        key[key_byte], time = byte_process(traces[:number_of_traces, :], plaintexts[:number_of_traces, :], key_byte)
        important_times_per_byte.append(time)

    key = ''.join(list(map(lambda x: "{:02x}".format(x), key)))
    return key, important_times_per_byte


def check_how_many_correct_bytes(key, correct_key):
    """
       This function checks how many correct bytes there are in key compared to correct_key
       :param key: a key represented as string. 32 characters are representing 16 bytes.
       :param correct_key: a key represented as string and compare to it, the function counts how many correct bytes
       :return: returns the number of correct bytes in key
    """
    correct_bytes = 0
    for char_index in range(0, len(key), 2):
        if key[char_index:char_index + 2] == correct_key[char_index:char_index + 2]:
            correct_bytes += 1
    return correct_bytes


def correct_bytes_number_traces(traces, plaintexts, correct_key):
    """
       This function goes over different number of traces in step of size 1000, and checks for each number of
       traces, how many correct bytes there are in the founded key. Eventually plots a graph with the number of
       traces on the x scale and the count of correct bytes in the output on the y scale
       :param traces: traces of power consumptions
       :param plaintexts: plaintext for each trace,  as an array of bytes. Each plaintext is 16 bytes
       :param correct_key: a key represented as string and compare to it, the function counts how many correct bytes in
       the calculated key
    """
    y_number_of_correct_bytes = []
    x_traces = range(1000, NUMBER_OF_TRACES + 1000, 1000)
    for i in x_traces:
        key, _ = get_correct_key(traces, plaintexts, i)
        correct_bytes = check_how_many_correct_bytes(key, correct_key)
        y_number_of_correct_bytes.append(correct_bytes)
        
    # plot graph
    plt.plot(x_traces, np.asarray(y_number_of_correct_bytes))
    plt.legend()
    plt.xlabel('Number Of Traces')
    plt.ylabel('Number Of Correct Bytes')
    plt.title('User 318841285 Difficulty 2')
    plt.show()


def main():
    user = '318841285'
    difficulty = 2
    server_url = f'http://aoi.ise.bgu.ac.il/encrypt?user={user}&difficulty={difficulty}'

    if len(sys.argv) < CORRECT_NUMBER_OF_ARGUMENTS:
        print(f'Illegal number of arguments')
        sys.exit()

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        download_power_traces(filename, server_url, NUMBER_OF_TRACES)

    traces, plaintexts = get_traces_and_plaintexts(filename)
    key, important_times_per_byte = get_correct_key(traces, plaintexts)
    print(f'{user},{key},{difficulty}')

    print(important_times_per_byte)
    correct_bytes_number_traces(traces, plaintexts, '7e680f4a466e17b864e561013eeac270')


if __name__ == '__main__':
    main()