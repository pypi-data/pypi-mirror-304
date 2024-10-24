import argparse
import os
from notoken887.encryptor import TokenCryptor

def encrypt_code(code):
    cryptor=TokenCryptor()
    encrypted_lines=[]
    for line in code.splitlines():
        if line.strip().startswith("import") or line.strip().startswith("from"):
            encrypted_lines.append(line)
        else:
            encrypted_lines.append(cryptor.encrypt(line))
    encrypted_code='\n'.join(encrypted_lines)
    return encrypted_code

def process_file(input_path,output_path,mode):
    os.makedirs(os.path.dirname(output_path),exist_ok=True)
    with open(input_path,'r') as infile:
        content=infile.read()
    if mode=='e':
        encrypted_code=encrypt_code(content)
        output_content=f"""from notoken887.encryptor import TokenCryptor
cryptor=TokenCryptor()
encrypted_code='''{encrypted_code}'''
def run_decrypted_code():
    decrypted_string=cryptor.decrypt(encrypted_code)
    exec(decrypted_string,globals())
if __name__=="__main__":
    run_decrypted_code()"""
    else:
        output_content=content
    with open(output_path,'w') as outfile:
        outfile.write(output_content)

def main():
    parser=argparse.ArgumentParser(description='Encrypt or decrypt Python files using TokenCryptor.')
    parser.add_argument('i',type=str,help='Input file path')
    parser.add_argument('o',type=str,help='Output file path')
    parser.add_argument('mode',choices=['e','d'],help='Mode: e for encrypt, d for decrypt')
    args=parser.parse_args()
    process_file(args.i,args.o,args.mode)

if __name__=="__main__":
    main()
