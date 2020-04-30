### Supported ANSI character sets
ANSI stands for American National Standards Institute.  
The [ANSI](http://ascii-table.com/ansi-codes.php) character set includes the standard ASCII character set (values 0 to 127), plus an extended character set (values 128 to 255).

### Results:
Tested file: [dickens.txt](https://github.com/kzjeef/algs4/blob/master/burrows-wheelers/testfile/dickens.txt)  

|   | LZW + Huffman | LZW  |  Huffman |
|---|---|---|---|
| Before compress  |  31457485 |  31457485 |  31457485 |
| After compress  | **10231109**  |  11098586 | 17786285  |
| After Decompressed |  31457485 |  31457485 |  31457485 |
| Files Identical |  True |  True |  True |
| Compress Time |  63.672 s |  36.560 s |  18.525 s |
| Decompress Time |  34.791 s |  13.231 s | 41.852 s  |
