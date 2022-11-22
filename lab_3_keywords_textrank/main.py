"""
Lab 3
Extract keywords based on TextRank algorithm
"""
from typing import Optional, Union


class TextPreprocessor:
    """
    A class to preprocess raw text

    ...

    Attributes
    ----------
    _stop_words: tuple[str, ...]
        insignificant words to remove from tokens
    _punctuation: tuple[str, ...]
        punctuation symbols to remove during text cleaning

    Methods
    -------
    _clean_and_tokenize(text: str) -> tuple[str, ...]:
        Removes punctuation, casts to lowercase, splits into tokens.
    _remove_stop_words(tokens: tuple[str, ...] -> tuple[str, ...]:
        Filters tokens, removing stop words
    preprocess_text(text: str) -> tuple[str, ...]:
        Produces filtered clean lowercase tokens from raw text
    """
    # Step 1.1
    def __init__(self, stop_words: tuple[str, ...], punctuation: tuple[str, ...]) -> None:
        """
        Constructs all the necessary attributes for the text preprocessor object

        Parameters
        ----------
            stop_words : tuple[str, ...]
                insignificant words to remove from tokens
            punctuation : tuple[str, ...]
                punctuation symbols to remove during text cleaning
        """
        self._stop_words = stop_words
        self._punctuation = punctuation

    # Step 1.2
    def _clean_and_tokenize(self, text: str) -> tuple[str, ...]:
        """
        Removes punctuation, casts to lowercase, splits into tokens.

        Parameters
        ----------
            text : str
                raw text

        Returns
        -------
            tuple[str, ...]
                clean lowercase tokens
        """
        for sign in self._punctuation:
            text = text.replace(sign, '')
        return tuple(text.lower().split())

    # Step 1.3
    def _remove_stop_words(self, tokens: tuple[str, ...]) -> tuple[str, ...]:
        """
        Filters tokens, removing stop words

        Parameters
        ----------
            tokens : tuple[str, ...]
                tokens containing stop-words

        Returns
        -------
            tuple[str, ...]
                tokens without stop-words
        """
        cleaned_text = []
        for word in tokens:
            if word in self._stop_words:
                continue
            cleaned_text.append(word)
        return tuple(cleaned_text)

    # Step 1.4
    def preprocess_text(self, text: str) -> tuple[str, ...]:
        """
        Produces filtered clean lowercase tokens from raw text

        Parameters
        ----------
            text : str
                raw text

        Returns
        -------
            tuple[str, ...]
                clean lowercase tokens with no stop-words
        """
        return self._remove_stop_words(self._clean_and_tokenize(text))


