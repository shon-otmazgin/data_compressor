import heapq
import os
from utils.heap_node import HeapNode
from utils.bytes_utils import pad_encoded_text, remove_padding, get_byte_array


class Huffman_Coding:
    def __init__(self, path):
        """
        :param path: file path to compress
        """

        self.path = path
        self.heap = []
        self.frequency = {}
        self.codes = {}
        self.reverse_mapping = {}

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
        mearging each 2 nodes(node characters) in heap with the lowest frequencies until no 2 nodes for characters
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

    def compress(self):
        """
        compress the file located in self.path
        :return: None. saving the compressed data into filename + ".bin"
        """
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()

            # text = text.rstrip()

            self.make_frequency_dict(text)
            self.make_heap()
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.get_encoded_text(text)

            padded_encoded_text = pad_encoded_text(encoded_text)

            b = get_byte_array(padded_encoded_text)

            output.write(bytes(b))

        print("Compressed")
        return output_path

    def decode_text(self, encoded_text):
        """
        transforming bit string to text
        :param encoded_text: bits string encoded text
        :return: text decoded.
        """
        current_code = ""
        decoded_text_list = []

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text_list.append(self.reverse_mapping[current_code])
                current_code = ""

        return ''.join(decoded_text_list)

    def decompress(self, input_path):
        """
        decompress input_file
        :param input_path: the file to decompress
        :return: None. file decompressed saved to filename + "_decompressed" + ".txt"
        """
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w', newline='') as output:
            bit_string_list = []

            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string_list.append(bits)
                byte = file.read(1)

            padded_encoded_text = ''.join(bit_string_list)

            encoded_text = remove_padding(padded_encoded_text)

            decompressed_text = self.decode_text(encoded_text)
            output.write(decompressed_text)

        print("Decompressed")
        return output_path
