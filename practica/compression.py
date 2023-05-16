# -*- coding: utf-8 -*-
"""compression.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Xe6MpFpmGERKm4DXdNJMZGbAtYLTnV4x
"""

from math import floor

def arithmetic_encode(txt,k,src):#hay q implementar lo de block size, es decir si la longitud de las letras de src
    block_size = len(src[0][0])
    suma = 0
    src2 = []
    for i in range(len(src)):
        suma += src[i][1]
    for i in range(len(src)):
        src2.append((src[i][0],src[i][1]/suma))
    alpha = '0' * k
    beta = '1' * k
    c = ""
    u = 0
    cumulative_probs = [0]
    aux = 0.0
    for i in range(len(src2)):
        aux += src2[i][1]
        cumulative_probs.append(aux)
    #for i in range(len(txt)):
    while txt:
        block = txt[:block_size]# q bueno soy hermano
        delta = int(beta,2) - int(alpha,2) + 1
        subintervals = []
        for j in range(1, len(cumulative_probs)):
            aux = (int(alpha,2) + int(floor(delta * cumulative_probs[j-1])),
                   int(alpha,2) + int(floor(delta * cumulative_probs[j]) - 1))
            subintervals.append(aux)
        ind = [src2.index(tupla) for tupla in src2 if tupla[0] == block][0]#solo se usa i aqui, en txt[i]
        alpha = bin(subintervals[ind][0])[2:].zfill(k)
        beta = bin(subintervals[ind][1])[2:].zfill(k)
        while alpha[0] == beta[0]:
            c += alpha[0]
            if alpha[0] == '0':
                    c += '1' * u
            else:
                    c += '0' * u
            u = 0
            alpha = alpha[1:] + '0'
            beta = beta[1:] + '1'
        while alpha[:2] == '01' and beta[:2] == '10':
            alpha = alpha[0] + alpha[2:] + '0'
            beta = beta[0] + beta[2:] + '1'
            u += 1
        txt = txt[block_size:]
    return c + '1'

def source_fromtext(txt):
    x = []
    for l in set(txt):
        n = txt.count(l)
        x.append((l,n))
    x.sort(key=lambda x: x[0])
    return x

class Node:
    def __init__(self, weight, sym, left=None, right=None):
        self.weight = weight
        self.sym = sym
        self.left = left
        self.right = right
        self.code = ""#0 o 1, depende de la dirección

def huffman_code(txt):
    total = 0
    src = source_fromtext(txt)
    for _, w in src:
        total += w#lo quito?
    src.sort(key=lambda x: x[1])
    #no se como hacer lo de los nodos la vd q coñazo, ademas hay q hacer un insert con selection PQ EL BISECT NO VA
    huff_tree = []
    for a, w in src:
      node = Node(w, a)
      huff_tree.append(node)
    while len(huff_tree) > 1:
      node1 = huff_tree[0]; node2 = huff_tree[1]
      huff_tree.remove(node1); huff_tree.remove(node2)
      weight = node1.weight + node2.weight
      sym = node1.sym + node2.sym
      left = node1
      right = node2
      node1.code = "0"
      node2.code = "1"
      node = Node(weight, sym, left, right)
      index = len(huff_tree)
      for i in range(0, len(huff_tree)):
          if huff_tree[i].weight >= weight:
              index = i
              break
      huff_tree.insert(index, node)
    huff_dict = calculate_codes(huff_tree[0])
    huff_code = [(k, v) for k, v in huff_dict.items()]#hay q pasarlo a lista para el output
    huff_code.sort(key=lambda x:x[0])#NECESARIO esto, para ordenarlo PRIMERO alfabéticamente...
    huff_code.sort(key=lambda x:len(x[1]))#... y luego para ordenarlos segun longitud respetando el orden alfabético
    #falta canonizar
    huff_lens = [len(x[1]) for x in huff_code] #longitudes de cada letra codificada en huffman
    huff_canon = canonize(huff_lens)
    letters = [x[0] for x in huff_code]
    huffman = list(zip(letters,huff_canon))
    huffman.sort(key = lambda x:x[0])

    return huffman

def canonize(lens):
  first = ""
  for i in range(0,lens[0]):
    first += "0"
  canonized = []
  canonized.append(first)
  last_len = lens[0]
  last_code = first
  del lens[0]
  for x in lens:
    code = increment_alf(last_code)
    n_appends = x-last_len
    for i in range(0,n_appends):
      code += "0"
    last_code = code
    last_len = x
    canonized.append(code)
  return canonized

def increment_alf(codeword,alf = ["0","1"]):#para sumar en binario
#     if codeword == None: esto nunca deberia suceder, hay un error
#         codeword = "" #es q si no se bugea lol
    carry = False
    s = list(codeword)
    i = len(codeword)-1
    if s[i] != alf[-1]:
        index_in_alf = alf.index(s[i])
        s[i] = alf[index_in_alf+1]
    else:
        s[i] = alf[0]
        carry = True
    
    if carry:
        while True:
            i -= 1
            #if i < 0: #esto es necesario? no sabria decirte
                #raise ValueError("ERROR: no existeix cap codi amb aquesta propietat")
            if s[i] != alf[-1]:
                index_in_alf = alf.index(s[i])
                s[i] = alf[index_in_alf+1]
                break
            else:
                s[i] = alf[0]
    codeword = "".join(s) #convertimos la lista en string
    return codeword #GILIPOLLAS

