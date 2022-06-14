"""Trabalho de Compiladores I

Grupo:
    Carlos Gabriel
    Isaque Almeida
    Luis Fernando
    Marcus Vinicius

Enunciado:
O controle numérico computadorizado (CNC) é sistema que automatiza o controle de centros de usinagem nas
indústrias, fazendo o controle simultâneo de vários eixos, através de um programa em uma linguagem
padronizada pela norma ISO 6983, como no exemplo a seguir:
    O0073
    N10G17G21G90G95
    N20T02
    N30M06
    N40G54S30M03
    N50G00X17Y20
    N60G43J02Z10
    N70G98G73Z85R02K10F03
    N80G49G80
    N90M30

**** Na entrada acima o "R" deve ser substituido por um "T"

Considere a seguinte gramática para as operações:
1. G = (Vn, Vt, S, P)
1. Vn = {<prga>,<nprg>,<blco>,<nblc>,<plva>,<endo>,<nmro>,<rtlo>}
2. Vt = {O,N,G,X,Y,Z,A,B,C,I,J,K,T,S,F,M,0,1,2,3,4,5,6,7,8,9}
3. S = <prga>
4. P = { <prga>::=<nprg><blco>+
         <nprg>::=O<rtlo>
         <blco>::=<nblc><plva>+
         <nblc>>::=N<rtlo>
         <plva>::=<endo><nmro><nmro>
         <rtlo>::=<nmro>+
         <endo>::= G|X|Y|Z|A|B|C|I|J|K|T|S|F|M
         <nmro>::=(0|1|2|3|4|5|6|7|8|9)
        }
"""
import sys
from dataclasses import dataclass
from typing import List, Dict, Union, TextIO
from datetime import datetime

@dataclass
class Production:
    """Classe usada para representar uma produção da gramática

    @left: Sendo o cabo da produção
    @right: Todas as produções do respectivo não terminal
    @rules: As regras deste não terminal baseado na tabela parser
    """
    left: str
    right: List
    rules: Dict

    def get_total_productions(self) -> int:
        """Retorna a quantidade de produções possiveis do não terminal"""
        return int(len(self.right))

    def get_rule(self, inp: str) -> Union[List, bool]:
        """Retorna uma regra caso exista"""
        try:
            return [self.rules[inp], f"{self.left} -> {self.rules[inp]}"]
        except KeyError:
            return False
    
    def rule_exists(self, inp: str) -> bool:
        """Verifica se uma determinada produção existe nas regras do não terminal"""
        try:
            tmp = [self.rules[inp], f"{self.left} -> {self.rules[inp]}"]
            return True
        except KeyError:
            return False

class Table:
    """Funciona como uma tabela parser

    @productions: Todas as produções da gramática, incluindo suas produções no first e no follow
    """
    def __init__(self) -> None:
        self.productions: Dict = {}
    
    def find_production(self, left: str) -> Dict:
        """Retorna uma determinada produção baseada no cabo"""
        return self.productions.get(left)
    
    def find_rule(self, stack_top: str, sentence_top: str) -> Union[List, bool]:
        """Retorna uma produção caso exista, se não existir retorna falso.
        """
        try:
            return self.productions.get(stack_top).get_rule(sentence_top)
        except AttributeError:
            return False
    
    def rule_exists(self, stack_top: str, sentence_top: str) -> bool:
        """Verifica se uma determinada produção existe na tabela"""
        try:
            return self.productions.get(stack_top).rule_exists(sentence_top)
        except AttributeError:
            return False

    def insert(self, left: str, right: List, rules: Dict):
        """Insere uma nova produção na tabela parser"""
        local_rules = {}
        
        for key in rules:
            local_rules[key] = right[rules[key]]
        
        tmp = Production(left, right, local_rules)

        self.productions[left] = tmp


"""
Gramática utilizada, (Foi necessario fazer modificações na gramática do trabalho), os não terminais foram renomeados
para facilitar a compreensão.
    s -> ca
    a -> da | ε
    c -> Oi | ε
    d -> ge | ε
    e -> hf | ε
    g -> Ni
    h -> kll | ε
    i -> lj | ε
    k -> G | X | Y | Z | A | B | C | I | J | K | T | S | F | M
    l -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | ε
    b -> a | ε
    f -> e | ε
    j -> i | ε
"""

