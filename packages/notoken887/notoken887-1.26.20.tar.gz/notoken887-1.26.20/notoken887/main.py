import argparse
import os
import re
from notoken887.encryptor import TokenCryptor

def encrypt_code(code):
    cryptor = TokenCryptor()
    encrypted_lines = []
    for line in code.splitlines():
        if line.strip().startswith("import") or line.strip().startswith("from"):
            continue  # Skip imports for encryption
        else:
            encrypted_lines.append(cryptor.encrypt(line))  # Encrypt other lines
    return '\n'.join(encrypted_lines)

def decrypt_code(encrypted_content):
    cryptor = TokenCryptor()
    decrypted_code = ''
    
    for line in encrypted_content.splitlines():
        if line.strip().startswith("encrypted_code"):
            encrypted_code = line.split('=')[1].strip().strip("'''")  # Remove quotes
            decrypted_code = cryptor.decrypt(encrypted_code)
            break
    
    decrypted_code = re.sub(r'#.*$', '', decrypted_code, flags=re.MULTILINE).strip()
    return decrypted_code

def process_file(input_path, output_path, mode):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, 'r', encoding='utf-8') as infile:
        content = infile.read()

    if mode == 'e':
        imports = [line for line in content.splitlines() if line.strip().startswith(("import", "from"))]
        encrypted_code = encrypt_code(content)
        
        output_content = f"""from notoken887.encryptor import TokenCryptor
cryptor = TokenCryptor()
{'\n'.join(imports)}\n# Encrypted code
encrypted_code = '''{encrypted_code}'''
def run_decrypted_code():
    decrypted_string = cryptor.decrypt(encrypted_code)
    exec(decrypted_string, globals())
if __name__ == "__main__":
    run_decrypted_code()"""
    else:
        decrypted_content = decrypt_code(content)
        output_content = decrypted_content.strip()  # Remove extra whitespace

    if mode == 'e':
        comment_lines = ["# " + "卐" * 350 for _ in range(2230)]
        output_lines_with_comments = []
        
        for line in output_content.splitlines():
            if "encrypted_code =" in line:
                output_lines_with_comments.append(line)
            else:
                output_lines_with_comments.append(f"{line}  # {('卐' * 2230)}")
                
        full_output_content = "\n".join(comment_lines) + "\n" + "\n".join(output_lines_with_comments) + "\n" + "\n".join(comment_lines)
    else:
        full_output_content = output_content

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(full_output_content)

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt Python files using TokenCryptor.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output file path')
    parser.add_argument('--mode', '-m', choices=['e', 'd'], required=True, help='Mode: e for encrypt, d for decrypt')
    args = parser.parse_args()
    process_file(args.input, args.output, args.mode)

if __name__ == "__main__":
    main()
