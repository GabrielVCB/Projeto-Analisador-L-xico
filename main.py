import re

# Definindo as expressões regulares para cada tipo de token
alfabeto = [
    ("NUM_INT", r'\b\d+\b'),
    ("NUM_DEC", r'\b\d+\.\d+\b'),
    ("ID", r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ("TEXTO", r'"[^"]*"'),
    ("PALAVRA_RESERVADA", r'\b(public|class|static|void|int|System|out|print)\b'),
    ("OPERADOR", r'[+\-*/%=]|&&|\|\||!|==|!=|<=|>=|<|>'),
    ("SIMBOLO_ESPECIAL", r'[()[\]{};,.]')
]

# Tabela de símbolos
tabela_simbolos = {}

# Função para analisar o código fonte
def analisar_codigo(codigo):
    tokens = []
    pos_id = 1

    # Loop para percorrer o código fonte
    while codigo:
        codigo = codigo.strip()

        # Verificar se há correspondência com algum padrão
        match = None
        for token_type, pattern in sorted(alfabeto, key=lambda x: -len(x[1])):
            regex = re.compile('^' + pattern)
            match = regex.match(codigo)
            if match:
                valor = match.group(0)
                if token_type == 'ID':
                    if valor not in tabela_simbolos:
                        tabela_simbolos[valor] = pos_id
                        pos_id += 1
                    tokens.append((token_type, valor, tabela_simbolos[valor]))
                else:
                    tokens.append((token_type, valor))
                codigo = codigo[match.end():]
                break

        # Se não houver correspondência, gerar erro
        if not match:
            raise Exception(f"Erro: Token inválido - {codigo.split()[0]}")

    return tokens

# Testando o analisador léxico com um código fonte de exemplo
codigo_fonte = '''
public static void main(String[]args) {
        int a = 3, b = 2;
        int c = a * b; 
        System.out.print(c);
}

'''

try:
    tokens = analisar_codigo(codigo_fonte)
    for token in tokens:
        print(token)
except Exception as e:
    print(e)