def calculate_codes(node, value = ""):#en vd creo q esto es INUTIL de cojones pq solo necesito las longitudes de cada letra y no el codigo entero, pero bueno, al menos lo tengo hecho por si aca
  codes = {}
  newValue = value + str(node.code)
  if(node.left): calculate_codes(node.left, newValue)
  if(node.right): calculate_codes(node.right, newValue)
  if(not node.left and not node.right): codes[node.sym] = newValue
  return codes

def encode(txta,corr):
#     txt = txta.split() #suponemos q son palabras separadas por espacios
#pues no son palabras SON LETRAS JAJJSKDJD TUS MUERTOS
    coded = []
    for c in txta:
        for x in corr:
            if c in x[0]:
                coded.append(x[1])
    txtb = "".join(coded)
    return txtb

def encode_LZ77(txt,s,t):
    tok = []
    tok.append((1, 0, txt[0]))
    current_pos = 1
    search = txt[0]
    lookahead = txt[1:1+t]
    while current_pos < len(txt):
        offset = 1
        length = 0
        char = lookahead[0]
        window = search + lookahead
        for i in range(len(search)-1, -1, -1):
            if search[i] == lookahead[0]:
                match = True
                iwind = i+1
                jwind = len(search)+1
                maxlen = 1
                while match and jwind < len(window):
                    if window[iwind] == window[jwind]:
                       maxlen += 1
                       iwind += 1
                       jwind += 1
                    else:
                        match = False
                if (maxlen > length):
                    if (current_pos+length+1 >= len(txt)):
                       break
                    offset = len(search)-i
                    length = maxlen
                    try:
                        char = window[jwind]
                    except:
                         try:
                             char = txt[current_pos+length]
                         except:
                              char = window[jwind-1]
                              length -= 1
                              if (length == 0):
                                  offset = 1
        tok.append((offset, length, char))
        current_pos += length+1
        if (current_pos-s < 0):
            search = txt[0:current_pos]
        else:
            search = txt[current_pos-s:current_pos]
        lookahead = txt[current_pos:current_pos+t]
    return tok

def encode_LZSS(txt,mm,s,t):
    tok = []
    tok.append(txt[0])
    current_pos = 1
    search = txt[0]
    lookahead = txt[1:1+t]
    while current_pos < len(txt):
        offset = 1
        length = 0
        window = search + lookahead
        for i in range(len(search)-1, -1, -1):
            if search[i] == lookahead[0]:
                match = True
                iwind = i+1
                jwind = len(search)+1
                maxlen = 1
                while match and jwind < len(window):
                    if window[iwind] == window[jwind]:
                       maxlen += 1
                       iwind += 1
                       jwind += 1
                    else:
                        match = False
                if (maxlen > length):
                    offset = len(search)-i
                    length = maxlen
        if length < mm:
            tok.append(lookahead[0])
            current_pos += 1
        else:
            tok.append((offset,length))
            current_pos += length
        if (current_pos-s < 0):
            search = txt[0:current_pos]
        else:
            search = txt[current_pos-s:current_pos]
        lookahead = txt[current_pos:current_pos+t]
    return tok

def encode_LZ78(txt):
    tok = []
    tok.append((0, txt[0]))
    dictionary = ['', txt[0]]
    current_pos = 1
    while current_pos < len(txt):
        pointer = ''
        if current_pos == len(txt)-1:
          tok.append((0, txt[current_pos]))
          break
        for i,x in enumerate(dictionary):
            if x == txt[current_pos]:
                pointer = i
                break
        if not pointer:
            tok.append((0, txt[current_pos]))
            dictionary.append(txt[current_pos])
            current_pos += 1
        else: 
            pos = current_pos+1
            b = True
            while b and pos < len(txt):
                if(pos == len(txt)-1):
                  b = True
                  pos += 1
                  break
                b = False
                for i,x in enumerate(dictionary):
                    if x == txt[current_pos:pos+1]:
                        pointer = i
                        b = True
                        break
                pos += 1
            if b and pos == len(txt):
                tok.append((pointer, txt[pos-1]))
            else:
                tok.append((pointer, txt[pos-1]))
            dictionary.append(txt[current_pos:pos])
            current_pos = pos
    return tok

def encode_LZW(txt):
    tok = []
    dictionary = sorted(list(set(txt)));
    current_pos = 0
    b = False
    while current_pos < len(txt):
        if b:
          break
        pointer = dictionary.index(txt[current_pos])
        pos = current_pos+1
        b = True
        while b and pos < len(txt):
            b = False
            for i,x in enumerate(dictionary):
                if x == txt[current_pos:pos+1]:
                    pointer = i
                    b = True
                    break
            pos += 1
        tok.append(pointer)
        dictionary.append(txt[current_pos:pos])
        if current_pos == len(txt)-1:
            current_pos = pos
        else:
            current_pos = pos-1
    return tok

def encode_burrows_wheeler(txt):
    n = len(txt)
    m = sorted([txt[i:n]+txt[0:i] for i in range(n)])
    cod = ''.join([q[-1] for q in m])
    i = m.index(txt)
    return cod,i

def encode_move_to_front(txt):
  alf = sorted(list(set(txt)));
  cod = []
  for c in txt:
    ind = alf.index(c)
    cod.append(ind)
    alf.insert(0,alf.pop(ind))
  return cod