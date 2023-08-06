import math
import nltk
import numpy as np
import pandas as pd
import re
import sys
import torch
import warnings

warnings.filterwarnings("ignore")

from collections import defaultdict, Counter
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from scipy.sparse import csr_matrix
from sentence_transformers import SentenceTransformer, util
from sklearn.preprocessing import normalize
from tqdm import tqdm

def print_error(status, func_name, message):
    print(status + "|" + func_name + "|" + message)

def custom_tokenizer(sent):
    """
    Args:
        sent (str): Target sentence
    Func:
        Tokenize sentence and filter out not-necessary tokens.
        This function would be used only when embedding == False.
    """
    # |sent| = "I love to go to school."
    word_tokens = word_tokenize(sent)
    # |word_tokens| = ["I", "love", "to", ...]

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    word_tokens = [token for token in word_tokens if not token.lower() in stop_words]

    # Remove special cases
    regex = re.compile(r'[.(),%:]$')
    word_tokens = [token for token in word_tokens if not regex.search(token)]

    # Get verb and noun, adjective, adverb through part-of-speech analysis
    pos_tags = nltk.pos_tag(word_tokens)
    word_tokens = [token for token, pos in pos_tags if (
            'NN' in pos or 'VB' in pos or 'JJ' in pos or 'RB' in pos
    )]

    # Lemmatize word
    lemmatizer = nltk.WordNetLemmatizer()
    word_tokens = [lemmatizer.lemmatize(token) for token in word_tokens]
    return word_tokens

def calc_similarity(sent_i, sent_j, mode="frequency"):
    """
    Args:
        sent_i (str): first sentence
        sent_j (str): second sentence
        mode (str): calculate the similarity of two sentences based on frequency counting or cosine distance. Must select one of ["frequency", "cosine"].
    Func:
        Calculate similarity between two sentences.
        This function would be used only when embedding == False.
    """

    func_name = sys._getframe().f_code.co_name

    # |sent_i| = [token1, token2, ..., token_n]
    # |sent_j| = [token1, token2, ..., token_n]

    num_tokens_i = len(sent_i)
    num_tokens_j = len(sent_j)

    if (num_tokens_i <= 1) or (num_tokens_j <= 1):
        return 0

    if mode.lower() not in ["frequency", "cosine"]:
        print_error("Fail", func_name, "Please type in the appropriate mode.")
        raise ValueError

    if mode.lower() == "frequency":
        common = len(set(sent_i).intersection(set(sent_j)))
        base = math.log(num_tokens_i) + math.log(num_tokens_j)
        return common / base

    elif mode.lower() == "cosine":
        sent_i = Counter(sent_i)
        sent_j = Counter(sent_j)

        # norm of sent_i and sent_j
        norm_i = math.sqrt(sum(v ** 2 for v in sent_i.values()))
        norm_j = math.sqrt(sum(v ** 2 for v in sent_j.values()))
        prod = 0

        for k, v in sent_i.items():
            prod += v * sent_j.get(k, 0)
        return prod / (norm_i * norm_j)