class TextEncoder:
    """
    A class to encode string sequence into matching integer sequence

    ...

    Attributes
    ----------
    _word2id: dict[str, int]
        maps words to integers
    _id2word: dict[int, str]
        maps integers to words

    Methods
    -------
     _learn_indices(self, tokens: tuple[str, ...]) -> None:
        Fills attributes mapping words and integer equivalents to each other
    encode(self, tokens: tuple[str, ...]) -> Optional[tuple[int, ...]]:
        Encodes input sequence of string tokens to sequence of integer tokens
    decode(self, encoded_tokens: tuple[int, ...]) -> Optional[tuple[str, ...]]:
        Decodes input sequence of integer tokens to sequence of string tokens
    """

    # Step 2.1
    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the text encoder object
        """
        self._word2id = {}
        self._id2word = {}

    # Step 2.2
    def _learn_indices(self, tokens: tuple[str, ...]) -> None:
        """
        Fills attributes mapping words and integer equivalents to each other

        Parameters
        ----------
            tokens : tuple[str, ...]
                sequence of string tokens
        """
        id_lst = [integer for integer in range(1000, len(tokens) + 1001)]
        self._word2id = {token: id_n for (token, id_n) in zip(tokens, id_lst)}
        self._id2word = {id_n: token for (id_n, token) in zip(id_lst, tokens)}


    # Step 2.3
    def encode(self, tokens: tuple[str, ...]) -> Optional[tuple[int, ...]]:
        """
        Encodes input sequence of string tokens to sequence of integer tokens

        Parameters
        ----------
            tokens : tuple[str, ...]
                sequence of string tokens

        Returns
        -------
            tuple[int, ...]
                sequence of integer tokens

        In case of empty tokens input data, None is returned
        """
        if not tokens:
            return None

        self._learn_indices(tokens)
        int_words = tuple((self._word2id[word] for word in tokens))
        return int_words

    # Step 2.4
    def decode(self, encoded_tokens: tuple[int, ...]) -> Optional[tuple[str, ...]]:
        """
        Decodes input sequence of integer tokens to sequence of string tokens

        Parameters
        ----------
            encoded_tokens : tuple[int, ...]
                sequence of integer tokens

        Returns
        -------
            tuple[str, ...]
                sequence of string tokens

        In case of out-of-dictionary input data, None is returned
        """
        for word in encoded_tokens:
            if word not in self._id2word.keys():
                return None

        str_words = tuple((self._id2word[id_n] for id_n in encoded_tokens))
        return str_words


# Step 3
def extract_pairs(tokens: tuple[int, ...], window_length: int) -> Optional[tuple[tuple[int, ...], ...]]:
    """
    Retrieves all pairs of co-occurring words in the token sequence

    Parameters
    ----------
        tokens : tuple[int, ...]
            sequence of tokens
        window_length: int
            maximum distance between co-occurring tokens: tokens are considered co-occurring
            if they appear in the same window of this length

    Returns
    -------
        tuple[tuple[int, ...], ...]
            pairs of co-occurring tokens

    In case of corrupt input data, None is returned:
    tokens must not be empty, window lengths must be integer, window lengths cannot be less than 2.
    """
    if not (tokens and isinstance(window_length, int) and window_length >= 2):
        return None

    window_tokens = tokens[:window_length]
    pairs = []
    start_slice = 0
    for word in tokens:
        for window_word in window_tokens:
            if word == window_word:
                continue

            pair = tuple(sorted((word, window_word)))

            if pair in pairs:
                continue

            pairs.append(pair)
        start_slice += 1
        end_slice = window_length + start_slice
        window_tokens = tokens[start_slice:end_slice]
    return tuple(pairs)


class AdjacencyMatrixGraph:
    """
    A class to represent graph as matrix of adjacency

    ...

    Attributes
    ----------
    _matrix: list[list[int]]
        stores information about vertices interrelation
    _positions: dict[int, list[int]]
        stores information about positions in text

    Methods
    -------
     get_vertices(self) -> tuple[int, ...]:
        Returns a sequence of all vertices present in the graph
     add_edge(self, vertex1: int, vertex2: int) -> int:
        Adds or overwrites an edge in the graph between the specified vertices
     is_incidental(self, vertex1: int, vertex2: int) -> int:
        Retrieves information about whether the two vertices are incidental
     calculate_inout_score(self, vertex: int) -> int:
        Retrieves a number of incidental vertices to a specified vertex
    fill_from_tokens(self, tokens: tuple[int, ...], window_length: int) -> None:
        Updates graph instance with vertices and edges extracted from tokenized text
    fill_positions(self, tokens: tuple[int, ...]) -> None:
        Saves information on all positions of each vertex in the token sequence
    calculate_position_weights(self) -> None:
        Computes position weights for all tokens in text
    get_position_weights(self) -> dict[int, float]:
        Retrieves position weights for all vertices in the graph
    """

    _matrix: list[list[int]]
    _positions: dict[int, list[int]]
    _position_weights: dict[int, float]

    # Step 4.1
    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the adjacency matrix graph object
        """
        self._matrix = []
        self._positions = {}
        self._position_weights = {}
        self._vertices = []


    # Step 4.2
    def add_edge(self, vertex1: int, vertex2: int) -> int:
        """
        Adds or overwrites an edge in the graph between the specified vertices

        Parameters
        ----------
            vertex1 : int
                the first vertex incidental to the added edge
            vertex2 : int
                the second vertex incidental to the added edge

        Returns
        -------
            int
                0 if edge was added successfully, otherwise -1

        In case of vertex1 being equal to vertex2, -1 is returned as loops are prohibited
        """
        if vertex1 == vertex2:
            return -1

        for vertex in vertex1, vertex2:
            if vertex not in self._vertices:
                self._vertices.append(vertex)
                self._matrix.append([0 for _ in range(len(self._vertices))])

        max_len_of_element = len(max(self._matrix, key=len))

        for element in self._matrix:
            if len(element) < max_len_of_element:
                element += [0] * (max_len_of_element - len(element))

        index1 = self._vertices.index(vertex1)
        index2 = self._vertices.index(vertex2)
        self._matrix[index1][index2] = 1
        self._matrix[index2][index1] = 1
        return 0


    # Step 4.3
    def is_incidental(self, vertex1: int, vertex2: int) -> int:
        """
        Retrieves information about whether the two vertices are incidental

        Parameters
        ----------
            vertex1 : int
                the first vertex incidental to the edge sought
            vertex2 : int
                the second vertex incidental to the edge sought

        Returns
        -------
            Optional[int]
                1 if vertices are incidental, otherwise 0

        If either of vertices is not present in the graph, -1 is returned
        """
        for vertex in vertex1, vertex2:
            if vertex not in self._vertices:
                return -1



        return 1

    # Step 4.4
    def get_vertices(self) -> tuple[int, ...]:
        """
        Returns a sequence of all vertices present in the graph

        Returns
        -------
            tuple[int, ...]
                a sequence of vertices present in the graph
        """
        pass

    # Step 4.5
    def calculate_inout_score(self, vertex: int) -> int:
        """
        Retrieves a number of incidental vertices to a specified vertex

        Parameters
        ----------
            vertex : int
                a vertex to calculate inout score for

        Returns
        -------
            int
                number of incidental vertices

        If vertex is not present in the graph, -1 is returned
        """
        pass

    # Step 4.6
    def fill_from_tokens(self, tokens: tuple[int, ...], window_length: int) -> None:
        """
        Updates graph instance with vertices and edges extracted from tokenized text
        Parameters
        ----------
            tokens : tuple[int, ...]
                sequence of tokens
            window_length: int
                maximum distance between co-occurring tokens: tokens are considered co-occurring
                if they appear in the same window of this length
        """
        pass

    # Step 8.2
    def fill_positions(self, tokens: tuple[int, ...]) -> None:
        """
        Saves information about all positions of each vertex in the token sequence
        ----------
            tokens : tuple[int, ...]
                sequence of tokens
        """
        pass

    # Step 8.3
    def calculate_position_weights(self) -> None:
        """
        Computes position weights for all tokens in text
        """
        pass

    # Step 8.4
    def get_position_weights(self) -> dict[int, float]:
        """
        Retrieves position weights for all vertices in the graph

        Returns
        -------
            dict[int, float]
                position weights for all vertices in the graph
        """
        pass


