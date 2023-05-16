import compression, sys

def main():
    name = sys.argv[1]
    f = open("../proves/" + name + ".txt","r")
    txt = f.read()
    #first BWT
    cod, ind = compression.encode_burrows_wheeler(txt)
    #then Huffman
    huff_cod = compression.huffman_code(cod)
    huff_txt = compression.encode(cod,huff_cod)
    codification = ind + '\n' + huff_txt
    f = open(name + ".cdi", "w")
    f.write(codification)


if __name__ == '__main__':
    main()