"""Explicação do sistema de tabela parser usado neste trabalho

Exemplo: table.insert("a", ["da", "\\epsilon"], {"N": 0, "$": 1})

No terceiro parâmetro encontramos um dicionário, {"N": 0, "$": 1}, ele indica quais produções existem na tabela parser

Por exemplo, nesta linha Quando o não terminal "a" receber na entrada um "N" ele irá produzir a produção na posição "0", logo
Se "a" está na pilha e encontra um "N" na sentença ele produz "da" ( a -> da )
Já se ele encontrar um "$" na sentença ele iraá produzir a produção de numero "1" que neste caso é ( a -> ε )
"""
table = Table()
table.insert("s", ["ca"], {"O": 0})
table.insert("a", ["da", "\\epsilon"], {"N": 0, "$": 1})
table.insert("b", ["a", "\\epsilon"], {"N": 0, "$": 1})
table.insert("c", ["Oi", "\\epsilon"], {"O": 0, "$": 1})
table.insert("d", ["ge", "\\epsilon"], {"N": 0, "$": 1})
table.insert("e", ["hf", "\\epsilon"], {"G": 0, "X": 0, "Y": 0, "Z": 0, "A": 0, "B": 0, "C": 0, "I": 0, "J": 0, "K": 0, "T": 0, "S": 0, "F": 0, "M": 0, "$": 1})
table.insert("f", ["e", "\\epsilon"], {"G": 0, "X": 0, "Y": 0, "Z": 0, "A": 0, "B": 0, "C": 0, "I": 0, "J": 0, "K": 0, "T": 0, "S": 0, "F": 0, "M": 0, "N": 1, "$": 1})
table.insert("g", ["Ni"], {"N": 0})
table.insert("h", ["kll", "\\epsilon"], {"G": 0, "X": 0, "Y": 0, "Z": 0, "A": 0, "B": 0, "C": 0, "I": 0, "J": 0, "K": 0, "T": 0, "S": 0, "F": 0, "M": 0, "$": 1})
table.insert("i", ["lj", "\\epsilon"], {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "$": 1})
table.insert("j", ["i", "\\epsilon"], {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "G": 1, "X": 1, "Y": 1, "Z": 1, "A": 1, "B": 1, "C": 1, "I": 1, "J": 1, "K": 1, "T": 1, "S": 1, "F": 1, "M": 1, "O": 1, "N": 1, "$": 1})
table.insert("k", ["G", "X", "Y", "Z", "A", "B", "C", "I", "J", "K", "T", "S", "F", "M"], {"G": 0, "X": 1, "Y": 2, "Z": 3, "A": 4, "B": 5, "C": 6, "I": 7, "J": 8, "K": 9, "T": 10, "S": 11, "F": 12, "M": 13})
table.insert("l", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "\\epsilon"], {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "$": 10})

class Stack:
    """Cria um pilha que funciona da mesma forma que sua representação
    visual, o item mais recente a esquerda.

    @__stack: Pilha a ser representada
    @split: Serve para separar a entrada para simbolos compostos e unicos. Exemplo:
        Digamos que na gramática tenha o terminal "id", ele será posto na pilha como "i", e "d" separados,
        impedindo o programa de identificar que é um terminal válido, com essa opção ele deixa os terminais
        compostos juntos, permitindo a identificação do mesmo
    @Vt: Recebe a lista de todos os terminais da grámatica
    """
    def __init__(self) -> None:
        self.__stack: List = ['$']
        self.split: bool = False
        self.Vt: List = []
    
    def __repr__(self) -> str:
        return ''.join(self.__stack)
    
    def __len__(self) -> int:
        return len(self.__stack)
    
    def insert_array(self, array: List) -> None:
        """Passa um vetor para dentro da stack"""
        for item in array:
            self.push(item)

    def push(self, item: any) -> None:
        """Insere algo no topo da pilha"""
        if self.split:
            if item in self.Vt:
                self.__stack.insert(0, str(item))
            else:
                for it in list(item)[::-1]:
                    self.__stack.insert(0, str(it))
        else:
            self.__stack.insert(-1, str(item))
    
    def top(self) -> str:
        """Retorna o item no topo da pilha"""
        return str(self.__stack[0])

    def pop(self, how_many: int = 1) -> None:
        """Remove um item do topo da pilha
        @how_many: Quantidade de itens a serem removidos da pilha, por padrão é apenas 1
        """
        assert isinstance(how_many, int)
        if how_many == 1:
            self.__stack.pop(0)
        else:
            self.__stack = self.__stack[how_many:]

