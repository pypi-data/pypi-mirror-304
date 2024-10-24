def railfence_cipher(text: str, no_of_rows=1) -> str:
    """
    Encrypts the given text using the Rail Fence cipher algorithm.
    """
    rows = [list() for _ in range(no_of_rows)]

    row_index = 0
    for char in text:
        rows[row_index].append(char)
        row_index = (row_index + 1) % no_of_rows

    encrypted_text = ''
    for row in rows:
        encrypted_text += ''.join(row)
    return encrypted_text

print('Railfence Cipher')
text = input('Enter text to encrypt: ')
row = int(input('Enter row value: '))
print('Cipher Text ->', railfence_cipher(text, no_of_rows=row))