class KeySentenceExtractor(object):

    def __init__(self):
        super(KeySentenceExtractor, self).__init__()

    def tokenize_doc(self, doc):
        """
        Args:
            doc (str): Target document
        Func:
            Tokenize document into sentence using NLTK sentence tokenizer.
        """

        func_name = sys._getframe().f_code.co_name
        try:
            sents = sent_tokenize(doc)
        except Exception as e:
            print_error("Fail", func_name, e)

        return sents

    def build_vocabs(self, sents, min_freq, tokenizer, **kwargs):
        """
        Args:
            sents (list): Tokenized document per sentence
            min_freq (int): Minimum frequency to be included in the vocabs
            tokenizer (function): Tokenization function
            kwargs: parameters passed to tokenizer
        Func:
            Build vocabularies of the document.
        """

        func_name = sys._getframe().f_code.co_name

        try:
            vocabs = defaultdict(int)
            word_tokens_per_sent = []

            for sent in sents:
                word_tokens = tokenizer(sent, **kwargs)
                word_tokens_per_sent += [word_tokens]
                for token in word_tokens:
                    vocabs[token] += 1

            # Filter out the words of which frequency < min_freq
            vocabs = dict(filter(lambda elem:elem[1] >= min_freq, vocabs.items()))
        except Exception as e:
            print_error("Fail", func_name, e)

        return vocabs, word_tokens_per_sent

    def adjust_bias(self, n_sents, position, rate):
        """
        Args:
            n_sents (int): The number of sentences in the document
            position (str): The emphasis position of the document ("begin" or "end")
            rate (int or float): The emphasis rate (default = 5)
        Func:
            Add bias to each node.
        """
        func_name = sys._getframe().f_code.co_name

        try:
            bias = np.ones(n_sents)
            # |bias| = (n_sents, )

            if position == "begin":
                bias[0] = rate
            elif position == "end":
                bias[-1] = rate
        except Exception as e:
            print_error("Fail", func_name, e)

        return bias

    def build_node_edge_matrix(self,
                               word_tokens_per_sent,
                               directed,
                               min_sim,
                               mode):
        """
        Args:
            word_tokens_per_sent (list): list of Tokenized sentences
            directed (bool): set as True to not create an edge with previous sentences
            min_sim (float): minimum similarity to create an edge
            mode (str): metrics to calculate the similarity when not using embedding ("cosine" or "frequency")
        Func:
            Build node and edge based on sentence similarity.
        """

        self.saved = None


        func_name = sys._getframe().f_code.co_name

        rows, cols, sims = [], [], []
        n_sents = len(word_tokens_per_sent)

        try:
            if directed:
                for i, sent_i in enumerate(word_tokens_per_sent):
                    for j, sent_j in enumerate(word_tokens_per_sent):
                        if i >= j:
                            continue
                        sim = calc_similarity(sent_i, sent_j, mode=mode)
                        if sim < min_sim:
                            continue
                        rows.append(i)
                        cols.append(j)
                        sims.append(sim)

                # Normalize similarity matrix
                node_edge_matrix = csr_matrix((sims, (rows, cols)), shape=(n_sents, n_sents))
                node_edge_matrix = normalize(node_edge_matrix, axis=0, norm='l2')
                # |node_edge_matrix| = (n_sents, n_sents)

            else:
                for i, sent_i in enumerate(word_tokens_per_sent):
                    for j, sent_j in enumerate(word_tokens_per_sent):
                        if i == j:
                            continue
                        sim = calc_similarity(sent_i, sent_j, mode=mode)
                        if sim < min_sim:
                            continue
                        rows.append(i)
                        cols.append(j)
                        sims.append(sim)

                # Get similarity matrix
                node_edge_matrix = csr_matrix((sims, (rows, cols)), shape=(n_sents, n_sents))
                # |node_edge_matrix| = (n_sents, n_sents)

        except Exception as e:
            print_error("Fail", func_name, e)

        return node_edge_matrix.toarray()

    def rank(self,
             graph,
             max_epoch,
             damping_factor,
             bias,
             early_stop):
        """
        Args:
            graph (list): nodes are sentences are connected with edges based on similarity
            max_epoch (int): maximum epoch in training
            damping_factor (float): damping factor in pagerank calculation
            bias (ndarray): bias to be applied to each sentence (bias.shape = (n_sents, ))
        Func:
            Calculate pagerank through iteration based on Markov Chains.
        """

        # |bias| = (n_sents, )
        # |node_edge_matrix| = (n_sents, n_sents)

        func_name = sys._getframe().f_code.co_name

        try:

            # Initialize pagerank and previous pagerank
            pagerank = np.ones(graph.shape[0]).reshape(-1, 1)
            prev_pagerank = np.zeros(graph.shape[0]).reshape(-1, 1)
            # |pagerank| = (n_sents, 1)

            # Position bias
            if bias is None:
                bias = (1 - damping_factor) * np.ones(graph.shape[0]).reshape(-1, 1)
                # |bias| = (n_sents, 1)
            else:
                bias = bias.reshape(-1, 1)
                bias = graph.shape[0] * bias / bias.sum()
                bias = (1 - damping_factor) * bias
                # |bias| = (n_sents, 1)

            # Train pagerank
            for epoch in range(max_epoch):
                pagerank = damping_factor * np.dot(graph, pagerank) + bias

                if early_stop:
                    loss = sum(abs(prev_pagerank - pagerank))
                    if loss < 1e-4:
                        break

                prev_pagerank = pagerank
            # |pagerank| = (n_sents, 1)

        except Exception as e:
            print_error("Fail", func_name, e)

        return pagerank

    def extract_topk_sents(self, sents, pagerank, topk):
        """
        Args:
            sents (list): Tokenized document per sentence
            pagerank (ndarray): Pageranks of each sentence (pagerank.shape = (n_sents, ))
            topk (int): Maximum number of sentences to be extracted
        Func:
            Extract key sentences based on pagerank scores.
        """

        func_name = sys._getframe().f_code.co_name

        try:

            topk = min(topk, math.ceil(len(sents) * 0.2))
            idx_to_sentence = {idx:sent for idx, sent in enumerate(sents)}
            # |itos| = {idx:sent}
            extracted_sents_idx = pagerank.argsort(axis=0)[-topk: ].flatten()
            # |extracted_sents_idx| = array([top_n_idx, ..., top_2_idx, top_1_idx])

            # Extract the topk sentences in order
            extracted_sents_idx = sorted(extracted_sents_idx)
            extracted_sents = {idx:idx_to_sentence[idx] for idx in extracted_sents_idx}

        except Exception as e:
            print_error("Fail", func_name, e)

        return extracted_sents

    def summarize(self,
                  doc,
                  embedding,
                  min_freq=1,
                  tokenizer=custom_tokenizer,
                  directed=True,
                  min_sim=.1,
                  mode="frequency",
                  pos_emph=None,
                  emph_rate=None,
                  max_epoch=100,
                  damping_factor=.85,
                  early_stop=True,
                  topk=2):
        """
        Args:
            doc (str): Target document
            embedding (bool): Calculate similarities through embedding sentences (sentence transformer). Default = False
            min_freq (int): Minimum frequency to be included in the vocabs. Default = 1
                If embedding == True, min_freq will be ignored
            tokenizer (function): Tokenization function. Default = custom_tokenizer
                If embedding == True, tokenizer will be ignored
            directed (bool): Whether to build edge with previous sentences. Default = True
                If embedding == True, directed will be ignored
            min_sim (float): Minimum similarity to create an edge. Default = .1
            mode (str): metrics to calculate the similarity ("cosine" or "frequency"). Default = "frequency"
                If embedding == True, mode will be ignored
            pos_emph (str): The emphasis position of the document ("begin" or "end"). Default = None
            emph_rate (int or float): The rate of emphasis. Default = None.
                If pos_emph == True but emph_rate is None, default emph_rate will be set as 5
            position (str): The emphasis position of the document ("begin" or "end")
            rate (int or float): The emphasis rate. Default = 5
            max_epoch (int): Maximum number of epochs in training. Default = 100
            damping_factor (float): Damping factor in pagerank calculation. Default = .85
            early_stop (bool): Whether to stop iteration pf pagerank calculation if the loss < 1e-2. Default = True
            topk (int): Maximum number of sentences to be extracted. Default = 2
        Func:
            Extract key sentences based on pagerank scores.
        """

        sents = self.tokenize_doc(doc)

        if embedding:
            SBERT = SentenceTransformer('all-MiniLM-L6-v2')
            embedded_sentences = SBERT.encode(sents)
            node_edge_matrix = util.cos_sim(embedded_sentences, embedded_sentences)
            n_sents = node_edge_matrix.size(0)

            if directed:
                # generate mask
                mask = torch.ones((n_sents, n_sents))
                for i in range(n_sents):
                    for j in range(n_sents):
                        if i < j:
                            mask[i, j] = 0
                mask = mask.bool()

                # mask fill
                node_edge_matrix.masked_fill_(mask, 0)
                # filter min_sim
                node_edge_matrix = torch.where(node_edge_matrix > min_sim, node_edge_matrix, 0)
                # normalize matrix - applied
                node_edge_matrix = normalize(node_edge_matrix, axis=0, norm='l2')
            else:
                # generate mask
                mask = torch.eye(n_sents).bool()
                # mask fill
                node_edge_matrix.masked_fill_(mask, 0)
                # filter min_sim
                node_edge_matrix = torch.where(node_edge_matrix > min_sim, node_edge_matrix, 0)

        else:
            vocabs, word_tokens_per_sent = self.build_vocabs(sents,
                                                             min_freq = min_freq,
                                                             tokenizer = tokenizer)

            node_edge_matrix = self.build_node_edge_matrix(word_tokens_per_sent,
                                                           directed = directed,
                                                           min_sim = min_sim,
                                                           mode = mode)

        if pos_emph is not None:
            emph_rate = emph_rate if emph_rate is not None else 5
            bias = self.adjust_bias(n_sents = len(sents),
                                    position = pos_emph,
                                    rate = emph_rate)
        else:
            bias = None

        pagerank = self.rank(node_edge_matrix,
                             max_epoch = max_epoch,
                             damping_factor = damping_factor,
                             early_stop = early_stop,
                             bias=bias)

        topk_sents = self.extract_topk_sents(sents = sents,
                                             pagerank = pagerank,
                                             topk = topk)

        return topk_sents