class LL1:
    def __init__(self, file_path: str, parse_table: Table, Vt: List, epsilon_symbol: bool, start_symbol: str, output_to_file: bool = False, output_file_type: str = "csv", output_header: bool = True) -> None:
        """Parser LL1, analisa a entrada e verifica se é aceita pela gramática

        @input: Conteúdo do arquivo a ser testado, convertido em uma string
        @sentence: Conteúdo do arquivo separado em uma stack
        @file_path: Caminho para o arquivo que contém o texto que será analisado
        @stack: Pilha principal do parser
        @Vt: Conjunto de terminais da gramática
        @epsilon_symbol: Opção para inserir o simbolo do Epsilon ou o "\\epsilon" na saida do programa para terminais-de-comando que não
            aceitam UTF-8
        @rule: Guarda a regra da linha atual do programa
        @parse_table: Recebe a tabela parser
        @start_symbol: Simbolo inicial da gramática
        @sentence_size: Tamanho da sentença, usado para formatar a saida do programa
        @history: Guarda todas as iterações do programa
        @output_to_file: Opção que controla a criação de um arquivo com o o resultado do programa, o padrão é True
        @output_file_type: Tipo de arquivo que será criado com o resultado final. Duas opções "csv" ou "txt", o padrão é "csv"
        @output_header: Opção para inserir no arquivo final os headers ("Pilha, sentença, regra"), o padrão é True
        """
        self.input: str = ""
        self.sentence: Stack = None
        self.file_path: str = file_path
        self.stack: Stack = Stack()
        self.stack.split = True
        self.Vt: List = Vt
        self.epsilon_symbol: bool = epsilon_symbol
        self.stack.Vt = self.Vt
        self.rule: str = None
        self.parse_table: Table = parse_table
        self.start_symbol: str = start_symbol
        self.sentence_size: int = None
        self.history: List = []
        self.output_to_file: bool = output_to_file
        self.output_file_type: str = output_file_type
        self.output_header: bool = output_header

    def analyze(self) -> str:
        """Inicia o parser LL1"""
        self.read_file()
        self.input_to_stack()
        self.parser()
        if self.output_to_file:
            wf = WriteFile(self.history, self.output_file_type, self.output_header)
            wf.write_csv()

    def input_to_stack(self) -> None:
        """Passa um vetor normal para uma stack"""
        tmp_stack = Stack()
        tmp_stack.insert_array(self.input)
        self.sentence = tmp_stack

    def print_line(self, header: bool = False) -> None:
        """Imprime um linha do parser no terminal
        
        @header: Opção para imprimir uma linha com os headers ("Pilha, sentença, regra"), o padrão é False.
        """
        if header:
            self.history.append(["Pilha", "Sentença", "Regra"]) if self.output_to_file else None
            print('|{0: >{stacksize}} | {1: >{sentencesize}} | {2: >{rulesize}} |'
            .format("Pilha", "Sentença", "Regra", stacksize=15, sentencesize=self.sentence_size, rulesize=8))
        else:
            self.history.append([str(self.stack), str(self.sentence), self.rule]) if self.output_to_file else None
            print('|{0: >{stacksize}} | {1: >{sentencesize}} | {2: >{rulesize}} |'
            .format(str(self.stack), str(self.sentence), self.rule, stacksize=15, sentencesize=self.sentence_size, rulesize=8))

    def parser(self) -> None:
        """Analisa a sentença"""
        self.print_line(header=True)
        self.stack.push(self.start_symbol)

        # Enquanto existir algo na Pilha
        while (len(self.stack) > 0):
            # Verifica se o topo da pilha e o topo da sentença são finais de sentença
            # Condição unica para a gramática ser aceita!
            if self.stack.top() == "$" and self.sentence.top() == "$":
                self.rule = "OK"
                self.print_line()
                print("\nA gramática FOI aceita!")
                break
            
            # Verifica se o topo da pilha e o topo da sentença fazem parte do conjunto de terminais
            # Se sim, removem o terminal correspondente de ambos
            if self.stack.top() in self.Vt and self.sentence.top() in self.Vt:
                self.rule = f"pop({self.stack.top()})"
                self.print_line()
                self.stack.pop()
                self.sentence.pop()
                continue
            
            # Verifica se existe a regra para o topo da pilha referente ao topo da sentença
            if self.parse_table.rule_exists(self.stack.top(), self.sentence.top()):
                tmp = self.parse_table.find_rule(self.stack.top(), self.sentence.top())

                # Se a produção existir e produzir vazio, remove o topo da pilha
                if tmp[0] == "\\epsilon":
                    if self.epsilon_symbol:
                        tmp_1 = tmp[1].split()
                        self.rule = f"{tmp_1[0]} {tmp_1[1]} ε"
                    else:
                        self.rule = tmp[1]
                    self.print_line()
                    self.stack.pop()
                    self.rule = ""
                    continue

                # Se a produção gerar outra produção que não seja um terminal, adiciona a pilha tal produção
                self.rule = tmp[1]
                self.print_line()
                self.stack.pop()
                self.stack.push(tmp[0])
                self.rule = ""
            else:
                # Se as condições acima não forem supridas, a sentença não foi aceita pela gramática
                self.rule = "ERRO"
                self.print_line()
                print("\nA gramática NÃO foi aceita!")

                # Informa qual foi a produção que gerou o erro
                print(f"NÃO há produção de: {self.stack.top()} -> {self.sentence.top()}")
                break

    def read_file(self) -> None:
        """Lê o arquivo com a sentença à ser testada"""
        try:
            f = open(self.file_path)
        except FileNotFoundError:
            print("ERRO (1): ARQUIVO NÃO ENCONTRADO!")
            quit(1)

        self.input = list(''.join(f.read().splitlines()))
        self.sentence_size = len(self.input) + 2


