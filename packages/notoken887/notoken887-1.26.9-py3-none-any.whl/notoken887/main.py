import argparse
from encryptor import TokenCryptor
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

def process_file(input_path, output_path, mode):
    with open(input_path, 'r') as infile:
        content = infile.read()
    
    if mode == 'encrypt':
        encrypted_code = encrypt_code(content)
        # Create the new structure with encrypted code
        output_content = f"""from notoken887.encryptor import TokenCryptor

cryptor = TokenCryptor()

# Encrypted code
encrypted_code = '''{encrypted_code}'''

def run_decrypted_code():
    decrypted_string = cryptor.decrypt(encrypted_code)
    exec(decrypted_string, globals())

# Run the function to execute the decrypted code
if __name__ == "__main__":
    run_decrypted_code()
"""
    else:
        output_content = content 

    with open(output_path, 'w') as outfile:
        outfile.write(output_content)

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt Python files using TokenCryptor.')
    parser.add_argument('mode', choices=['-e', '-d'], help='Mode: -e for encrypt, -d for decrypt')
    parser.add_argument('-filepath', type=str, required=True, help='Path to the input file')
    parser.add_argument('-outputpath', type=str, required=True, help='Path to save the output file')

    args = parser.parse_args()
    
    process_file(args.filepath, args.outputpath, args.mode)

if __name__ == "__main__":
    main()
