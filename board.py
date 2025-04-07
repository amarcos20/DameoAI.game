import pygame
import sys
from piece import Piece
from vars import *

class Board:
    """
    Representa o tabuleiro do jogo de damas (Dameo).

    Contém informações sobre o tamanho do tabuleiro, cores,
    a matriz que representa o tabuleiro, e listas de peças.
    """

    def __init__(self, size):
        """
        Inicializa o tabuleiro.

        Args:
            size (int): O tamanho do tabuleiro (número de linhas e colunas).
        """
        self.size = size
        self.square_size = int(min(width, height)/self.size)  # Tamanho de cada quadrado
        self.color1 =  (255, 206, 158)  # Cor 1 do tabuleiro
        self.color2 = (209, 139, 71)  # Cor 2 do tabuleiro
        self.chessboard = [[None for i in range(self.size)] for j in range(self.size)]  # Matriz representando o tabuleiro
        self.all_pieces_white = []  # Lista para armazenar as peças brancas
        self.all_pieces_black = []  # Lista para armazenar as peças pretas
        self.last_moved_piece = None  # A última peça que foi movida
        self.last_move = ()  # O último movimento realizado
        self.is_terminal = False  # Flag para indicar se o jogo terminou
        self.turn = None  # A cor do jogador atual (WHITE ou BLACK)
        self.moves_whitout_catching = 0  # Contador de movimentos sem capturas


    def change_size(self, size):
        """
        Altera o tamanho do tabuleiro.

        Args:
            size (int): O novo tamanho do tabuleiro.
        """
        self.size = size
        self.square_size = int(min(width, height)/size)
        self.chessboard = [[None for i in range(self.size)] for j in range(self.size)]


    def start_game(self, gui, screen):
        """
        Inicia um novo jogo.

        Inicializa as peças no tabuleiro e desenha o estado inicial.

        Args:
            gui (GUI): A interface gráfica do jogo.
            screen (pygame.Surface): A superfície do Pygame onde o jogo será desenhado.
        """
        screen.fill((0,0,0))
        self.initialize_pieces()
        self.draw_initial_state(screen, self.all_pieces_white, self.all_pieces_black)
        pygame.display.flip()


    def initialize_pieces(self):
        """
        Inicializa as peças no tabuleiro.

        Cria as peças brancas e pretas e as coloca em suas posições iniciais.
        """
        # Limpa as listas de peças (para reiniciar o jogo)
        self.all_pieces_white = []
        self.all_pieces_black = []

        # Peças para tabuleiros de tamanho 6 ou maior
        if self.size>=6:
            # Inicializa as peças brancas
            for row in range (self.size-3, self.size):
                for col in range(self.size):
                    # Pula algumas posições específicas
                    if (row == self.size-2 and col in [0, self.size-1]) or (row == self.size-3 and col in [0, 1, self.size-1, self.size-2]):
                        continue
                    else:
                        piece = Piece(self.size, row, col, WHITE)  # Cria uma nova peça branca
                        self.all_pieces_white.append(piece)  # Adiciona a peça à lista de peças brancas
                        self.chessboard[row][col] = piece  # Coloca a peça na matriz do tabuleiro

            # Inicializa as peças pretas
            for row in range (3):
                for col in range(self.size):
                    # Pula algumas posições específicas
                    if (row == 1 and col in [0, self.size-1]) or (row == 2 and col in [0, 1, self.size-1, self.size-2]):
                        continue
                    else:
                        piece = Piece(self.size, row, col, BLACK)  # Cria uma nova peça preta
                        self.all_pieces_black.append(piece)  # Adiciona a peça à lista de peças pretas
                        self.chessboard[row][col] = piece  # Coloca a peça na matriz do tabuleiro

        # Peças para tabuleiros de tamanho 4 ou 5
        if self.size== 4 or self.size== 5:
            # Inicializa as peças brancas
            for row in range (self.size-2, self.size):
                for col in range(self.size):
                    # Pula algumas posições específicas
                    if (row == self.size-2 and col in [0, self.size-1]):
                        continue
                    else:
                        piece = Piece(self.size, row, col, WHITE)  # Cria uma nova peça branca
                        self.all_pieces_white.append(piece)  # Adiciona a peça à lista de peças brancas
                        self.chessboard[row][col] = piece  # Coloca a peça na matriz do tabuleiro

            # Inicializa as peças pretas
            for row in range (2):
                for col in range(self.size):
                    # Pula algumas posições específicas
                    if (row == 1 and col in [0, self.size-1]):
                        continue
                    else:
                        piece = Piece(self.size, row, col, BLACK)  # Cria uma nova peça preta
                        self.all_pieces_black.append(piece)  # Adiciona a peça à lista de peças pretas
                        self.chessboard[row][col] = piece  # Coloca a peça na matriz do tabuleiro

        return self.all_pieces_white, self.all_pieces_black


    def draw_initial_state(self, screen, all_pieces_white, all_pieces_black):
        """
        Desenha o estado inicial do tabuleiro no ecrã.

        Args:
            screen (pygame.Surface): A superfície do Pygame onde o jogo será desenhado.
            all_pieces_white (list): Lista de peças brancas.
            all_pieces_black (list): Lista de peças pretas.
        """
        self.draw_chessboard(screen)
        # Desenha todas as peças (pretas e brancas)
        for piece in all_pieces_black + all_pieces_white:
            self.draw_piece(screen, piece.row, piece.col, piece)


    def actual_state(self, screen):
        """Desenha o estado atual do tabuleiro."""
        screen.fill((0, 0, 0))
        self.draw_chessboard(screen)

        # Desenha as peças pretas
        for i in range(len(self.all_pieces_black)):
            self.draw_piece(screen, self.all_pieces_black[i].row, self.all_pieces_black[i].col, self.all_pieces_black[i])
        # Desenha as peças brancas
        for i in range(len(self.all_pieces_white)):
            self.draw_piece(screen, self.all_pieces_white[i].row, self.all_pieces_white[i].col, self.all_pieces_white[i])

        pygame.display.flip()


    def draw_king(self, screen, row, col, piece):
        """Desenha uma peça como rei (dama)."""
        if piece.color == WHITE:
            piece_image = pygame.image.load("../Projeto_1_final/icons/king_white.png")  # Carrega a imagem da dama branca
        else:
            piece_image = pygame.image.load("../Projeto_1_final/icons/king_black.png")  # Carrega a imagem da dama preta

        piece_image = pygame.transform.scale(piece_image, (self.square_size - 10, self.square_size - 10))  # Redimensiona a imagem

        # Calcula a posição para desenhar a imagem
        x_pos = col * self.square_size + 5
        y_pos = row * self.square_size + 5

        screen.blit(piece_image, (x_pos, y_pos))  # Desenha a imagem no ecrã


    def draw_piece(self, screen, row, col, piece):
        """Desenha uma peça no tabuleiro."""
        if piece.king:  # Se a peça é uma dama
            self.draw_king(screen, row, col, piece)
        else:  # Se a peça é normal
            if piece.color == WHITE:
                piece_image = pygame.image.load("../Projeto_1_final/icons/piece_white.png")  # Carrega a imagem da peça branca
            else:
                piece_image = pygame.image.load("../Projeto_1_final/icons/piece_black.png")  # Carrega a imagem da peça preta
            piece_image = pygame.transform.scale(piece_image, (self.square_size - 10, self.square_size - 10))  # Redimensiona a imagem

            # Calcula a posição para desenhar a imagem
            x_pos = col * self.square_size + 5
            y_pos = row * self.square_size + 5

            screen.blit(piece_image, (x_pos, y_pos))  # Desenha a imagem no ecrã


    def draw_chessboard(self, screen):
        """Desenha o tabuleiro no ecrã."""
        for row in range(self.size):
            for col in range(self.size):
                # Define a cor do quadrado com base na sua posição
                color = self.color1 if (row + col) % 2 == 0 else self.color2
                pygame.draw.rect(screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))


    def find_piece(self, row, col, all_pieces_black, all_pieces_white):
        """
        Encontra uma peça na posição especificada.

        Args:
            row (int): A linha da posição.
            col (int): A coluna da posição.
            all_pieces_black (list): A lista de peças pretas.
            all_pieces_white (list): A lista de peças brancas.

        Returns:
            Piece: A peça encontrada na posição, ou None se não houver nenhuma peça.
        """
        # Itera sobre todas as peças para encontrar a peça na posição especificada
        for piece in all_pieces_black + all_pieces_white:
            if piece.row == row and piece.col == col:
                return piece
        return None  # Retorna None se não encontrar nenhuma peça


    def occupied(self):
        """
        Obtém as posições ocupadas pelas peças.

        Returns:
            tuple: Uma tupla contendo duas listas:
                - A primeira lista contém as posições ocupadas pelas peças brancas.
                - A segunda lista contém as posições ocupadas pelas peças pretas.
        """
        taken_white = []
        taken_black = []
        # Itera sobre as peças brancas e adiciona as suas posições à lista
        for i in range(len(self.all_pieces_white)):
            taken_white += [(self.all_pieces_white[i].row, self.all_pieces_white[i].col)]
        # Itera sobre as peças pretas e adiciona as suas posições à lista
        for i in range(len(self.all_pieces_black)):
            taken_black += [(self.all_pieces_black[i].row, self.all_pieces_black[i].col)]
        return taken_white, taken_black


    def drop_piece(self, row, col):
        """
        Remove uma peça do tabuleiro.

        Args:
            row (int): A linha da posição da peça a ser removida.
            col (int): A coluna da posição da peça a ser removida.
        """
        # Remove a peça da lista de peças pretas, se estiver lá
        for i in range(len(self.all_pieces_black)):
            if row == self.all_pieces_black[i].row and col == self.all_pieces_black[i].col:
                self.all_pieces_black.pop(i)
                break

        # Remove a peça da lista de peças brancas, se estiver lá
        for i in range(len(self.all_pieces_white)):
            if row == self.all_pieces_white[i].row and col == self.all_pieces_white[i].col:
                self.all_pieces_white.pop(i)
                break


    def check_piece_to_capture(self, turn):
        """
        Verifica se alguma peça pode capturar outra peça.

        Args:
            turn (tuple): A cor do jogador atual (WHITE ou BLACK).

        Returns:
            list: Uma lista de peças que podem capturar outras peças.
        """
        can_catch=[]
        # Seleciona a lista de peças do jogador atual
        all_pieces = self.all_pieces_black if turn == BLACK else self.all_pieces_white
        # Itera sobre as peças do jogador atual
        for piece in all_pieces:
            # Verifica se a peça é uma dama ou não e chama a função apropriada para verificar se pode capturar
            if not piece.king:
                piece.check_catch(self)  # Atualiza os movimentos legais considerando capturas
            elif piece.king:
                piece.check_catch_king(self)  # Atualiza os movimentos legais considerando capturas para damas

            # Se a peça pode capturar, adiciona-a à lista
            if piece.legal:
                can_catch.append(piece)

                # Se a peça já capturou, retorna apenas essa peça (captura obrigatória)
                if piece.has_caught:
                    can_catch = [piece]
                    break
        return can_catch


    def check_if_capture(self, gui, screen, can_catch, piece, turn, selected_piece):
        """
        Verifica se o jogador deve capturar uma peça (e força a captura, se aplicável).

        Args:
            gui (GUI): A interface gráfica do jogo.
            screen (pygame.Surface): A superfície do Pygame onde o jogo será desenhado.
            can_catch (list): Uma lista de peças que podem capturar outras peças.
            piece (Piece): A peça que o jogador selecionou.
            turn (tuple): A cor do jogador atual (WHITE ou BLACK).
            selected_piece (Piece): A peça que foi selecionada anteriormente.

        Returns:
            Piece: A peça que o jogador deve mover.
        """
        catch_position =[]
        # Cria uma lista de posições onde as peças podem ser capturadas
        for i in can_catch:
            catch_position.append((i.row, i.col))

        pos = ()
        piece_color=None
        # Obtém a posição e a cor da peça selecionada
        if piece is not None:
            pos = (piece.row, piece.col)
            piece_color = piece.color

        message_displayed = True

        # Loop para forçar o jogador a capturar a peça correta
        while can_catch and pos not in catch_position and piece_color == turn and pos != ():

            # Exibe uma mensagem informando que o jogador deve capturar uma peça
            if message_displayed:
                self.actual_state(screen)
                gui.display_selected_piece(screen, selected_piece)
                gui.display_message(screen, '          CAPTURAR') # Mensagem em português
                pygame.display.flip()
                message_displayed = False

            # Captura eventos do Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False # Falta definir a variavel running

                # Se o jogador clicar com o rato
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row = y // self.square_size
                    col = x // self.square_size

                    # Encontra a peça na posição clicada
                    piece = self.find_piece(row, col, self.all_pieces_black, self.all_pieces_white)
                    if piece is not None:
                        pos = (piece.row, piece.col)
                        colour = piece.color

        return piece


    def check_winner(self):
        """Verifica se há um vencedor."""
        self.is_terminal = False  # Reinicia o estado terminal
        legal_pieces_white, _ = self.find_available_moves(WHITE)
        legal_pieces_black, _ = self.find_available_moves(BLACK)

        # Se não houver peças pretas ou o jogador preto não puder mover-se, o jogador branco vence
        if len(self.all_pieces_black) == 0 or (not legal_pieces_black and self.turn == BLACK):  #or black cannot move
            self.is_terminal = True
            return "Player 1"
        # Se não houver peças brancas ou o jogador branco não puder mover-se, o jogador preto vence
        elif len(self.all_pieces_white) == 0 or (not legal_pieces_white and self.turn == WHITE):  #or white cannot move
            self.is_terminal = True
            return "Player 2"

        # Se o número de movimentos sem captura atingir um limite, o jogo termina em empate
        if self.moves_whitout_catching == self.size*7:
            return "Empate" # Retorna "Empate" em vez de "Tie"


    def find_available_moves(self, turn):
        """
        Encontra os movimentos disponíveis para um determinado jogador.

        Args:
            turn (tuple): A cor do jogador atual (WHITE ou BLACK).

        Returns:
            tuple: Uma tupla contendo duas listas:
                - A primeira lista contém as peças que podem mover-se.
                - A segunda lista contém os movimentos legais para cada peça.
        """
        legal_moves = []
        # Verifica se alguma peça pode capturar
        legal_pieces = self.check_piece_to_capture(turn)

        # Se houver peças que podem capturar, encontra os movimentos legais para cada peça
        if legal_pieces:

            # Obtém os movimentos legais para cada peça, seja dama ou não
            for piece in legal_pieces:
                if piece.king:
                    piece.check_catch_king(self)
                    legal_moves.append(piece.legal)
                else:
                    piece.check_catch(self)
                    legal_moves.append(piece.legal)

        # Se não houver peças que podem capturar, encontra os movimentos normais
        else:

            # Seleciona a lista de peças do jogador atual
            if turn == WHITE:
                legal_pieces = self.all_pieces_white
            else:
                legal_pieces = self.all_pieces_black

            # Obtém os movimentos legais para cada peça
            for piece in legal_pieces:
                piece.legal_positions()
                piece.check_position(self)
                piece.no_jump(self)
                legal_moves.append(piece.legal)

            # Remove as peças sem movimentos disponíveis
            index = []
            for i in range(len(legal_moves)):
                if legal_moves[i] == []:
                    index.append(i)

            legal_pieces = [legal_pieces[i] for i in range(len(legal_pieces)) if i not in index]
            legal_moves = [legal_moves[i] for i in range(len(legal_moves)) if i not in index]

        return legal_pieces, legal_moves


    def print_board(self):
        """Imprime o estado atual do tabuleiro na consola (para depuração)."""
        print("O" if self.turn == WHITE else "X")
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                piece = self.chessboard[i][j]
                if piece == None:
                    row += "-"
                else:
                    row += ("O" if piece.king else "o") if piece.color == WHITE else ("X" if piece.king else "x")
            print(row)
        print('\n')


    def count_possible_moves(self):
        """Conta o número de movimentos possíveis para o jogador atual."""
        legal_pieces, legal_moves = self.find_available_moves(self.turn)
        n_children = 0
        for i in range(len(legal_pieces)):
            for j in range(len(legal_moves)):
                n_children += 1
        return n_children