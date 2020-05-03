import os
import heapq
from utils.heap_node import HeapNode
from utils.bytes_utils import pad_encoded_text, remove_padding, get_byte_array


ASCII_TO_INT: dict = {i.to_bytes(1, 'big'): i for i in range(256)}
INT_TO_ASCII: dict = {i: b for b, i in ASCII_TO_INT.items()}


class Lempel_Ziv_Huffman_Coding:
    def __init__(self, path):
        """
        :param path: the file path to compress
        """
        self.path = path
        self.lzw_n_bits = None
        self.lzw_keys = ASCII_TO_INT.copy()
        self.reverse_lzw_keys = INT_TO_ASCII.copy()
        self.n_keys = len(ASCII_TO_INT)

        self.heap = []
        self.frequency = {}
        self.codes = {}
        self.reverse_mapping = {}

    def compress(self):
        """
        compress the file located in self.path using lempel-ziv & huffman algo.
        :return: None. saving the compressed data into filename + ".bin"
        """
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'rb') as file, open(output_path, 'wb') as output:
            data = file.read()

            lzw_compress = self.lzw_compress(data=data)

            b = self.huffman_compress(lzw_compress=lzw_compress)

            output.write(b)
        return output_path

    def decompress(self, input_path):
        """
        decompress input_file
        :param input_path: the file to decompress using huffman & lempel-ziv algo.
        :return: None. file decompressed saved to filename + "_decompressed" + ".txt"
        """
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'wb') as output:
            bit_string_list = []

            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string_list.append(bits)
                byte = file.read(1)

            padded_encoded_text = ''.join(bit_string_list)

            huffman_decompress = self.huffman_decompress(padded_encoded_text=padded_encoded_text)

            b = self.lzw_decompress(huffman_decompress=huffman_decompress)

            output.write(b)
        return output_path

    def lzw_compress(self, data):
        """
        compressing text file using lempel-ziv algo.
        :param data: data text to compress using lempel-ziv algo
        :return: list of numbers - the data encoded.
        """
        compressed: list = []
        string = b''

        for symbol in data:
            string_plus_symbol = string + symbol.to_bytes(1, 'big') # get input symbol.
            if string_plus_symbol in self.lzw_keys:
                string = string_plus_symbol
            else:
                compressed.append(self.lzw_keys[string])
                self.lzw_keys[string_plus_symbol] = self.n_keys
                self.reverse_lzw_keys[self.n_keys] = string_plus_symbol
                self.n_keys += 1
                string = symbol.to_bytes(1, 'big')

        if string in self.lzw_keys:
            compressed.append(self.lzw_keys[string])
        print("Compressed LZW")
        return compressed
        # self.lzw_n_bits = len(bin(self.n_keys)[2:])
        # bits: str = ''.join([bin(i)[2:].zfill(self.lzw_n_bits) for i in compressed])
        # padded_text = self.pad_encoded_text(encoded_text=bits)
        # b = self.get_byte_array(padded_encoded_text=padded_text)
        # return b

    def lzw_decompress(self, huffman_decompress):
        """
        decompress using lempel-ziv algo. the data should be decompressed using huffman
        :param huffman_decompress: list of numbers to decompress
        :return: text decoded
        """
        decoded_text = []
        for code in huffman_decompress:
            decoded_text.append(self.reverse_lzw_keys[code])
        print('Decompressed LZW')
        return b''.join(decoded_text)

    def make_frequency_dict(self, text):
        """
        :param text: text to count the frequency of each character
        :return: None saved to self.frequency
        """
        for character in text:
            try:
                self.frequency[character] += 1
            except KeyError:
                self.frequency[character] = 1

    def make_heap(self):
        """
        creating heap: node for each character value is the frequency.
        :return: None saved to self.heap
        """
        for key, frq in self.frequency.items():
            node = HeapNode(key, frq)
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        """
        merging each 2 nodes(node characters) in heap with the lowest frequencies until no 2 nodes for characters
        :return: None. saved to self.heap
        """
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        """
        recursive method to calculate the code for root
        :param root: the root of the heap/the sub tree during the recursive
        :param current_code: the current mode in the path to the character
        :return: None saved to self.codes and self.reverse_mapping
        """
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        """
        creating code and the reserve info for each character
        :return: None saved to self.codes and self.reverse_mapping
        """
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        """
        encoding the text to string of bits
        :param text: the text to encode
        :return: the encoded text - bits string
        """
        encoded_text_list = []
        for character in text:
            encoded_text_list.append(self.codes[character])
        return ''.join(encoded_text_list)

    def huffman_compress(self, lzw_compress):
        """
        getting data compressed after lempel ziv algo. and compress it using huffman.
        :param lzw_compress: list of numbers -> the data compressed with lempel-ziv
        :return: bytes -> the data compressed with huffman.
        """
        # text = text.rstrip()

        self.make_frequency_dict(lzw_compress)
        self.make_heap()
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(lzw_compress)

        padded_encoded_text = pad_encoded_text(encoded_text)

        b = get_byte_array(padded_encoded_text)

        print("Compressed Huffman")
        return b

    def decode_text(self, encoded_text):
        """
        transforming bit string to text
        :param encoded_text: bits string encoded text
        :return: text decoded.
        """
        current_code = ""
        decoded_list = []

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_list.append(self.reverse_mapping[current_code])
                current_code = ""
        return decoded_list

    def huffman_decompress(self, padded_encoded_text):
        """
        decompressing bits string using huffman
        :param padded_encoded_text: the bits sting to decompressed
        :return: list of numbers (the data compressed using lempel ziv)
        """
        encoded_text = remove_padding(padded_encoded_text)

        decompressed_list = self.decode_text(encoded_text)
        print("Decompressed Huffman")
        return decompressed_list

