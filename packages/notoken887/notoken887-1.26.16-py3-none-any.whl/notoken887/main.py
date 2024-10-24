import argparse
import os
from notoken887.encryptor import TokenCryptor

def encrypt_code(code):
    cryptor = TokenCryptor()
    encrypted_lines = []
    for line in code.splitlines():
        if line.strip().startswith("import") or line.strip().startswith("from"):
            encrypted_lines.append(line)
        else:
            encrypted_lines.append(cryptor.encrypt(line))
    encrypted_code = '\n'.join(encrypted_lines)
    return encrypted_code

def decrypt_code(encrypted_content):
    cryptor = TokenCryptor()
    encrypted_code = ''
    for line in encrypted_content.splitlines():
        if line.strip().startswith("encrypted_code"):
            encrypted_code = line.split('=')[1].strip().strip("'''")
            break
    decrypted_string = cryptor.decrypt(encrypted_code)
    return decrypted_string

def smash_into_one_line(content):
    smashed_content = ''.join(content.split())
    smashed_content_with_char = ''
    for i, char in enumerate(smashed_content):
        smashed_content_with_char += char
        if (i + 1) % 2 == 0:  # Insert the character after every character
            smashed_content_with_char += '╢'
    return smashed_content_with_char.rstrip('╢')  # Remove the last '╢'

def process_file(input_path, output_path, mode):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, 'r', encoding='utf-8') as infile:
        content = infile.read()

    if mode == 'e':
        encrypted_code = encrypt_code(content)
        output_content = f"""from notoken887.encryptor import TokenCryptor
cryptor = TokenCryptor()
encrypted_code = '''{encrypted_code}'''
def run_decrypted_code():
    decrypted_string = cryptor.decrypt(encrypted_code)
    exec(decrypted_string, globals())
if __name__ == "__main__":
    run_decrypted_code()"""
        smashed_output_content = smash_into_one_line(output_content)
    else:
        decrypted_content = decrypt_code(content)
        smashed_output_content = smash_into_one_line(decrypted_content)

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(smashed_output_content)

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt Python files using TokenCryptor.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output file path')
    parser.add_argument('--mode', '-m', choices=['e', 'd'], required=True, help='Mode: e for encrypt, d for decrypt')
    args = parser.parse_args()
    process_file(args.input, args.output, args.mode)

if __name__ == "__main__":
    main()
