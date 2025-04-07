import random
from vars import *  # Importa variáveis globais (ex: cores, tamanhos)
from board import Board  # Importa a classe Board para representar o tabuleiro
import math
from copy import deepcopy  # Importa deepcopy para criar cópias independentes de objetos
import time  # Importa o módulo time para medir o tempo de execução


class Minimax:
    """
    Implementação do algoritmo Minimax com poda Alpha-Beta para a tomada de decisões da IA.
    """

    def __init__(self, depth):
        """
        Inicializa o objeto Minimax.

        Args:
            depth (int): A profundidade máxima da árvore de busca Minimax.
        """
        self.depth = depth

    def minimax(self, board, depth, maximizing_player, alpha, beta, turn, evaluation_func):
        """
        Implementa o algoritmo Minimax com poda Alpha-Beta recursivamente.

        Args:
            board (Board): O estado atual do tabuleiro.
            depth (int): A profundidade restante na árvore de busca.
            maximizing_player (bool): True se o nó atual representa um movimento do jogador maximizador, False caso contrário.
            alpha (float): O melhor valor que o jogador maximizador pode garantir até agora.
            beta (float): O melhor valor que o jogador minimizador pode garantir até agora.
            turn (int): A cor do jogador atual (WHITE ou BLACK).
            evaluation_func (int): Qual função de avaliação usar (1, 2 ou 3).

        Returns:
            float: O valor heurístico do nó atual.
        """
        if depth == 0 or board.check_winner():
            # Se atingiu a profundidade máxima ou um estado terminal (vitória/derrota/empate), avalia o estado do tabuleiro
            if evaluation_func == 1:
                return self.evaluate(board, turn)
            elif evaluation_func == 2:
                return self.evaluate_2(board, turn)
            elif evaluation_func == 3:
                return self.evaluate_3(board, turn)

        # Alterna o turno para o próximo jogador
        turn = WHITE if turn == BLACK else BLACK

        # Encontra os movimentos legais para o jogador atual
        legal_pieces, legal_moves = board.find_available_moves(turn)

        if maximizing_player:
            # Jogador Maximizador (IA)
            max_eval = float('-inf')  # Inicializa com o menor valor possível
            for i, piece in enumerate(legal_pieces):
                for move in legal_moves[i]:
                    # Itera sobre cada possível movimento
                    # Efetua o movimento
                    previous_row = piece.row
                    previous_col = piece.col
                    board.chessboard[piece.row][piece.col] = None  # Remove a peça da posição atual
                    piece.move(move[0], move[1], board)  # Move a peça para a nova posição
                    board.chessboard[piece.row][piece.col] = piece  # Atualiza a posição da peça no tabuleiro

                    # Calcula o valor do nó filho recursivamente
                    eval = self.minimax(deepcopy(board), depth - 1, False, alpha, beta, turn, evaluation_func)

                    # Desfaz o movimento
                    board.chessboard[piece.row][piece.col] = None  # Remove a peça da nova posição
                    piece.move(previous_row, previous_col, board)  # Move a peça de volta para a posição original
                    board.chessboard[piece.row][piece.col] = piece  # Atualiza a posição da peça no tabuleiro

                    max_eval = max(max_eval, eval)  # Atualiza o melhor valor encontrado
                    alpha = max(alpha, eval)  # Atualiza o valor de Alpha

                    if beta <= alpha:
                        break  # Pruning (poda Alpha-Beta)

            return max_eval  # Retorna o melhor valor encontrado
        else:
            # Jogador Minimizador (oponente)
            min_eval = float('inf')  # Inicializa com o maior valor possível
            for i, piece in enumerate(legal_pieces):
                for move in legal_moves[i]:
                    # Itera sobre cada possível movimento
                    # Efetua o movimento
                    previous_row = piece.row
                    previous_col = piece.col
                    board.chessboard[piece.row][piece.col] = None  # Remove a peça da posição atual
                    piece.move(move[0], move[1], board)  # Move a peça para a nova posição
                    board.chessboard[piece.row][piece.col] = piece  # Atualiza a posição da peça no tabuleiro

                    # Calcula o valor do nó filho recursivamente
                    eval = self.minimax(board, depth - 1, True, alpha, beta, turn, evaluation_func)

                    # Desfaz o movimento
                    board.chessboard[piece.row][piece.col] = None  # Remove a peça da nova posição
                    piece.move(previous_row, previous_col, board)  # Move a peça de volta para a posição original
                    board.chessboard[piece.row][piece.col] = piece  # Atualiza a posição da peça no tabuleiro

                    min_eval = min(min_eval, eval)  # Atualiza o melhor valor encontrado
                    beta = min(beta, eval)  # Atualiza o valor de Beta

                    if beta <= alpha:
                        break  # Pruning (poda Alpha-Beta)

            return min_eval  # Retorna o melhor valor encontrado

    def execute_minimax(self, board, depth, turn, evaluation_func):
        """
        Executa o algoritmo Minimax para determinar o melhor movimento.

        Args:
            board (Board): O estado atual do tabuleiro.
            depth (int): A profundidade da árvore de busca.
            turn (int): A cor do jogador atual.
            evaluation_func (int): Qual função de avaliação usar (1, 2 ou 3).

        Returns:
            tuple: Uma tupla contendo a posição da peça e o movimento a ser realizado.
        """
        legal_pieces, legal_moves = board.find_available_moves(turn)  # Encontra movimentos legais
        best_eval = float('-inf')  # Inicializa com o menor valor possível
        best_move = None
        best_piece = None

        board_copy = deepcopy(board)  # Cria uma cópia do tabuleiro
        legal_pieces_copy, legal_moves_copy = board_copy.find_available_moves(turn)  # Encontra movimentos legais na cópia

        for i, piece in enumerate(legal_pieces_copy):
            # Itera sobre cada peça legal
            for move in legal_moves_copy[i]:
                # Itera sobre cada movimento legal para a peça
                # Efetua o movimento
                previous_row = piece.row
                previous_col = piece.col
                board_copy.chessboard[piece.row][piece.col] = None  # Remove a peça da posição atual
                piece.move(move[0], move[1], board_copy)  # Move a peça para a nova posição

                board_copy.chessboard[piece.row][piece.col] = piece  # Atualiza a posição da peça no tabuleiro

                # Calcula o valor do nó filho recursivamente
                eval = self.minimax(deepcopy(board_copy), depth - 1, True, float('-inf'), float('inf'), turn, evaluation_func)

                # Desfaz o movimento
                board_copy.chessboard[piece.row][piece.col] = None  # Remove a peça da nova posição
                piece.move(previous_row, previous_col, board_copy)  # Move a peça de volta para a posição original
                board_copy.chessboard[piece.row][piece.col] = piece  # Atualiza a posição da peça no tabuleiro

                if eval > best_eval:
                    # Se o valor for melhor que o melhor valor encontrado até agora
                    best_eval = eval  # Atualiza o melhor valor
                    best_move = move  # Atualiza o melhor movimento
                    best_piece = legal_pieces[i]  # Atualiza a melhor peça

        return (best_piece.row, best_piece.col), best_move  # Retorna a posição da peça e o melhor movimento

    def evaluate(self, board, turn):
        """
        Função de avaliação heurística para o estado do tabuleiro.

        Args:
            board (Board): O estado do tabuleiro a ser avaliado.
            turn (int): A cor do jogador atual.

        Returns:
            float: Um valor heurístico representando a qualidade do estado do tabuleiro para o jogador atual.
        """
        score = 0

        # Contagem de Peças
        white_pieces = len(board.all_pieces_white)
        black_pieces = len(board.all_pieces_black)
        score += white_pieces - black_pieces if turn == WHITE else black_pieces - white_pieces

        # Contagem de Damas
        white_kings = sum(piece.king for piece in board.all_pieces_white)
        black_kings = sum(piece.king for piece in board.all_pieces_black)
        score += (white_kings - black_kings) * 2 if turn == WHITE else (black_kings - white_kings) * 2

        # Controlo do Tabuleiro (posição das peças)
        for piece in board.all_pieces_white:
            if turn == WHITE:
                # score += piece.row  # Favoriza as linhas mais altas para as peças brancas
                score += (board.size - 1 - piece.row) # Favoriza as linhas mais altas para as peças brancas
            else:
                score -= (board.size - 1 - piece.row)  # Favoriza as linhas mais baixas para as peças pretas

        for piece in board.all_pieces_black:
            if turn == BLACK:
                # score += (board.size - 1 - piece.row)  # Favoriza as linhas mais altas para as peças pretas
                score += piece.row # Favoriza as linhas mais altas para as peças pretas
            else:
                score -= piece.row  # Favoriza as linhas mais baixas para as peças brancas

        return score

    def evaluate_2(self, board, turn):
        """
        Função de avaliação heurística simplificada (apenas contagem de peças).

        Args:
            board (Board): O estado do tabuleiro.
            turn (int): A cor do jogador atual.

        Returns:
            float: Um valor heurístico baseado na contagem de peças.
        """
        score = 0

        # Contagem de Peças
        white_pieces = len(board.all_pieces_white)
        black_pieces = len(board.all_pieces_black)
        score += white_pieces - black_pieces if turn == WHITE else black_pieces - white_pieces
        return score

    def evaluate_3(self, board, turn):
        """
        Função de avaliação heurística com contagem de peças e damas (damas tem peso maior).

        Args:
            board (Board): O estado do tabuleiro.
            turn (int): A cor do jogador atual.

        Returns:
            float: Um valor heurístico baseado na contagem de peças e damas.
        """
        score = 0

        # Contagem de Peças
        white_pieces = len(board.all_pieces_white)
        black_pieces = len(board.all_pieces_black)
        score += white_pieces - black_pieces if turn == WHITE else black_pieces - white_pieces

        # Contagem de Damas
        white_kings = sum(piece.king for piece in board.all_pieces_white)
        black_kings = sum(piece.king for piece in board.all_pieces_black)
        score += (white_kings - black_kings) * 5 if turn == WHITE else (black_kings - white_kings) * 5
        return score


