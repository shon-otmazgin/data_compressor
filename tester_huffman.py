import time
from huffman.huffman import Huffman_Coding
import os

#input file path
path = 'dickens.txt'

h = Huffman_Coding(path=path)

start_time = time.time()
output_path = h.compress()
print(f'Compressed to {output_path}')
print(f'Before compress: {os.path.getsize(path)}')
print(f'After compress:  {os.path.getsize(output_path)}')
print(f"--- {time.time() - start_time:.3f} seconds ---")

print()

start_time = time.time()
output_path = h.decompress(output_path)
print(f'Decompressed to {output_path}')
print(f'Before compress:     {os.path.getsize(path)}')
print(f'After Decompressed:  {os.path.getsize(output_path)}')
print(f"--- {time.time() - start_time:.3f} seconds ---")

print()
with open(path, 'rb') as ori_file, open(output_path, 'rb') as deco_file:
    text1 = ori_file.read()
    text2 = deco_file.read()
    print('Before-After:')
    print('Identical files !' if text1 == text2 else 'Not identical files!')