class EdgeListGraph:
    """
    A class to represent graph as a list of edges

    ...

    Attributes
    ----------
    _edges: dict[int, list[int]]
        stores information about vertices interrelation

    Methods
    -------
     get_vertices(self) -> tuple[int, ...]:
        Returns a sequence of all vertices present in the graph
     add_edge(self, vertex1: int, vertex2: int) -> int:
        Adds or overwrites an edge in the graph between the specified vertices
     is_incidental(self, vertex1: int, vertex2: int) -> int:
        Retrieves information about whether the two vertices are incidental
     calculate_inout_score(self, vertex: int) -> int:
        Retrieves a number of incidental vertices to a specified vertex
    fill_from_tokens(self, tokens: tuple[int, ...], window_length: int) -> None:
        Updates graph instance with vertices and edges extracted from tokenized text
    fill_positions(self, tokens: tuple[int, ...]) -> None:
        Saves information on all positions of each vertex in the token sequence
    calculate_position_weights(self) -> None:
        Computes position weights for all tokens in text
    get_position_weights(self) -> dict[int, float]:
        Retrieves position weights for all vertices in the graph
    """

    # Step 7.1
    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the edge list graph object
        """
        pass

    # Step 7.2
    def get_vertices(self) -> tuple[int, ...]:
        """
        Returns a sequence of all vertices present in the graph

        Returns
        -------
            tuple[int, ...]
                a sequence of vertices present in the graph
        """
        pass

    # Step 7.2
    def add_edge(self, vertex1: int, vertex2: int) -> int:
        """
        Adds or overwrites an edge in the graph between the specified vertices

        Parameters
        ----------
            vertex1 : int
                the first vertex incidental to the added edge
            vertex2 : int
                the second vertex incidental to the added edge

        Returns
        -------
            int
                0 if edge was added successfully, otherwise -1

        In case of vertex1 being equal to vertex2, -1 is returned as loops are prohibited
        """
        pass

    # Step 7.2
    def is_incidental(self, vertex1: int, vertex2: int) -> int:
        """
        Retrieves information about whether the two vertices are incidental

        Parameters
        ----------
            vertex1 : int
                the first vertex incidental to the edge sought
            vertex2 : int
                the second vertex incidental to the edge sought

        Returns
        -------
            Optional[int]
                1 if vertices are incidental, otherwise 0

        If either of vertices is not present in the graph, -1 is returned
        """
        pass

    # Step 7.2
    def calculate_inout_score(self, vertex: int) -> int:
        """
        Retrieves a number of incidental vertices to a specified vertex

        Parameters
        ----------
            vertex : int
                a vertex to calculate inout score for

        Returns
        -------
            int
                number of incidental vertices

        If vertex is not present in the graph, -1 is returned
        """
        pass

    # Step 7.2
    def fill_from_tokens(self, tokens: tuple[int, ...], window_length: int) -> None:
        """
        Updates graph instance with vertices and edges extracted from tokenized text
        Parameters
        ----------
            tokens : tuple[int, ...]
                sequence of tokens
            window_length: int
                maximum distance between co-occurring tokens: tokens are considered co-occurring
                if they appear in the same window of this length
        """
        pass

    # Step 8.2
    def fill_positions(self, tokens: tuple[int, ...]) -> None:
        """
        Saves information on all positions of each vertex in the token sequence
        ----------
            tokens : tuple[int, ...]
                sequence of tokens
        """
        pass

    # Step 8.3
    def calculate_position_weights(self) -> None:
        """
        Computes position weights for all tokens in text
        """
        pass

    # Step 8.4
    def get_position_weights(self) -> dict[int, float]:
        """
        Retrieves position weights for all vertices in the graph

        Returns
        -------
            dict[int, float]
                position weights for all vertices in the graph
        """
        pass


class VanillaTextRank:
    """
    Basic TextRank implementation

    ...

    Attributes
    ----------
    _graph: Union[AdjacencyMatrixGraph, EdgeListGraph]
        a graph representing the text
    _damping_factor: float
         probability of jumping from a given vertex to another random vertex
         in the graph during vertices scores calculation
    _convergence_threshold: float
        maximal acceptable difference between the vertices scores in two consequent iteration
    _max_iter: int
        maximal number of iterations to perform
    _scores: dict[int, float]
        scores of significance for all vertices present in the graph


    Methods
    -------
     update_vertex_score(self, vertex: int, incidental_vertices: list[int], scores: dict[int, float]) -> None:
        Changes vertex significance score using algorithm-specific formula
     score_vertices(self) -> dict[int, float]:
        Iteratively computes significance scores for vertices
     get_scores(self) -> dict[int, float]:
        Retrieves importance scores of all tokens in the encoded text
     get_top_keywords(self, n_keywords: int) -> tuple[int, ...]:
        Retrieves top n most important tokens in the encoded text
     """

    _scores: dict[int, float]

    # Step 5.1
    def __init__(self, graph: Union[AdjacencyMatrixGraph, EdgeListGraph]) -> None:
        """
        Constructs all the necessary attributes for the text rank algorithm implementation

        Parameters
        ----------
        graph: Union[AdjacencyMatrixGraph, EdgeListGraph]
            a graph representing the text
        """
        pass

    # Step 5.2
    def update_vertex_score(self, vertex: int, incidental_vertices: list[int], scores: dict[int, float]) -> None:
        """
        Changes vertex significance score using algorithm-specific formula

        Parameters
        ----------
            vertex : int
                a vertex which significance score is updated
            incidental_vertices: list[int]
                vertices incidental to the scored one
            scores: dict[int, float]
                scores of all vertices in the graph
        """
        pass

    # Step 5.3
    def score_vertices(self) -> None:
        """
        Iteratively computes significance scores for vertices

        Returns
        -------
            dict[int, float]:
                scores for all vertices present in the graph
        """
        vertices = self._graph.get_vertices()
        for vertex in vertices:
            self._scores[vertex] = 1.0

        for iteration in range(0, self._max_iter):
            prev_score = self._scores.copy()
            for scored_vertex in vertices:
                incidental_vertices = [vertex for vertex in vertices
                                       if self._graph.is_incidental(scored_vertex, vertex) == 1]
                self.update_vertex_score(scored_vertex, incidental_vertices, prev_score)
            abs_score_diff = [abs(i - j) for i, j in zip(prev_score.values(), self._scores.values())]
            if sum(abs_score_diff) <= self._convergence_threshold:
                break

    # Step 5.4
    def get_scores(self) -> dict[int, float]:
        """
        Retrieves importance scores of all tokens in the encoded text

        Returns
        -------
            dict[int, float]
                importance scores of all tokens in the encoded text
        """
        pass

    # Step 5.5
    def get_top_keywords(self, n_keywords: int) -> tuple[int, ...]:
        """
        Retrieves top n most important tokens in the encoded text

        Returns
        -------
            tuple[int, ...]
                top n most important tokens in the encoded text
        """
        pass


class PositionBiasedTextRank(VanillaTextRank):
    """
    Advanced TextRank implementation: positions of tokens in text are taken into consideration

    ...

    Attributes
    ----------
    _graph: Union[AdjacencyMatrixGraph, EdgeListGraph]
        a graph representing the text
    _damping_factor: float
         probability of jumping from a given vertex to another random vertex
         in the graph during vertices scores calculation
    _convergence_threshold: float
        maximal acceptable difference between the vertices scores in two consequent iteration
    _max_iter: int
        maximal number of iterations to perform
    _scores: dict[int, float]
        scores of significance for all vertices present in the graph
    _position_weights: dict[int, float]
        position weights for all tokens in the text


    Methods
    -------
     update_vertex_score(self, vertex: int, incidental_vertices: list[int], scores: dict[int, float]) -> None:
        Changes vertex significance score using algorithm-specific formula
     score_vertices(self) -> dict[int, float]:
        Iteratively computes significance scores for vertices
     get_scores(self) -> dict[int, float]:
        Retrieves importance scores of all tokens in the encoded text
     get_top_keywords(self, n_keywords: int) -> tuple[int, ...]:
        Retrieves top n most important tokens in the encoded text
    """

    # Step 9.1
    def __init__(self, graph: Union[AdjacencyMatrixGraph, EdgeListGraph]) -> None:
        """
        Constructs all the necessary attributes
        for the position-aware text rank algorithm implementation

        Attributes
        ----------
        graph: Union[AdjacencyMatrixGraph, EdgeListGraph]
            a graph representing the text
        """
        pass

    # Step 9.2
    def update_vertex_score(self, vertex: int, incidental_vertices: list[int], scores: dict[int, float]) -> None:
        """
        Changes vertex significance score using algorithm-specific formula

        Parameters
        ----------
            vertex : int
                a vertex which significance score is updated
            incidental_vertices: list[int]
                vertices incidental to the scored one
            scores: dict[int, float]
                scores of all vertices in the graph
        """
        pass