class WriteFile:
    def __init__(self, data: Union[str, List], output_file_type: str = "csv", header: bool = True) -> None:
        """Classe responsável por receber os resultados e persistirem os mesmos em arquivos
        
        @data: Dados dos resultados da gramática
        @output_file_type: Tipo de arquivo que será criado com o resultado final. Duas opções "csv" ou "txt", o padrão é "csv"
        @header: Opção para inserir no arquivo final os headers ("Pilha, sentença, regra"), o padrão é True
        """
        self.output_file_type: str = output_file_type
        self.data: Union[str, List] = data
        self.header: bool = header
    
    def write_csv(self) -> TextIO:
        if not self.output_file_type in ["csv", "txt"]:
            print("ERRO: Tipo de saida de arquivo inválida!")
            quit(1)

        now = datetime.now()
        date = now.strftime("%m-%d-%YT%H-%M-%S")

        with open(f"RESULTADO-{date}.{self.output_file_type}", "w", encoding="utf-8") as f:
            if self.header:
                self.data = self.data[1:]
            for line in self.data:
                tmp = []
                for item in line:
                    if self.output_file_type == "csv":
                        tmp.append(f'\"{item}\"')
                    else:
                        tmp.append(f'{item}')
                f.write(', '.join(tmp) + '\n')
        
        print(f"Um arquivo foi criado com o resultado da grámatica! -> RESULTADO-{date}.{self.output_file_type}")

if __name__ == "__main__":
    """ || Configuração do Programa || """
    # Terminais da gramática
    Vt = ["G", "X", "Y", "Z", "A", "B", "C", "I", "J", "K", "T", "S", "F", "M", "O", "N", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    # Simbolo inicial da gramática
    start_symbol = "s"
    # Gerar o simbolo epsilon na saida do programa
    epsilon_symbol = True
    # Caminho para o arquivo de entrada
    # A entrada foi modificada, sendo alterado o "R" para um "T"
    file_path = "./entrada.txt"
    # Tabela parser
    parse_table = table

    # Gerar um arquivo com os resultados
    output_to_file = True
    # Tipo do arquivo à ser gerado
    output_file_type = "csv"
    # Gerar o header no arquivo
    output_header = True
    """ ||--------------------------|| """

    # Parser
    ll1 = LL1(file_path, parse_table, Vt, epsilon_symbol, start_symbol, output_to_file, output_file_type, output_header)
    ll1.analyze()