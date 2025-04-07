from vars import *

class Piece:
    """
    Representa uma peça do jogo de damas (Dameo).

    Contém informações sobre a sua posição, cor,
    se é uma dama, e os seus movimentos legais.
    """

    def __init__(self, size, row, col, color, king = False):
        """
        Inicializa uma peça.

        Args:
            size (int): O tamanho do tabuleiro.
            row (int): A linha da posição da peça.
            col (int): A coluna da posição da peça.
            color (tuple): A cor da peça (WHITE ou BLACK).
            king (bool): True se a peça é uma dama, False caso contrário.
        """
        self.size = size
        self.row = row
        self.col = col
        self.color = color
        self.king = king
        self.legal = []  # Lista de movimentos legais para a peça
        self.right = size - 1 - self.col  # Espaço livre à direita da peça
        self.down = size - 1 - self.row  # Espaço livre abaixo da peça
        self.catch = False  # Flag para indicar se a peça pode capturar outra peça
        self.previous_position = ()  # Posição anterior da peça
        self.has_caught = False  # Flag para indicar se a peça já capturou outra peça


    def move(self, row, col, board):
        """
        Move a peça para uma nova posição.

        Args:
            row (int): A nova linha da posição da peça.
            col (int): A nova coluna da posição da peça.
            board (Board): O tabuleiro do jogo.
        """
        self.previous_position = (self.row, self.col)  # Guarda a posição anterior da peça
        self.row = row  # Atualiza a linha da posição da peça
        self.col = col  # Atualiza a coluna da posição da peça
        self.right = self.size - 1 - col  # Recalcula o espaço livre à direita
        self.down = self.size - 1 - row  # Recalcula o espaço livre abaixo
        self.has_caught = False  # Reinicia o estado de captura

        # Elimina a peça capturada, se houver
        if (self.row == self.previous_position[0] and self.col != self.previous_position[1]) or (self.row != self.previous_position[0] and self.col == self.previous_position[1]):  # Evita esta função para movimentos diagonais (sem capturas)
            if abs(self.previous_position[0] - self.row) > 1:  # Movimento vertical maior que um quadrado
                for i in range(1, abs(self.row - self.previous_position[0])):
                    # Captura para cima
                    if self.previous_position[0] > self.row and board.chessboard[self.previous_position[0] - i][self.previous_position[1]] != None and board.chessboard[self.previous_position[0] - i][self.previous_position[1]].color != self.color:
                        board.drop_piece(self.previous_position[0] - i, self.previous_position[1])
                        board.chessboard[self.previous_position[0] - i][self.previous_position[1]] = None
                        self.has_caught = True
                    # Captura para baixo
                    if self.previous_position[0] < self.row and board.chessboard[self.previous_position[0] + i][self.previous_position[1]] != None and board.chessboard[self.previous_position[0] + i][self.previous_position[1]].color != self.color:
                        board.drop_piece(self.previous_position[0] + i, self.previous_position[1])
                        board.chessboard[self.previous_position[0] + i][self.previous_position[1]] = None
                        self.has_caught = True

            if abs(self.previous_position[1] - self.col) > 1:  # Movimento horizontal maior que um quadrado
                # Captura para a esquerda
                for i in range(1, abs(self.col - self.previous_position[1])):
                    if self.previous_position[1] > self.col and board.chessboard[self.previous_position[0]][self.previous_position[1] - i] != None and board.chessboard[self.previous_position[0]][self.previous_position[1] - i].color != self.color:
                        board.drop_piece(self.previous_position[0], self.previous_position[1] - i)
                        board.chessboard[self.previous_position[0]][self.previous_position[1] - i] = None
                        self.has_caught = True
                    # Captura para a direita
                    if self.previous_position[1] < self.col and board.chessboard[self.previous_position[0]][self.previous_position[1] + i] != None and board.chessboard[self.previous_position[0]][self.previous_position[1] + i].color != self.color:
                        board.drop_piece(self.previous_position[0], self.previous_position[1] + i)
                        board.chessboard[self.previous_position[0]][self.previous_position[1] + i] = None
                        self.has_caught = True

        board.moves_whitout_catching += 1  # Incrementa o contador de movimentos sem captura
        if self.has_caught:
            board.moves_whitout_catching = 0  # Reinicia o contador se houve captura

        board.last_moved_piece = self  # Define esta peça como a última movida
        board.last_move = (row, col)  # Define o movimento como o último movimento


    def transform_king(self):
        """Transforma a peça numa dama se ela chegar à extremidade oposta do tabuleiro."""
        if self.row == 0 and self.color == WHITE and self.king == False:
            self.king = True
        if self.row == self.size - 1 and self.color == BLACK and self.king == False:
            self.king = True


    def legal_positions(self):
        """Calcula as posições legais para a peça se mover (movimentos normais, sem captura)."""

        self.legal = []

        # Movimentos para a direita
        if self.right and self.king:
            for col in range(1, self.right + 1):
                self.legal += [(self.row, self.col + col)]

        # Movimentos para a esquerda
        if self.col and self.king:
            for col in range(1, self.col + 1):
                self.legal += [(self.row, self.col - col)]

        # Movimentos para cima
        if self.row  and not (self.color == BLACK and not self.king):
            for row in range(1, self.row + 1):
                self.legal += [(self.row - row, self.col)]

        # Movimentos para baixo
        if self.down and not (self.color == WHITE and not self.king):
            for row in range(1, self.down + 1):
                self.legal += [(self.row + row, self.col)]

        # Movimentos diagonais
            # Cima direita
        if self.row and self.right and not (self.color == BLACK and not self.king):
            for i in range(1, min(self.row, self.right) + 1):
                self.legal += [(self.row - i, self.col + i)]

            # Baixo direita
        if self.down and self.right and not (self.color == WHITE and not self.king):
            for i in range(1, min(self.down, self.right) + 1):
                self.legal += [(self.row + i, self.col + i)]

            # Cima esquerda
        if self.row and self.col and not (self.color == BLACK and not self.king):
            for i in range(1, min(self.row, self.col) + 1):
                self.legal += [(self.row - i, self.col - i)]

            # Baixo esquerda
        if self.down and self.col and not (self.color == WHITE and not self.king):
            for i in range(1, min(self.down, self.col) + 1):
                self.legal += [(self.row + i, self.col - i)]


    def check_position(self, board):
        """Verifica se as posições legais estão ocupadas e remove as posições inválidas."""
        arg_taken = []
        arg_inval = []
        inval=[]
        whites, blacks = board.occupied()
        # Remove posições ocupadas por outras peças
        op_pieces = whites + blacks

        for i in range(len(self.legal)):
            if self.legal[i] in whites or self.legal[i] in blacks:
                arg_taken.append(i)
        self.legal = [self.legal[i] for i in range(len(self.legal)) if i not in arg_taken]

        # Remove posições inválidas para peças normais (não damas)
        if self.color == BLACK and not self.king:
            # Remove posições extra para baixo
            if self.down >= 2:
                if (self.row+1, self.col) not in blacks and (self.row+1, self.col) not in whites:
                    for i in range(2, self.down+1):
                        inval+= [(self.row+i, self.col)]

                if self.down >= 3 and (self.row+1, self.col) in whites:
                    # Remove a casa três espaços abaixo até ao fim
                    for i in range(3, self.down+1):
                        inval+= [(self.row+i, self.col)]

                for j in range (3, self.size-1):
                    if self.down >= j and (self.row+1, self.col) in blacks:
                        for k in range (2, j+1):
                            if (self.row+k, self.col) not in blacks:
                             # Remove a casa k+1 espaços abaixo até ao fim
                                 for i in range(k+1, self.down+1):
                                     inval+= [(self.row+i, self.col)]

            # Remove posições em excesso diagonal direita/baixo
            for j in range (2, self.size-1):
                 if min(self.down, self.right) >= j:  # and (self.row+1, self.col+1) not in blacks:
                   for k in range (1, j+1):
                        if (self.row+k, self.col+k) not in blacks:
                            for i in range(k+1, min(self.down, self.right)+1):
                                 inval+= [(self.row+i, self.col+i)]

            # Remove posições em excesso esquerda/baixo
            for j in range (2, self.size-1):
                 if min(self.down, self.col) >= j:  # and (self.row+1, self.col+1) not in blacks:
                   for k in range (1, j+1):
                        if (self.row+k, self.col-k) not in blacks:
                            for i in range(k+1, min(self.down, self.col)+1):
                                 inval+= [(self.row+i, self.col-i)]

        if self.color == WHITE and not self.king:
            # Remove posições extra para cima
            if self.row >= 2:
                if (self.row-1, self.col) not in blacks and (self.row-1, self.col) not in whites:
                    for i in range(2, self.row+1):
                        inval += [(self.row-i, self.col)]

            if self.row >= 3 and (self.row-1, self.col) in blacks:
                # Remove posições três espaços acima até ao fim
                for i in range(3, self.row+1):
                    inval += [(self.row-i, self.col)]

            for j in range(3, self.size):
                if self.row >= j and (self.row-1, self.col) in whites:
                    for k in range(2, j):
                        if (self.row-k, self.col) not in whites:
                            # Remove posições k+1 espaços acima até ao fim
                            for i in range(k+1, self.row+1):
                                inval += [(self.row-i, self.col)]

            # Remove posições em excesso diagonal esquerda/cima
            for j in range(2, self.size-1):
                if min(self.row, self.col) >= j:
                    for k in range(1, j+1):
                        if (self.row-k, self.col-k) not in whites:
                            for i in range(k+1, min(self.row, self.col)+1):
                                inval += [(self.row-i, self.col-i)]

            # Remove posições em excesso direita/cima
            for j in range(2, self.size-1):
                if min(self.row, self.right) >= j:
                    for k in range(1, j+1):
                        if (self.row-k, self.col+k) not in whites:
                            for i in range(k+1, min(self.row, self.right)+1):
                                inval += [(self.row-i, self.col+i)]

        # Remove as posições inválidas da lista de posições legais
        for j in range(len(self.legal)):
            if self.legal[j] in inval:
                arg_inval.append(j)

        self.legal = [self.legal[j] for j in range(len(self.legal)) if j not in arg_inval]


    def no_jump(self, board):
        """Remove as posições legais onde a peça saltaria sobre outra peça."""
        to_pop = []
        whites, blacks = board.occupied()
        op_pieces = whites + blacks

        if self.king:
            for i in range(len(self.legal)):
                if self.legal[i][0] == self.row:  # Posição legal na mesma linha
                    for j in range(1, abs(self.legal[i][1] - self.col) + 1):
                        # if self.col > self.legal[i][1] and (self.row, self.col - j) in whites:  # Posição legal à esquerda
                        if self.col > self.legal[i][1] and (self.row, self.col - j) in op_pieces:  # Posição legal à esquerda
                            to_pop.append(i)
                        if self.col < self.legal[i][1] and (self.row, self.col + j) in op_pieces:  # Posição legal à direita
                            to_pop.append(i)

                elif self.legal[i][1] == self.col:  # Posição legal na mesma coluna
                    for j in range(1, abs(self.legal[i][0] - self.row) + 1):
                        if self.row > self.legal[i][0] and (self.row - j, self.col) in op_pieces:  # Posição legal para cima
                            to_pop.append(i)
                        if self.row < self.legal[i][0] and (self.row + j, self.col) in op_pieces:  # Posição legal para baixo
                            to_pop.append(i)

                else:  # Posição legal na diagonal
                    for j in range(1, abs(self.legal[i][0] - self.row)):
                        if self.row > self.legal[i][0] and self.col > self.legal[i][1] and (self.row - j, self.col - j) in op_pieces:  # Posição legal cima esquerda
                            to_pop.append(i)
                        if self.row > self.legal[i][0] and self.col < self.legal[i][1] and (self.row - j, self.col + j) in op_pieces:  # Posição legal cima direita
                            to_pop.append(i)
                        if self.row < self.legal[i][0] and self.col > self.legal[i][1] and (self.row + j, self.col - j) in op_pieces:  # Posição legal baixo esquerda
                            to_pop.append(i)
                        if self.row < self.legal[i][0] and self.col < self.legal[i][1] and (self.row + j, self.col + j) in op_pieces:  # Posição legal baixo direita
                            to_pop.append(i)

        # Remove as posições onde a peça saltaria sobre outra peça
        self.legal = [self.legal[i] for i in range(len(self.legal)) if i not in to_pop]


    def check_catch(self, board):
        """Calcula as posições legais para a peça capturar outras peças."""
        catchable = [(self.row - 1, self.col), (self.row + 1, self.col), (self.row, self.col + 1), (self.row, self.col - 1)]  # Posições onde peças capturáveis podem estar
        landing_pos = [(self.row - 2, self.col), (self.row + 2, self.col), (self.row, self.col + 2), (self.row, self.col - 2)]  # Posição depois disso
        self.legal = []
        whites, blacks = board.occupied()

        if self.color == WHITE:
            for i in range(len(catchable)):
                if catchable[i] in blacks and landing_pos[i] not in whites + blacks and landing_pos[i][1] <= self.size - 1:
                    self.legal += [(landing_pos[i])]
        if self.color == BLACK:
            for i in range(len(catchable)):
                if catchable[i] in whites and landing_pos[i] not in whites + blacks and landing_pos[i][1] <= self.size - 1:
                    self.legal += [(landing_pos[i])]
        self.drop_out_range()


    def check_catch_king(self, board):
        """Calcula as posições legais para a dama capturar outras peças."""
        self.legal = []
        # Verificação para baixo
        end = False
        for i in range(1, self.down + 1):
            # Se encontrar uma peça adjacente e a próxima casa estiver ocupada ou for da mesma cor, para
            if self.row + i + 1 <= self.size - 1 and board.chessboard[self.row + i][self.col] != None and (board.chessboard[self.row + i + 1][self.col] != None or board.chessboard[self.row + i][self.col].color == self.color):
                break

            # Se encontrar uma peça adjacente de cor diferente e a próxima casa estiver livre
            if self.row + i + 1 <= self.size - 1 and board.chessboard[self.row + i][self.col] != None and board.chessboard[self.row + i][self.col].color != self.color and board.chessboard[self.row + i + 1][self.col] == None:
                # Se for a primeira casa após a peça atual
                if i == 1:
                    self.legal += [(self.row + i + 1, self.col)]
                    # Adiciona todas as casas livres após a casa de captura
                    for j in range(1, self.row + i + 2):
                        if self.row + i + 1 + j <= self.size - 1 and board.chessboard[self.row + i + 1 + j][self.col] == None:
                            self.legal += [(self.row + i + 1 + j, self.col)]
                        else:
                            end = True
                            break
                # Se não for a primeira casa, mas a casa anterior estiver livre
                elif i > 1 and board.chessboard[self.row + i - 1][self.col] == None:
                    self.legal += [(self.row + i + 1, self.col)]
                    # Adiciona todas as casas livres após a casa de captura
                    for j in range(1, self.row + i + 2):
                        if self.row + i + 1 + j <= self.size - 1 and board.chessboard[self.row + i + 1 + j][self.col] == None:
                            self.legal += [(self.row + i + 1 + j, self.col)]
                        else:
                            end = True
                            break
            if end:
                break

        # Verificação para cima
        end = False
        for i in range(1, self.row + 1):
            if self.row - i - 1 >= 0 and board.chessboard[self.row - i][self.col] != None and (board.chessboard[self.row - i - 1][self.col] != None or board.chessboard[self.row - i][self.col].color == self.color):
                break

            if self.row - i - 1 >= 0 and board.chessboard[self.row - i][self.col] != None and board.chessboard[self.row - i][self.col].color != self.color and board.chessboard[self.row - i - 1][self.col] == None:
                if i == 1:
                    self.legal += [(self.row - i - 1, self.col)]
                    for j in range(1, self.row - i):
                        if self.row - i - 1 - j >= 0 and board.chessboard[self.row - i - 1 - j][self.col] == None:
                            self.legal += [(self.row - i - 1 - j, self.col)]
                        else:
                            end = True
                            break
                elif i > 1 and board.chessboard[self.row - i + 1][self.col] == None:
                    self.legal += [(self.row - i - 1, self.col)]
                    for j in range(1, self.row - i):
                        if self.row - i - 1 - j >= 0 and board.chessboard[self.row - i - 1 - j][self.col] == None:
                            self.legal += [(self.row - i - 1 - j, self.col)]
                        else:
                            end = True
                            break
            if end:
                break

        # Verificação para a direita
        end = False
        for i in range(1, self.right + 1):
            if self.col + i + 1 <= self.size - 1 and board.chessboard[self.row][self.col + i] != None and (board.chessboard[self.row][self.col + i + 1] != None or board.chessboard[self.row][self.col + i].color == self.color):
                break

            if self.col + i + 1 <= self.size - 1 and board.chessboard[self.row][self.col + i] != None and board.chessboard[self.row][self.col + i].color != self.color and board.chessboard[self.row][self.col + i + 1] == None:
                if i == 1:
                    self.legal += [(self.row, self.col + i + 1)]
                    for j in range(1, self.col + i + 2):
                        if self.col + i + 1 + j <= self.size - 1 and board.chessboard[self.row][self.col + i + 1 + j] == None:
                            self.legal += [(self.row, self.col + i + 1 + j)]
                        else:
                            end = True
                            break
                elif i > 1 and board.chessboard[self.row][self.col + i - 1] == None:
                    self.legal += [(self.row, self.col + i + 1)]
                    for j in range(1, self.col + i + 2):
                        if self.col + i + 1 + j <= self.size - 1 and board.chessboard[self.row][self.col + i + 1 + j] == None:
                            self.legal += [(self.row, self.col + i + 1 + j)]
                        else:
                            end = True
                            break
            if end:
                break

        # Verificação para a esquerda
        end = False
        for i in range(1, self.col + 1):
            if self.col - i - 1 >= 0 and board.chessboard[self.row][self.col - i] != None and (board.chessboard[self.row][self.col - i - 1] != None or board.chessboard[self.row][self.col - i].color == self.color):
                break

            if self.col - i - 1 >= 0 and board.chessboard[self.row][self.col - i] != None and board.chessboard[self.row][self.col - i].color != self.color and board.chessboard[self.row][self.col - i - 1] == None:
                if i == 1:
                    self.legal += [(self.row, self.col - i - 1)]
                    for j in range(1, self.col - i):
                        if self.col - i - 1 - j >= 0 and board.chessboard[self.row][self.col - i - 1 - j] == None:
                            self.legal += [(self.row, self.col - i - 1 - j)]
                        else:
                            end = True
                            break

                elif i > 1 and board.chessboard[self.row][self.col - i + 1] == None:  # Isto é para evitar saltar sobre mais do que uma peça adversária consecutiva
                    self.legal += [(self.row, self.col - i - 1)]
                    for j in range(1, self.col - i):
                        if self.col - i - 1 - j >= 0 and board.chessboard[self.row][self.col - i - 1 - j] == None:
                            self.legal += [(self.row, self.col - i - 1 - j)]
                        else:
                            end = True
                            break
            if end:
                break  # Isto é porque depois de encontrar uma peça para capturar e os espaços livres seguintes, o loop interno para e o loop externo
                       # continua e pode haver outra peça adversária para capturar, mas não é suposto nos preocuparmos com essa, então isto quebra o loop externo

        self.drop_out_range()


    def drop_out_range(self):
        """Remove as posições legais que estão fora do tabuleiro."""
        drop = []
        for i in range(len(self.legal)):
            if self.legal[i][0] < 0 or self.legal[i][0] > self.size - 1 or self.legal[i][1] < 0 or self.legal[i][1] > self.size - 1:
                drop.append(i)
        self.legal = [self.legal[i] for i in range(len(self.legal)) if i not in drop]