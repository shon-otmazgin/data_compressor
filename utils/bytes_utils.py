def pad_encoded_text(encoded_text):
    """
    padding the encoded text to fit for bytes. if bit string is 14 adding 2 bits
    :param encoded_text: the encoded text to pad
    :return: padded encoded text
    """
    extra_padding = 8 - len(encoded_text) % 8
    for i in range(extra_padding):
        encoded_text += "0"

    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text


def remove_padding(padded_encoded_text):
    """
    removing the extra padded bits from bits string
    :param padded_encoded_text: bits string to un pad
    :return: bit string  un padded encoded text
    """
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)

    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1 * extra_padding]

    return encoded_text


def get_byte_array(padded_encoded_text):
    """
    creating bytes array from bits string
    :param padded_encoded_text: bits string to transform to bytes array
    :return: bytes array
    """
    if len(padded_encoded_text) % 8 != 0:
        print("Encoded text not padded properly")
        exit(0)

    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i + 8]
        b.append(int(byte, 2))
    return b

