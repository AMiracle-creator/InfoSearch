import numpy as np

import spacy


class VectorizeSearch:
    def __init__(self, path_to_lemmas, path_to_tokens, pages_vectors):
        self.nlp = spacy.load("ru_core_news_sm")
        self.path_to_lemmas = path_to_lemmas
        self.path_to_tokens = path_to_tokens
        self.lemmas = []
        self.pages_vectors = pages_vectors

    @staticmethod
    def read_lemmas(path_to_lemmas):
        lemmas = []
        with open(path_to_lemmas, 'r', encoding='utf-8') as file:
            for line in file:
                lemmas_split = line.split(" ")
                lemmas.append(lemmas_split[0])

        return lemmas

    @staticmethod
    def words_vectorize(lemmas, words, nlp):
        word_weight = len(words) / len(lemmas)
        word_vector = [0] * len(lemmas)

        for word in words:
            try:
                word_vector[lemmas.index(nlp(word)[0].lemma_)] = word_weight
            except Exception as e:
                pass

        return word_vector

    @staticmethod
    def count_cosine_similarity(page_vector, words_vector):
        scalar_vectors = np.dot(page_vector, words_vector)

        similarity = scalar_vectors / np.linalg.norm(words_vector) * np.linalg.norm(page_vector)

        return similarity

    def search(self, request):
        self.lemmas = self.read_lemmas(self.path_to_lemmas)
        words_vector = self.words_vectorize(self.lemmas, request.split(" "), self.nlp)

        result_search = []

        for key in self.pages_vectors:
            page_vector = [float(i) for i in key.vector]
            page_num = key.name.split("_")[1].strip(".txt")

            similarity = self.count_cosine_similarity(page_vector, words_vector)

            if not np.isnan(similarity) and similarity != 0.0:
                result_search.append((page_num, similarity))

        return sorted(result_search, key=lambda x: x[1], reverse=True)
