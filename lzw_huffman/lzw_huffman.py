import os
import heapq
from utils.heap_node import HeapNode

ASCII_TO_INT: dict = {i.to_bytes(1, 'big'): i for i in range(256)}
INT_TO_ASCII: dict = {i: b for b, i in ASCII_TO_INT.items()}


class Lempel_Ziv_Huffman_Coding:
    def __init__(self, path):
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
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'rb') as file, open(output_path, 'wb') as output:
            data = file.read()

            lzw_compress = self.lzw_compress(data=data)

            b = self.huffman_compress(lzw_compress=lzw_compress)

            output.write(b)
        return output_path

    def decompress(self, input_path):
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

    def lzw_compress(self, data) -> bytes:
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

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def lzw_decompress(self, huffman_decompress):
        decoded_text = []
        for code in huffman_decompress:
            decoded_text.append(self.reverse_lzw_keys[code])
        print('Decompressed LZW')
        return b''.join(decoded_text)

    def make_frequency_dict(self, text):
        for character in text:
            try:
                self.frequency[character] += 1
            except KeyError:
                self.frequency[character] = 1

    def make_heap(self):
        for key, frq in self.frequency.items():
            node = HeapNode(key, frq)
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        encoded_text_list = []
        for character in text:
            encoded_text_list.append(self.codes[character])
        return ''.join(encoded_text_list)

    def huffman_compress(self, lzw_compress):
        # text = text.rstrip()

        self.make_frequency_dict(lzw_compress)
        self.make_heap()
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(lzw_compress)

        padded_encoded_text = self.pad_encoded_text(encoded_text)

        b = self.get_byte_array(padded_encoded_text)

        print("Compressed Huffman")
        return b

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_list = []

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_list.append(self.reverse_mapping[current_code])
                current_code = ""
        return decoded_list

    def huffman_decompress(self, padded_encoded_text):
        encoded_text = self.remove_padding(padded_encoded_text)

        decompressed_list = self.decode_text(encoded_text)
        print("Decompressed Huffman")
        return decompressed_list

