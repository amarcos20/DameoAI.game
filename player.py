import random
from vars import *
from board import Board
import math
from copy import deepcopy
from ai import Minimax, MontecarloTreeSearch
import pygame

class Player:
    """
    Representa um jogador no jogo de damas (Dameo).

    Pode ser um jogador humano ou uma IA (Minimax, Monte Carlo ou Random).
    """

    def __init__(self, player_type, depth_or_iterations, team, evaluation_function = 1):
        """
        Inicializa um jogador.

        Args:
            player_type (str): O tipo de jogador ("Humano", "Minimax", "Montecarlo" ou "Random").
            depth_or_iterations (int): A profundidade da busca Minimax ou o número de iterações do Monte Carlo.
                                       Para o jogador "Random", este parâmetro não é usado.
            team (tuple): A cor do jogador (WHITE ou BLACK).
            evaluation_function (int): A função de avaliação a ser usada pelo Minimax (1, 2 ou 3).
        """
        self.type = player_type
        self.depth_or_iterations = depth_or_iterations
        self.team = team
        self.evaluation_function = evaluation_function


    def get_ai_move(self, board):
        """
        Obtém o movimento da IA.

        Args:
            board (Board): O tabuleiro do jogo.

        Returns:
            Piece: A peça que a IA moveu.
        """

        if self.type == "Minimax":
            # Cria uma instância do Minimax
            minimax = Minimax(self.depth_or_iterations)
            # Executa o Minimax para obter o melhor movimento
            best_piece_pos, best_move = minimax.execute_minimax(board, self.depth_or_iterations, self.team, self.evaluation_function)
            # Realiza o movimento no tabuleiro
            return self.make_ai_move(board, best_piece_pos, best_move)

        elif self.type == "Montecarlo":
            # Cria uma instância do MontecarloTreeSearch
            monte_carlo = MontecarloTreeSearch(self.depth_or_iterations)
            # Executa o Monte Carlo Tree Search para obter o melhor movimento
            best_piece_pos, best_move = monte_carlo.mcts(board, self.team)
            # Realiza o movimento no tabuleiro
            return self.make_ai_move(board, best_piece_pos, best_move)

        elif self.type == "Random":
            # Obtém todos os movimentos válidos para o jogador atual
            legal_pieces, legal_moves = board.find_available_moves(self.team)

            # Se não houver movimentos válidos, retorna None
            if not legal_pieces:
                return None

            # Escolhe uma peça aleatória
            piece_index = random.randint(0, len(legal_pieces) - 1)
            piece = legal_pieces[piece_index]

            # Escolhe um movimento aleatório para a peça
            move_index = random.randint(0, len(legal_moves[piece_index]) - 1)
            move = legal_moves[piece_index][move_index]

            # Realiza o movimento no tabuleiro
            best_piece_pos = (piece.row, piece.col)
            best_move = move
            return self.make_ai_move(board, best_piece_pos, best_move)


    def make_ai_move(self, board, best_piece_pos, best_move):
        """
        Realiza o movimento da IA no tabuleiro.

        Args:
            board (Board): O tabuleiro do jogo.
            best_piece_pos (tuple): A posição da peça a ser movida.
            best_move (tuple): A posição para onde a peça deve ser movida.

        Returns:
            Piece: A peça que foi movida.
        """
        # Obtém a peça na posição especificada
        selected_piece = board.chessboard[best_piece_pos[0]][best_piece_pos[1]]
        # Remove a peça da posição antiga
        board.chessboard[selected_piece.row][selected_piece.col] = None
        # Move a peça para a nova posição
        selected_piece.move(best_move[0], best_move[1], board)
        # Atualiza a posição da peça no tabuleiro
        board.chessboard[selected_piece.row][selected_piece.col] = selected_piece
        return selected_piece


    def get_human_move(self, board, gui, screen, winner, square_size, selected_piece):
        """
        Obtém o movimento do jogador humano.

        Args:
            board (Board): O tabuleiro do jogo.
            gui (GUI): A interface gráfica do jogo.
            screen (pygame.Surface): A superfície do Pygame onde o jogo é desenhado.
            winner (str): O vencedor do jogo (se houver).
            square_size (int): O tamanho de cada quadrado do tabuleiro.
            selected_piece (Piece): A peça atualmente selecionada pelo jogador.

        Returns:
            Piece: A peça que o jogador moveu.
        """
        human_playing = True
        # Loop para obter o movimento do jogador humano
        while human_playing:
            # Captura eventos do Pygame
            for event in pygame.event.get():
                # Se o jogador clicar no botão de fechar a janela
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                # Se o jogador clicar com o botão esquerdo do rato
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botão esquerdo do rato clicado
                    # Se o jogo já tiver um vencedor, reinicia o jogo
                    if winner:
                        winner = None
                        game_over = False
                        players, size = gui.main_menu(screen)
                        square_size = int(min(width, height)/size)
                        gui.square_size = square_size
                        board=Board(size)
                        board.start_game(gui, screen)
                        player1 = Player(players[0], players[2], WHITE)
                        player2 = Player(players[1], players[3], BLACK)
                        selected_piece = None
                        turn = WHITE
                        board.turn = WHITE


                    # Obtém a posição do rato
                    x, y = pygame.mouse.get_pos()
                    row = y // square_size
                    col = x // square_size


                    # Obtém a peça na posição do rato
                    piece = board.find_piece(row, col, board.all_pieces_black, board.all_pieces_white)


                    # Verifica se o jogador deve capturar uma peça
                    can_catch = board.check_piece_to_capture(self.team)
                    piece = board.check_if_capture( gui, screen, can_catch, piece, self.team, selected_piece)  # Verifica se a peça já capturou (se necessário)

                    # Se o jogador selecionou uma peça válida
                    if piece and piece.color == self.team:
                        selected_piece = piece

                        # Verifica se a peça pode capturar
                        if not piece.king:
                            selected_piece.check_catch(board)
                        elif piece.king:
                            selected_piece.check_catch_king(board)

                        # Se a peça não puder capturar, calcula os movimentos normais
                        if not selected_piece.legal:
                            selected_piece.legal_positions()  # Se não houver peça para capturar, a lista de movimentos legais estará vazia, então calculamos os movimentos normalmente
                            selected_piece.check_position(board)  # Remove os espaços ocupados dos movimentos legais
                            selected_piece.no_jump(board)
                            board.actual_state(screen)  # Desenha novamente o tabuleiro para limpar os destaques anteriores
                            gui.display_selected_piece(screen, selected_piece)  # Destaca a peça selecionada
                            gui.display_legal_moves(screen, selected_piece.legal)  # Destaca os movimentos legais
                            pygame.display.flip()

                        # Se a peça puder capturar, exibe os movimentos de captura
                        else:
                            # selected_piece.check_catch(board)
                            board.actual_state(screen)  # Desenha novamente o tabuleiro para limpar os destaques anteriores
                            gui.display_selected_piece(screen, selected_piece)  # Destaca a peça selecionada
                            gui.display_legal_moves(screen, selected_piece.legal)  # Destaca os movimentos legais
                            pygame.display.flip()

                    # Se o jogador já tiver selecionado uma peça
                    elif selected_piece:  # Se uma peça está selecionada e um quadrado é clicado

                        # Verifica se a peça pode capturar
                        if not selected_piece.king:
                            selected_piece.check_catch(board)
                        else:
                            selected_piece.check_catch_king(board)

                        # Se a peça não puder capturar, calcula os movimentos normais
                        if not selected_piece.legal:
                            selected_piece.legal_positions()  # Se não houver peça para capturar, a lista de movimentos legais estará vazia, então calculamos os movimentos normalmente
                            selected_piece.check_position(board)  # Remove os espaços ocupados dos movimentos legais
                            selected_piece.no_jump(board)  # Se for uma dama, não pode saltar por cima


                        # Se a posição clicada for um movimento legal
                        if (row, col) in selected_piece.legal:  # Se o quadrado selecionado é um movimento legal para a peça

                            board.chessboard[selected_piece.row][selected_piece.col] = None  # MATRIZ

                            selected_piece.move(row, col, board)  # Move
                            board.chessboard[selected_piece.row][selected_piece.col] = selected_piece  # MATRIZ
                            human_playing = False

                            board.actual_state(screen)
                            gui.display_turn(screen, "   BRANCAS" if self.team == WHITE else "   PRETAS")  # Exibe o turno 
                            pygame.display.flip()
                            return selected_piece
