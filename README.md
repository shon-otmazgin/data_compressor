|   |  |
|---|---|
| Shon Otmazgin  |  305394975 |
| Sapir Rubin  |  301659751 | 

### Abstract
Compering 3 methods for compressing text files:
- Lempel-Ziv-Welch
- Huffman Coding
- Lempel-Ziv-Welch + Huffman Coding (**best results**)

Coded at Python 3.7.4.

### Results
Tested file: [dickens.txt](https://github.com/kzjeef/algs4/blob/master/burrows-wheelers/testfile/dickens.txt)  

|   | LZW + Huffman | LZW  |  Huffman |
|---|---|---|---|
| Before compress  |  31457485 |  31457485 |  31457485 |
| After compress  | **10231109**  |  11098586 | 17786285  |
| After Decompressed |  31457485 |  31457485 |  31457485 |
| Files Identical |  True |  True |  True |
| Compress Time |  63.672 s |  36.560 s |  18.525 s |
| Decompress Time |  34.791 s |  13.231 s | 41.852 s  |

### Supported ANSI character sets
ANSI stands for American National Standards Institute.  
The [ANSI](http://ascii-table.com/ansi-codes.php) character set includes the standard ASCII character set (values 0 to 127), plus an extended character set (values 128 to 255).

### Instrucations
- Send the imput file **path** to constructor classes  
    Example:
    ```python
    path = 'dickens.txt'
    
    lzw_h = Lempel_Ziv_Huffman_Coding(path=path)
    lzw = LZW_Coding(path=path)
    h = Huffman_Coding(path=path)
    ```
- Compress method  
  return: output_file_**path** name(.bin) and creating file with data compressed.  
  Example:
  ```python
    output_path = lzw_h.compress()
    output_path = lzw.compress()
    output_path = h.compress()
    ```
- Decompress method  
  input: file_path_to_decompress(.bin)  
  return: output_file_**path** name and creating '_decompressed.txt' file with the data decompressed.  
  Example:
  ```python
    output_path = lzw_h.decompress(output_path)
    output_path = lzw.lzw_decompress(output_path)
    output_path = h.decompress(output_path)
    ```
  
 For full Example please run ```tester_lzw_huffman.py```, ```tester_lzw.py```, ```tester_huffman.py```
