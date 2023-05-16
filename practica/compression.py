{"nbformat":4,"nbformat_minor":0,"metadata":{"colab":{"provenance":[],"authorship_tag":"ABX9TyMrw2bNm9r3rLBZtEX+XVmT"},"kernelspec":{"name":"python3","display_name":"Python 3"},"language_info":{"name":"python"}},"cells":[{"cell_type":"code","execution_count":null,"metadata":{"id":"2lVnDWfjdjsc"},"outputs":[],"source":["from math import floor\n","\n","def arithmetic_encode(txt,k,src):#hay q implementar lo de block size, es decir si la longitud de las letras de src\n","    block_size = len(src[0][0])\n","    suma = 0\n","    src2 = []\n","    for i in range(len(src)):\n","        suma += src[i][1]\n","    for i in range(len(src)):\n","        src2.append((src[i][0],src[i][1]/suma))\n","    alpha = '0' * k\n","    beta = '1' * k\n","    c = \"\"\n","    u = 0\n","    cumulative_probs = [0]\n","    aux = 0.0\n","    for i in range(len(src2)):\n","        aux += src2[i][1]\n","        cumulative_probs.append(aux)\n","    #for i in range(len(txt)):\n","    while txt:\n","        block = txt[:block_size]# q bueno soy hermano\n","        delta = int(beta,2) - int(alpha,2) + 1\n","        subintervals = []\n","        for j in range(1, len(cumulative_probs)):\n","            aux = (int(alpha,2) + int(floor(delta * cumulative_probs[j-1])),\n","                   int(alpha,2) + int(floor(delta * cumulative_probs[j]) - 1))\n","            subintervals.append(aux)\n","        ind = [src2.index(tupla) for tupla in src2 if tupla[0] == block][0]#solo se usa i aqui, en txt[i]\n","        alpha = bin(subintervals[ind][0])[2:].zfill(k)\n","        beta = bin(subintervals[ind][1])[2:].zfill(k)\n","        while alpha[0] == beta[0]:\n","            c += alpha[0]\n","            if alpha[0] == '0':\n","                    c += '1' * u\n","            else:\n","                    c += '0' * u\n","            u = 0\n","            alpha = alpha[1:] + '0'\n","            beta = beta[1:] + '1'\n","        while alpha[:2] == '01' and beta[:2] == '10':\n","            alpha = alpha[0] + alpha[2:] + '0'\n","            beta = beta[0] + beta[2:] + '1'\n","            u += 1\n","        txt = txt[block_size:]\n","    return c + '1'\n","\n","def source_fromtext(txt):\n","    x = []\n","    for l in set(txt):\n","        n = txt.count(l)\n","        x.append((l,n))\n","    x.sort(key=lambda x: x[0])\n","    return x"]},{"cell_type":"code","source":["class Node:\n","    def __init__(self, weight, sym, left=None, right=None):\n","        self.weight = weight\n","        self.sym = sym\n","        self.left = left\n","        self.right = right\n","        self.code = \"\"#0 o 1, depende de la dirección\n","\n","def huffman_code(txt):\n","    total = 0\n","    src = source_fromtext(txt)\n","    for _, w in src:\n","        total += w#lo quito?\n","    src.sort(key=lambda x: x[1])\n","    #no se como hacer lo de los nodos la vd q coñazo, ademas hay q hacer un insert con selection PQ EL BISECT NO VA\n","    huff_tree = []\n","    for a, w in src:\n","      node = Node(w, a)\n","      huff_tree.append(node)\n","    while len(huff_tree) > 1:\n","      node1 = huff_tree[0]; node2 = huff_tree[1]\n","      huff_tree.remove(node1); huff_tree.remove(node2)\n","      weight = node1.weight + node2.weight\n","      sym = node1.sym + node2.sym\n","      left = node1\n","      right = node2\n","      node1.code = \"0\"\n","      node2.code = \"1\"\n","      node = Node(weight, sym, left, right)\n","      index = len(huff_tree)\n","      for i in range(0, len(huff_tree)):\n","          if huff_tree[i].weight >= weight:\n","              index = i\n","              break\n","      huff_tree.insert(index, node)\n","    huff_dict = calculate_codes(huff_tree[0])\n","    huff_code = [(k, v) for k, v in huff_dict.items()]#hay q pasarlo a lista para el output\n","    huff_code.sort(key=lambda x:x[0])#NECESARIO esto, para ordenarlo PRIMERO alfabéticamente...\n","    huff_code.sort(key=lambda x:len(x[1]))#... y luego para ordenarlos segun longitud respetando el orden alfabético\n","    #falta canonizar\n","    huff_lens = [len(x[1]) for x in huff_code] #longitudes de cada letra codificada en huffman\n","    huff_canon = canonize(huff_lens)\n","    letters = [x[0] for x in huff_code]\n","    huffman = list(zip(letters,huff_canon))\n","    huffman.sort(key = lambda x:x[0])\n","\n","    return huffman\n","\n","def canonize(lens):\n","  first = \"\"\n","  for i in range(0,lens[0]):\n","    first += \"0\"\n","  canonized = []\n","  canonized.append(first)\n","  last_len = lens[0]\n","  last_code = first\n","  del lens[0]\n","  for x in lens:\n","    code = increment_alf(last_code)\n","    n_appends = x-last_len\n","    for i in range(0,n_appends):\n","      code += \"0\"\n","    last_code = code\n","    last_len = x\n","    canonized.append(code)\n","  return canonized\n","\n","def increment_alf(codeword,alf = [\"0\",\"1\"]):#para sumar en binario\n","#     if codeword == None: esto nunca deberia suceder, hay un error\n","#         codeword = \"\" #es q si no se bugea lol\n","    carry = False\n","    s = list(codeword)\n","    i = len(codeword)-1\n","    if s[i] != alf[-1]:\n","        index_in_alf = alf.index(s[i])\n","        s[i] = alf[index_in_alf+1]\n","    else:\n","        s[i] = alf[0]\n","        carry = True\n","    \n","    if carry:\n","        while True:\n","            i -= 1\n","            #if i < 0: #esto es necesario? no sabria decirte\n","                #raise ValueError(\"ERROR: no existeix cap codi amb aquesta propietat\")\n","            if s[i] != alf[-1]:\n","                index_in_alf = alf.index(s[i])\n","                s[i] = alf[index_in_alf+1]\n","                break\n","            else:\n","                s[i] = alf[0]\n","    codeword = \"\".join(s) #convertimos la lista en string\n","    return codeword #GILIPOLLAS\n","\n","def calculate_codes(node, value = \"\"):#en vd creo q esto es INUTIL de cojones pq solo necesito las longitudes de cada letra y no el codigo entero, pero bueno, al menos lo tengo hecho por si aca\n","  codes = {}\n","  newValue = value + str(node.code)\n","  if(node.left): calculate_codes(node.left, newValue)\n","  if(node.right): calculate_codes(node.right, newValue)\n","  if(not node.left and not node.right): codes[node.sym] = newValue\n","  return codes\n","\n","def encode(txta,corr):\n","#     txt = txta.split() #suponemos q son palabras separadas por espacios\n","#pues no son palabras SON LETRAS JAJJSKDJD TUS MUERTOS\n","    coded = []\n","    for c in txta:\n","        for x in corr:\n","            if c in x[0]:\n","                coded.append(x[1])\n","    txtb = \"\".join(coded)\n","    return txtb"],"metadata":{"id":"qPyWSaCSkogO"},"execution_count":null,"outputs":[]},{"cell_type":"code","source":["def encode_LZ77(txt,s,t):\n","    tok = []\n","    tok.append((1, 0, txt[0]))\n","    current_pos = 1\n","    search = txt[0]\n","    lookahead = txt[1:1+t]\n","    while current_pos < len(txt):\n","        offset = 1\n","        length = 0\n","        char = lookahead[0]\n","        window = search + lookahead\n","        for i in range(len(search)-1, -1, -1):\n","            if search[i] == lookahead[0]:\n","                match = True\n","                iwind = i+1\n","                jwind = len(search)+1\n","                maxlen = 1\n","                while match and jwind < len(window):\n","                    if window[iwind] == window[jwind]:\n","                       maxlen += 1\n","                       iwind += 1\n","                       jwind += 1\n","                    else:\n","                        match = False\n","                if (maxlen > length):\n","                    if (current_pos+length+1 >= len(txt)):\n","                       break\n","                    offset = len(search)-i\n","                    length = maxlen\n","                    try:\n","                        char = window[jwind]\n","                    except:\n","                         try:\n","                             char = txt[current_pos+length]\n","                         except:\n","                              char = window[jwind-1]\n","                              length -= 1\n","                              if (length == 0):\n","                                  offset = 1\n","        tok.append((offset, length, char))\n","        current_pos += length+1\n","        if (current_pos-s < 0):\n","            search = txt[0:current_pos]\n","        else:\n","            search = txt[current_pos-s:current_pos]\n","        lookahead = txt[current_pos:current_pos+t]\n","    return tok\n","\n","def encode_LZSS(txt,mm,s,t):\n","    tok = []\n","    tok.append(txt[0])\n","    current_pos = 1\n","    search = txt[0]\n","    lookahead = txt[1:1+t]\n","    while current_pos < len(txt):\n","        offset = 1\n","        length = 0\n","        window = search + lookahead\n","        for i in range(len(search)-1, -1, -1):\n","            if search[i] == lookahead[0]:\n","                match = True\n","                iwind = i+1\n","                jwind = len(search)+1\n","                maxlen = 1\n","                while match and jwind < len(window):\n","                    if window[iwind] == window[jwind]:\n","                       maxlen += 1\n","                       iwind += 1\n","                       jwind += 1\n","                    else:\n","                        match = False\n","                if (maxlen > length):\n","                    offset = len(search)-i\n","                    length = maxlen\n","        if length < mm:\n","            tok.append(lookahead[0])\n","            current_pos += 1\n","        else:\n","            tok.append((offset,length))\n","            current_pos += length\n","        if (current_pos-s < 0):\n","            search = txt[0:current_pos]\n","        else:\n","            search = txt[current_pos-s:current_pos]\n","        lookahead = txt[current_pos:current_pos+t]\n","    return tok\n","\n","def encode_LZ78(txt):\n","    tok = []\n","    tok.append((0, txt[0]))\n","    dictionary = ['', txt[0]]\n","    current_pos = 1\n","    while current_pos < len(txt):\n","        pointer = ''\n","        if current_pos == len(txt)-1:\n","          tok.append((0, txt[current_pos]))\n","          break\n","        for i,x in enumerate(dictionary):\n","            if x == txt[current_pos]:\n","                pointer = i\n","                break\n","        if not pointer:\n","            tok.append((0, txt[current_pos]))\n","            dictionary.append(txt[current_pos])\n","            current_pos += 1\n","        else: \n","            pos = current_pos+1\n","            b = True\n","            while b and pos < len(txt):\n","                if(pos == len(txt)-1):\n","                  b = True\n","                  pos += 1\n","                  break\n","                b = False\n","                for i,x in enumerate(dictionary):\n","                    if x == txt[current_pos:pos+1]:\n","                        pointer = i\n","                        b = True\n","                        break\n","                pos += 1\n","            if b and pos == len(txt):\n","                tok.append((pointer, txt[pos-1]))\n","            else:\n","                tok.append((pointer, txt[pos-1]))\n","            dictionary.append(txt[current_pos:pos])\n","            current_pos = pos\n","    return tok\n","\n","def encode_LZW(txt):\n","    tok = []\n","    dictionary = sorted(list(set(txt)));\n","    current_pos = 0\n","    b = False\n","    while current_pos < len(txt):\n","        if b:\n","          break\n","        pointer = dictionary.index(txt[current_pos])\n","        pos = current_pos+1\n","        b = True\n","        while b and pos < len(txt):\n","            b = False\n","            for i,x in enumerate(dictionary):\n","                if x == txt[current_pos:pos+1]:\n","                    pointer = i\n","                    b = True\n","                    break\n","            pos += 1\n","        tok.append(pointer)\n","        dictionary.append(txt[current_pos:pos])\n","        if current_pos == len(txt)-1:\n","            current_pos = pos\n","        else:\n","            current_pos = pos-1\n","    return tok\n","\n","def encode_burrows_wheeler(txt):\n","    n = len(txt)\n","    m = sorted([txt[i:n]+txt[0:i] for i in range(n)])\n","    cod = ''.join([q[-1] for q in m])\n","    i = m.index(txt)\n","    return cod,i\n","\n","def encode_move_to_front(txt):\n","  alf = sorted(list(set(txt)));\n","  cod = []\n","  for c in txt:\n","    ind = alf.index(c)\n","    cod.append(ind)\n","    alf.insert(0,alf.pop(ind))\n","  return cod"],"metadata":{"id":"JynWEyP2uxvg"},"execution_count":null,"outputs":[]}]}