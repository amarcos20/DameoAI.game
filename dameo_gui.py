import pygame
from vars import *
import time

class GUI:
    """
    Classe responsável pela interface gráfica do jogo.

    Gerencia a exibição de menus, tabuleiro, peças,
    movimentos legais e mensagens no ecrã.
    """

    def __init__(self):
        """Inicializa a interface gráfica."""
        self.square_size = None


    def main_menu(self, screen):
        """
        Exibe o menu principal do jogo.

        Permite que o utilizador inicie o jogo.

        Args:
            screen (pygame.Surface): A superfície do Pygame onde o menu será desenhado.

        Returns:
            tuple: Uma tupla contendo:
                - players (list): Uma lista com informações sobre os jogadores.
                - size (int): O tamanho do tabuleiro.
        """
        font = pygame.font.Font(None, 36)

        # Cria o texto "Clique para Iniciar"
        start_text = font.render("Clique para Iniciar", True, (255, 255, 255))  # select text and color
        text_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))  # Centre the text

        # Preenche o ecrã com preto
        screen.fill((0, 0, 0))
        # Desenha o texto no ecrã
        screen.blit(start_text, text_rect)
        # Atualiza o ecrã
        pygame.display.flip()  # display

        waiting = True
        # Loop de espera por um evento do utilizador
        while waiting:
            # Captura eventos do Pygame
            for event in pygame.event.get():
                # Se o utilizador clicar no botão de fechar a janela
                if event.type == pygame.QUIT:  # close if click on 'x' symbol
                    pygame.quit()
                    exit()
                # Se o utilizador clicar com o botão esquerdo do rato
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Start if click on ecran
                    # Abre o menu de seleção de jogadores e tamanho do tabuleiro
                    players, size = self.player_select_menu(screen)  # Call function to go to the next screen
                    self.square_size = int(min(width, height)/size)
                    return players, size

    def player_select_menu(self, screen):
        """
        Exibe o menu de seleção de jogadores.

        Permite que o utilizador selecione o tipo de jogador (Humano, IA)
        e o tamanho do tabuleiro.

        Args:
            screen (pygame.Surface): A superfície do Pygame onde o menu será desenhado.

        Returns:
            tuple: Uma tupla contendo:
                - players (list): Uma lista com informações sobre os jogadores.
                - size (int): O tamanho do tabuleiro.
        """
        # Opções de tipo de jogador
        player_options = ['Humano', 'Bebé', 'Fácil', 'Médio', 'Difícil' ] # Tradução das opções
        # Opções de tamanho do tabuleiro
        size_board_options = ['5x5', '6x6', '7x7', '8x8']
        # Tamanho padrão do tabuleiro
        size='6x6'
        # Lista para armazenar informações sobre os jogadores
        players = ["Humano", "Humano", None, None]  # [player1, player2, depth1, depth2] # Tradução das opções
        # Preenche o ecrã com cinzento
        screen.fill(GREY2)
        # Cria um objeto de fonte
        font = pygame.font.Font(None, 36)

        running = True
        # Loop principal do menu de seleção de jogadores
        while running:
            # Captura eventos do Pygame
            for event in pygame.event.get():
                # Se o utilizador clicar no botão de fechar a janela
                if event.type == pygame.QUIT:
                    running = False

                # Se o utilizador clicar com o rato
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Se o utilizador clicar na seta para trás do jogador 1
                    if 75 < event.pos[0] < 90 and 260 < event.pos[1] < 290:
                        players[0] = player_options[(player_options.index(players[0]) - 1) % len(player_options)]
                    # Se o utilizador clicar na seta para a frente do jogador 1
                    elif 210 < event.pos[0] < 225 and 260 < event.pos[1] < 290:
                        players[0] = player_options[(player_options.index(players[0]) + 1) % len(player_options)]

                    # Se o utilizador clicar na seta para trás do jogador 2
                    if 325 < event.pos[0] < 340 and 260 < event.pos[1] < 290:
                        players[1] = player_options[(player_options.index(players[1]) - 1) % len(player_options)]
                    # Se o utilizador clicar na seta para a frente do jogador 2
                    elif 460 < event.pos[0] < 475 and 260 < event.pos[1] < 290:
                        players[1] = player_options[(player_options.index(players[1]) + 1) % len(player_options)]

                    # Se o utilizador clicar para diminuir o tamanho do tabuleiro
                    elif 255 < event.pos[0] < 295 and 235 < event.pos[1] < 255:
                        size = size_board_options[(size_board_options.index(size) - 1) % len(size_board_options)]
                    # Se o utilizador clicar para aumentar o tamanho do tabuleiro
                    elif 255 < event.pos[0] < 295 and 175 < event.pos[1] < 195:
                        size = size_board_options[(size_board_options.index(size) + 1) % len(size_board_options)]

                    # Se o utilizador clicar no botão "GO!"
                    elif 250 < event.pos[0] < 300 and 335 < event.pos[1] < 365:
                        # Define o tipo de jogador 1 e a sua profundidade (se for IA)
                        if players[0] == 'Humano':
                            players[0], players[2] = 'Humano', None

                        elif players[0] == 'Bebé': # Tradução das opções
                            players[0], players[2] = 'Random', None

                        elif players[0] == 'Fácil': # Tradução das opções
                            players[0], players[2] = 'Minimax', 2

                        elif players[0] == 'Médio': # Tradução das opções
                            players[0], players[2] = 'Montecarlo', 20

                        elif players[0] == 'Difícil': # Tradução das opções
                            players[0], players[2] = 'Montecarlo', 40

                        # Define o tipo de jogador 2 e a sua profundidade (se for IA)
                        if players[1] == 'Humano':
                            players[1], players[3] = 'Humano', None

                        elif players[1] == 'Bebé': # Tradução das opções
                            players[1], players[3] = 'Random', None

                        elif players[1] == 'Fácil': # Tradução das opções
                            players[1], players[3] = 'Minimax', 2

                        elif players[1] == 'Médio': # Tradução das opções
                            players[1], players[3] = 'Montecarlo', 20

                        elif players[1] == 'Difícil': # Tradução das opções
                            players[1], players[3] = 'Montecarlo', 40

                        return players, int(size[0])
    



            # Preenche o ecrã com cinzento
            screen.fill(GREY2)  # Clear the screen

            # Título do jogo
            text_surface = font.render("Jogo do Dameo", True, (50,50,50)) # Tradução do título
            text_rect = text_surface.get_rect()
            text_rect.topleft = (190, 50)
            screen.blit(text_surface, text_rect)

            # Texto "Jogador 1"
            text_surface = font.render("Jogador 1", True, WHITE) # Tradução das opções
            text_rect = text_surface.get_rect()
            text_rect.topleft = (100, 200)
            screen.blit(text_surface, text_rect)

            # Texto "Jogador 2"
            text_surface = font.render("Jogador 2", True, BLACK) # Tradução das opções
            text_rect = text_surface.get_rect()
            text_rect.topright = (460, 200)
            screen.blit(text_surface, text_rect)

            text_surface = font.render("         Tamanho do Tabuleiro", True, (0,0,255)) # Tradução das opções
            text_rect = text_surface.get_rect()
            text_rect.topright = (410, 140)
            screen.blit(text_surface, text_rect)

            # Caixa de seleção do jogador 1
            pygame.draw.rect(screen, WHITE, (100, 250, 100, 50))
            pygame.draw.polygon(screen, BLACK, [(90, 260), (90, 290), (75, 275)])
            pygame.draw.polygon(screen, BLACK, [(210, 260), (210, 290), (225, 275)])
            text_surface = font.render(players[0], True, BLACK)
            text_rect = text_surface.get_rect()
            text_rect.center = (150, 275)
            screen.blit(text_surface, text_rect)

            # Caixa de seleção do jogador 2
            pygame.draw.rect(screen, BLACK, (350, 250, 100, 50))
            pygame.draw.polygon(screen, WHITE, [(340, 260), (340, 290), (325, 275)])
            pygame.draw.polygon(screen, WHITE, [(460, 260), (460, 290), (475, 275)])
            text_surface = font.render(players[1], True, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.center = (400, 275)
            screen.blit(text_surface, text_rect)

            # Caixa de seleção do tamanho do tabuleiro
            pygame.draw.rect(screen, (180,165,100), (250, 200, 50, 30))
            pygame.draw.polygon(screen, GREY1, [(255, 195), (295, 195), (275, 175)])
            pygame.draw.polygon(screen, GREY1, [(255, 235), (295, 235), (275, 255)])
            text_surface = font.render(size, True, (0,0,255))
            text_rect = text_surface.get_rect()
            text_rect.center = (275, 215)
            screen.blit(text_surface, text_rect)

            # Botão "GO!"
            pygame.draw.rect(screen, (180,165,100), (250, 335, 50, 30))
            text_surface = font.render('GO!', True, (0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (275, 350)
            screen.blit(text_surface, text_rect)

            pygame.display.flip()


    def display_legal_moves(self, screen, legal_moves):
        """
        Destaca os quadrados dos movimentos legais no ecrã.

        Args:
            screen (pygame.Surface): A superfície do Pygame onde os movimentos serão destacados.
            legal_moves (list): Uma lista de tuplas (row, col) representando os movimentos legais.
        """
        for move in legal_moves:
            row, col = move
            pygame.draw.rect(screen, (180, 195, 100), (col * self.square_size, row * self.square_size, self.square_size, self.square_size))
            pygame.draw.rect(screen, (255, 255, 153), (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 3)


    def display_turn(self, screen, turn):
        """Exibe de quem é a vez de jogar."""
        font = pygame.font.Font(None, 36)
        text = font.render(f"{turn}", True,(135, 205, 250))
        text_rect = text.get_rect(center=(460, 50))
        screen.blit(text, text_rect)


    def display_selected_piece(self, screen, piece):
        """Destaca a peça selecionada."""
        if piece:
            row, col = piece.row, piece.col
            pygame.draw.rect(screen, (50, 50, 50), (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 3)


    def display_message(self, screen, message, color=(135, 206, 250), place =(438, 190)):
        """Exibe uma mensagem no ecrã."""
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=place)
        screen.blit(text, text_rect)