def ceaser_cipher(text, shift=0):
    """
    Encrypts the given text using the Caesar cipher algorithm.
    """

    cipher_text = ""

    for char in text:
        if not char.isalpha():
            cipher_text += char; continue

        ascii_offset = 65 if char.isupper() else 97
        cipher_text += chr(ord(char) + shift)
            
    return cipher_text

print('Ceaser cipher', ceaser_cipher("Hello world", 1))