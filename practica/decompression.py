# -*- coding: utf-8 -*-
"""decompression.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FU_NV6mhdRd6Za7lNCppdS1QKB7uzZi7
"""

from math import floor
def arithmetic_decode(code,k,src,l): #supongo q tambien tendré q hacer lo de blocksize
    block_size = len(src[0][0])
    suma = 0
    src2 = []
    for i in range(len(src)):
        suma += src[i][1]
    for i in range(len(src)):
        src2.append((src[i][0],src[i][1]/suma))
    alpha = '0' * k
    beta = '1' * k
    gamma = code[:k]
    usados = k
    x = ''
    cumulative_probs = [0]
    aux = 0.0
    for i in range(len(src2)):
        aux += src2[i][1]
        cumulative_probs.append(aux)
    while len(x) != l:
        delta = int(beta,2) - int(alpha,2) + 1
        subintervals = []
        for j in range(1, len(cumulative_probs)):
            aux = (int(alpha,2) + int(floor(delta * cumulative_probs[j-1])),
                   int(alpha,2) + int(floor(delta * cumulative_probs[j]) - 1))
            subintervals.append(aux)
        for ind, subint in enumerate(subintervals):
            if subint[0] <= int(gamma,2) <= subint[1]:
                x += src2[ind][0]
                alpha = bin(subint[0])[2:].zfill(k)
                beta = bin(subint[1])[2:].zfill(k)
        if len(x) == l:
            break
        while alpha[0] == beta[0]:
            alpha = alpha[1:] + '0'
            beta = beta[1:] + '1'
            if usados == len(code):
                gamma = gamma[1:] + '0'
            else:
                gamma = gamma[1:] + code[usados]
                usados += 1
        while alpha[:2] == '01' and beta[:2] == '10':
            alpha = alpha[0] + alpha[2:] + '0'
            beta = beta[0] + beta[2:] + '1'
            if usados == len(code):
                gamma = gamma[0] + gamma[2:] + '0'
            else:
                gamma = gamma[0] + gamma[2:] + code[usados]
                usados += 1
    return x

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

def decode(txtb,corr):
#     txt = txtb.split() vale no está separado, mira pregunta 6
#     decoded = []
#     for c in txt:
#         for x in corr:
#             if c in x[1]:
#                 decoded.append(x[0])
#     txta = " ".join(decoded)
#     return txta
    i = 0
    txta = ""
    chain = ""
    while i < len(txtb):
        chain += txtb[i]
        for p in corr:
            if chain == p[1]:
                txta += p[0]
                chain = ""
                break
        i += 1
    return txta

def decode_LZ77(tok):
    txt = ''
    for offset, length, char in tok:
        if offset == 1 and length == 0:
            txt += char
        else:
            for i in range(length):
                txt += txt[-offset]
            txt += char
    return txt

def decode_LZSS(tok):
    txt = ''
    for token in tok:
        if type(token) != tuple:
            txt += token
        else:
            for i in range(token[1]):
                txt += txt[-token[0]]
    return txt

def decode_LZ78(tok):
    txt = ''
    dictionary = ['']
    for token in tok:
        txt += dictionary[token[0]] + token[1]
        dictionary.append(dictionary[token[0]] + token[1])
    return txt

def decode_LZW(tok,alp):
  dictionary = alp
  txt = ""
  last_sym = ""
  sym = ""
  first = True
  for ind in tok:
    sym = dictionary[ind]
    if(not first):
      dictionary[-1] += sym[0]
      if ind == len(dictionary) - 1:
        sym = dictionary[ind]#da igual poner ind q -1
    else:
      first = False
    txt += sym
    dictionary.append(sym)
  return txt

from operator import itemgetter
def decode_burrows_wheeler(cod,i):
    n = len(cod)
    X = sorted([(j, x) for j, x in enumerate(cod)], key=itemgetter(1))

    T = [None for j in range(n)]
    for j, y in enumerate(X):
        k, _ = y
        T[k] = j

    Tx = [i]
    for j in range(1, n):
        Tx.append(T[Tx[j-1]])

    S = [cod[j] for j in Tx]
    S.reverse()
    return ''.join(S)

def decode_move_to_front(cod,alf):
  txt = ""
  for i in cod:
    c = alf[i]
    txt += c
    alf.insert(0,alf.pop(i))
  return txt