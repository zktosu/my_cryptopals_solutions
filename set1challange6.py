from base64 import b64decode

class S1L6:
    # this is the possible keysizes, [ we will check for these values ] 
    KEYSIZES = list(range(2,41))
    BLOCKSIZE = 0


    def __init__(self, file_name: str):
        self.input_data = b64decode(open(file_name,'rb').read())
        self.find_keysize()
        self.t_data = self.transpose()
        self.repeated_key = self.find_repeated_key()

    def transpose(self):
        # this was the tricky point!
        t_data = [[] for _ in range(self.BLOCKSIZE)]
        # print(t_data)
        for k in range(self.BLOCKSIZE):
            for i in range(k, len(self.input_data), self.BLOCKSIZE):
                t_data[k].append(self.input_data[i])
        return t_data

    def ham_dis_norm(self, st1, st2, keysize):
        ''' calculates the number of the diferent bits '''
        return sum([bin(a ^ b).count('1') for a,b in zip(st1,st2)])/keysize

    def find_keysize(self):
        ''' finds and assigns the key_size to self.BLOCKSIZE by averaging distance between consecutive byteblocks '''
        res = []
        for ks in self.KEYSIZES:
            distances = list()
            for i in range(0,len(self.input_data)-1,ks):
                # this line is tricky,
                # calculate normalized distance between consecutive values 
                # then we also normalize the normalizeddistance itself!! careful!!!
                # then we got the answer!
                distances.append(self.ham_dis_norm(self.input_data[i:i+ks], self.input_data[i+ks:i+2*ks], ks) / ks)
            # this line calculates average score, and sticks keysize to values,
            res.append((sum(sorted(distances)[:8])/8, ks))
        # we just assign the "min normalized ham distance giver keysize" to BLOCKSIZE for later use.
        self.BLOCKSIZE = min(res)[1]
    
    def english_score(self, data) -> int:
        ''' returns the english score number(int), bigger the number 
        bigger the chance that text is english '''
        s = 0
        data = data.lower()
        common = b'etaoin shrdlu'[::-1]
        for ch in data:
            i = common.find(ord(ch))
            if i:
                s+=i
        return s
    
    def xor_key(self, data, key) -> bytes :
        res = ''
        for b in data:
            res += chr(b ^ key)
        return res

    def decrypt_key(self, data):
        res = []
        for key in range(255):
            res.append( (self.english_score(self.xor_key(data, key)), key) )
        return max(res)[1]

    def find_repeated_key(self):
        res = ''
        for data in self.t_data:
            res += chr(self.decrypt_key(data))
        return res

    def repeated_key_xor(self,key):
        res = ''
        for i,b in enumerate(self.input_data):
            res += chr( ord(key[i%len(key)]) ^ b )
        return res

if __name__ == '__main__':
    o = S1L6('6.txt')
    print(o.repeated_key)
    # test for the un-encrypted result ;)
    print('='*100)
    print(o.repeated_key_xor(o.repeated_key)[:200])
