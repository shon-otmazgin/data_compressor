import os
from utils.bytes_utils import pad_encoded_text, remove_padding, get_byte_array


ASCII_TO_INT: dict = {i.to_bytes(1, 'big'): i for i in range(256)}
INT_TO_ASCII: dict = {i: b for b, i in ASCII_TO_INT.items()}


class LZW_Coding:
    def __init__(self, path):
        """
        :param path: file path to compress
        """
        self.path = path
        self.n_bits = None
        self.keys = ASCII_TO_INT.copy()
        self.reverse_lzw_mapping = INT_TO_ASCII.copy()
        self.n_keys = len(ASCII_TO_INT)

    def lzw_compress(self):
        """
        compress the file located in self.path using lempel-ziv algo.
        :return: None. saving the compressed data into filename + ".bin"
        """

        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".lzw.bin"

        with open(self.path, 'rb') as file, open(output_path, 'wb') as output:
            data = file.read()

            compressed: list = []
            string = b''

            for symbol in data:
                string_plus_symbol = string + symbol.to_bytes(1, 'big') # get input symbol.
                if string_plus_symbol in self.keys:
                    string = string_plus_symbol
                else:
                    compressed.append(self.keys[string])
                    self.keys[string_plus_symbol] = self.n_keys
                    self.reverse_lzw_mapping[self.n_keys] = string_plus_symbol
                    self.n_keys += 1
                    string = symbol.to_bytes(1, 'big')

            if string in self.keys:
                compressed.append(self.keys[string])
            self.n_bits = len(bin(self.n_keys)[2:])
            bits: str = ''.join([bin(i)[2:].zfill(self.n_bits) for i in compressed])
            padded_text = pad_encoded_text(encoded_text=bits)
            b = get_byte_array(padded_encoded_text=padded_text)
            output.write(b)
        print("LZW Compressed")
        return output_path

    def lzw_decompress(self, input_path):
        """
        decompress input_file
        :param input_path: the file to decompress using lempel-ziv algo.
        :return: None. file decompressed saved to filename + "_decompressed" + ".txt"
        """
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed_lzw" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'wb') as output:
            bit_string_list = []

            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string_list.append(bits)
                byte = file.read(1)

            padded_encoded_text = ''.join(bit_string_list)

            encoded_text = remove_padding(padded_encoded_text)

            decoded_text = []
            start = 0
            while start < len(encoded_text):
                code = encoded_text[start:start + self.n_bits]
                key = int(code, 2)
                decoded_text.append(self.reverse_lzw_mapping[key])
                start += self.n_bits
            output.write(b''.join(decoded_text))
            print("LZW Decompressed")
            return output_path
