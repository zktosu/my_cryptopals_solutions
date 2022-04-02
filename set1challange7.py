import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# in file testing, 
# same key against sample test generated, 
#
key = b'YELLOW SUBMARINE'
text_to_text = b'sample'
sample_res = '9f9090339977d09ba130509b61122261'

def read_file(fname):
    return base64.b64decode(open(fname,'rb').read())

if __name__ == '__main__':
    ''' this challenge was about how to use AES with python
    - import AES
    - create new cipher ( could be used to decrypt or encrypt)
    - give it the key
    - decrypt file, 
    - unpad to make sure that it gives the correct result 
    '''
    all_text = read_file('7.txt')
    cipher = AES.new(key, AES.MODE_ECB)
    # test, make sure you get b'sample' with this test.
    # ciphered_text = cipher.decrypt(bytes.fromhex(sample_res))
    ciphered_text = cipher.decrypt(all_text)
    ciphered_text = unpad(ciphered_text, AES.block_size)
    print(ciphered_text)