class MCTSNode:
    """
    Representa um nó na árvore de busca Monte Carlo Tree Search (MCTS).
    """

    def __init__(self, state, parent=None):
        """
        Inicializa um novo nó MCTS.

        Args:
            state (Board): O estado do tabuleiro associado ao nó.
            parent (MCTSNode): O nó pai (se houver).
        """
        self.state = state  # Estado do tabuleiro
        self.parent = parent  # Nó pai
        self.children = []  # Lista de nós filhos
        self.visits = 0  # Número de vezes que o nó foi visitado
        self.reward = 0  # Recompensa acumulada (resultados das simulações)


class MontecarloTreeSearch:
    """
    Implementação do algoritmo Monte Carlo Tree Search (MCTS).
    """

    def __init__(self, iterations, exploration_weight=1.4):
        """
        Inicializa o objeto MontecarloTreeSearch.

        Args:
            iterations (int): O número de iterações para executar a busca MCTS.
            exploration_weight (float): O peso da exploração no cálculo do UCB (Upper Confidence Bound).
        """
        self.iterations = iterations
        self.exploration_weight = exploration_weight

    def expand(self, node):
        """
        Expande um nó adicionando um novo nó filho aleatório.

        Args:
            node (MCTSNode): O nó a ser expandido.

        Returns:
            MCTSNode: O novo nó filho criado.
        """
        new_state = deepcopy(node.state)  # Cria uma cópia do estado atual do tabuleiro
        new_legal_pieces, new_legal_moves = new_state.find_available_moves(new_state.turn)  # Encontra os movimentos legais no novo estado

        # Escolhe um movimento aleatório
        random_piece_index = random.choice(range(len(new_legal_pieces)))
        random_piece = new_legal_pieces[random_piece_index]
        random_move_index = random.choice(range(len(new_legal_moves[random_piece_index])))
        random_move = new_legal_moves[random_piece_index][random_move_index]

        # Realiza o movimento no novo estado
        new_state.chessboard[random_piece.row][random_piece.col] = None
        random_piece.move(random_move[0], random_move[1], new_state)
        new_state.chessboard[random_piece.row][random_piece.col] = random_piece

        # Verifica se tem capturas
        if random_piece.has_caught and not random_piece.king:
            random_piece.check_catch(new_state)
            if random_piece.legal:
                new_state.turn = WHITE if new_state.turn == WHITE else BLACK
            else:
                new_state.turn = WHITE if new_state.turn == BLACK else BLACK

        elif random_piece.has_caught and random_piece.king:
            random_piece.check_catch_king(new_state)
            if random_piece.legal:
                new_state.turn = WHITE if new_state.turn == WHITE else BLACK
            else:
                new_state.turn = WHITE if new_state.turn == BLACK else BLACK

        else:
            new_state.turn = WHITE if new_state.turn == BLACK else BLACK

        if random_piece.legal and random_piece.has_caught:
            pass # Mantém o turno se ainda houver capturas disponíveis
        else:
            random_piece.transform_king() # Transforma em dama se chegar ao final do tabuleiro

        new_state.check_winner()

        new_node = MCTSNode(new_state, parent=node)  # Cria um novo nó com o novo estado
        node.children.append(new_node)  # Adiciona o novo nó como filho do nó atual
        return new_node

    def select(self, node):
        """
        Seleciona um nó para expandir com base na política UCB (Upper Confidence Bound).

        Args:
            node (MCTSNode): O nó a partir do qual iniciar a seleção.

        Returns:
            MCTSNode: O nó selecionado para expansão.
        """
        n_children = node.state.count_possible_moves()
        if not node.children or len(node.children) < n_children:
            return node

        selected_child = max(node.children, key=lambda child: self.ucb_score(child))
        return self.select(selected_child)

    def ucb_score(self, node):
        """
        Calcula a pontuação UCB para um nó.

        Args:
            node (MCTSNode): O nó para o qual calcular a pontuação UCB.

        Returns:
            float: A pontuação UCB do nó.
        """
        # O fator de exploração influencia o quanto o algoritmo explora novos nós vs. explora nós já conhecidos.
        # Um valor mais alto incentiva a exploração.
        self.exploration_weight = 1.4  # Pode ser necessário ajustar este parâmetro para melhor desempenho
        return node.reward / node.visits + self.exploration_weight * math.sqrt(math.log(node.parent.visits) / node.visits)

    def simulate(self, node, initial_turn):
        """
        Simula um jogo a partir do estado do nó.

        Args:
            node (MCTSNode): O nó a partir do qual iniciar a simulação.
            initial_turn (int): O turno inicial da simulação.

        Returns:
            int: 1 se o jogador inicial venceu a simulação, -1 se perdeu, 0 se empatou.
        """
        current_state = deepcopy(node.state)

        winner = current_state.check_winner()
        if (winner == 'Player 1' and initial_turn == WHITE) or (winner == 'Player 2' and initial_turn == BLACK):
            return 1
        elif (winner == 'Player 1' and initial_turn == BLACK) or (winner == 'Player 2' and initial_turn == WHITE):
            return -1
        elif winner == 'Tie':
            return 0

        while True:

            winner = current_state.check_winner()
            if (winner == 'Player 1' and initial_turn == WHITE) or (winner == 'Player 2' and initial_turn == BLACK):
                return 1
            elif (winner == 'Player 1' and initial_turn == BLACK) or (winner == 'Player 2' and initial_turn == WHITE):
                return -1
            elif winner == 'Tie':
                return 0

            legal_pieces, legal_moves = current_state.find_available_moves(current_state.turn)
            random_piece_index = random.choice(range(len(legal_pieces)))
            random_piece = legal_pieces[random_piece_index]
            random_move_index = random.choice(range(len(legal_moves[random_piece_index])))
            random_move = legal_moves[random_piece_index][random_move_index]
            current_state.chessboard[random_piece.row][random_piece.col] = None
            current_piece_row = random_piece.row
            current_piece_col = random_piece.col
            random_piece.move(random_move[0], random_move[1], current_state)
            current_state.chessboard[random_piece.row][random_piece.col] = random_piece

            # Verifica se há outras peças para capturar
            if not random_piece.king:
                random_piece.check_catch(current_state)
            else:
                random_piece.check_catch_king(current_state)

            if random_piece.legal and random_piece.has_caught:
                pass # Mantém o turno se ainda houver capturas disponíveis

            else:
                random_piece.transform_king()
                if current_state.turn == WHITE:
                    current_state.turn = BLACK
                else:
                    current_state.turn = WHITE

    def backpropagate(self, node, result):
        """
        Atualiza as estatísticas do nó com o resultado da simulação e propaga para os nós pais.

        Args:
            node (MCTSNode): O nó a ser atualizado.
            result (int): O resultado da simulação (1, -1 ou 0).
        """
        node.visits += 1  # Incrementa o número de visitas
        node.reward += result  # Adiciona a recompensa
        if node.parent:
            # node.parent.backpropagate(result)
            self.backpropagate(node.parent, result)  # Propaga a atualização para o nó pai

    def mcts(self, root_state, turn):
        """
        Executa o algoritmo MCTS para determinar o melhor movimento.

        Args:
            root_state (Board): O estado inicial do tabuleiro.
            turn (int): A cor do jogador atual.

        Returns:
            tuple: Uma tupla que contem a posição da peça e o movimento a ser realizado.
        """
        root_state.turn = turn  # Associa o turno ao estado raiz
        root = MCTSNode(root_state)  # Cria o nó raiz
        for _ in range(self.iterations):
            node = root

            # Fase de Seleção
            while not node.state.is_terminal:  # Enquanto o estado não for terminal
                n_children = node.state.count_possible_moves()
                if len(node.children) < n_children:
                    # Expandir
                    node = self.expand(node)  # Expande o nó
                    break
                else:  # Expansão Máxima
                    # Seleção
                    # print('Init')
                    node = self.select(node)  # Seleciona o próximo nó
                    # print('End')

            # Fase de Simulação
            reward = self.simulate(node, turn)  # Simula um jogo a partir do nó

            # Fase de Retropropagação
            self.backpropagate(node, reward)  # Atualiza as estatísticas dos nós

        # Seleciona o nó filho com o maior número de visitas
        best_piece_pos = max(root.children, key=lambda child: child.visits).state.last_moved_piece.previous_position
        best_move = max(root.children, key=lambda child: child.visits).state.last_move
        return best_piece_pos, best_move  # Retorna a posição da peça e o melhor movimento encontrado