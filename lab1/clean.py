import sys
from unidecode import unidecode

def clean_text(txt):
    clean = ''.join(x for x in txt if x.isalpha() or x.isspace()) #deja solo letras y espacios
    clean = clean.lower() #en minúsculas
    clean = unidecode(clean) #quita acentos
    clean = ' '.join(clean.split()) #solo un espacio
    return clean

def main():
    x = sys.argv[1]
    path_file = './textos/' + x + '.txt'
    with open(path_file, 'r') as file:
        text = file.read()
    text_clean = clean_text(text)
    path_clean_file = x + '_clean.txt'
    with open(path_clean_file, 'w') as file:
        file.write(text_clean)


if __name__ == "__main__":
    main()