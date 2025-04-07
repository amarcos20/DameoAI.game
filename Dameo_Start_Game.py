import pygame
from board import Board
from piece import Piece
from dameo_gui import GUI
from vars import *
from player import Player
import time
import os

def main():
    """Inicia o jogo Dameo."""
    pygame.init()  # Inicializa o Pygame
    screen = pygame.display.set_mode((width, height))  # Cria a janela do jogo
    pygame.display.set_caption('DAMEO')  # Define o título da janela
    running = True  # Flag para controlar o loop principal do jogo
    gui = GUI()  # Cria uma instância da interface gráfica
    # Abre o menu principal e obtém informações sobre os jogadores e o tamanho do tabuleiro
    players, size = gui.main_menu(screen)  # [player1, player2, depth1, depth2], tamanho do tabuleiro
    square_size = int(min(width, height)/size)  # Calcula o tamanho de cada quadrado do tabuleiro
    gui.square_size = square_size  # Define o tamanho do quadrado na interface gráfica
    board=Board(size)  # Cria uma instância do tabuleiro
    board.start_game(gui, screen)  # Inicializa o jogo
    selected_piece = None  # Variável para armazenar a peça selecionada pelo jogador
    turn = WHITE  # Define o turno inicial como branco
    winner = None  # Variável para armazenar o vencedor do jogo
    player1 = Player(players[0], players[2], WHITE)  # Cria o jogador 1
    player2 = Player(players[1], players[3], BLACK)  # Cria o jogador 2
    gui.display_turn(screen, turn)  # Exibe o turno inicial no ecrã
    game_over=False  # Flag para indicar se o jogo terminou

    # Loop principal do jogo
    while running:

        # Preenche o fundo do ecrã com a cor do turno atual
        if turn == WHITE:
            screen.fill(WHITE)  # Preenche com branco se for a vez do branco
        else:
            screen.fill(GREY2)  # Preenche com cinzento2 se for a vez do preto

        # Captura eventos do Pygame
        for event in pygame.event.get():
            # Se o jogador clicar no botão de fechar a janela
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botão esquerdo do rato clicado
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


        # Se o jogo terminou, sai do loop
        if game_over:
            break

        # Loop para alternar entre os jogadores
        while not game_over and running:
            for player in (player1, player2):

                # Se for a vez de um jogador humano
                if player.type == 'Humano' and turn == player.team:
                    selected_piece = player.get_human_move(board, gui, screen, winner, square_size, selected_piece)


                # Se for a vez de um jogador IA
                if player.type != 'Humano' and turn == player.team:
                    selected_piece = player.get_ai_move(board)

                # Verifica se a peça pode capturar
                if not selected_piece.king:
                    selected_piece.check_catch(board)
                else:
                    selected_piece.check_catch_king(board)

                # Se a peça puder capturar, continua o turno
                if selected_piece.legal and selected_piece.has_caught:
                    pass  # NÃO É PRECISO FAZER NADA

                # Se a peça não puder capturar, passa o turno para o próximo jogador
                else:
                    is_king = selected_piece.king
                    selected_piece.transform_king()


                    selected_piece = None  # Desativa a peça selecionada
                    if turn == WHITE:
                        turn = BLACK
                        board.turn = BLACK
                    else:
                        turn = WHITE
                        board.turn = WHITE


                    board.actual_state(screen)
                    gui.display_turn(screen, "   BRANCAS" if turn == WHITE else "   PRETAS") # Exibe o turno (traduzido)
                    time.sleep(0.3)
                    pygame.display.flip()


                # Verifica se há um vencedor
                winner = board.check_winner()


                # Se houver um vencedor, exibe a mensagem e sai do loop
                if winner:
                    game_over = True
                    font = pygame.font.SysFont("Impact", 45)
                    if winner == 'Empate': 
                        text = font.render("Deu Empate!", True, (255, 255, 153)) 
                    elif winner and winner != 'Empate': 
                        text = font.render(f"O Vencedor é o {winner}!", True, (255, 255, 153))
                    screen.blit(text, (100, height // 2))
                    pygame.display.flip()
                    break

if __name__ == "__main__":
    main()