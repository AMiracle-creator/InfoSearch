import os
import numpy as np

import spacy
from numpy import linalg as LA

NULL_VECTOR_LEMMAS = []
NULL_VECTOR = []

nlp = spacy.load("ru_core_news_sm")


def all_lemmas():
    with open("lemmas.txt") as f:
        for line in f:
            lemma, _ = line.split(":")
            NULL_VECTOR_LEMMAS.append(lemma)
            NULL_VECTOR.append(0)


all_lemmas()

pages_dict = {}


def main():
    for file in os.listdir('task_4/lemmas'):
        with open(f"task_4/lemmas/{file}", "r") as f:
            page_num = file.split("_")[1].strip(".txt")
            pages_dict[page_num] = [0] * len(NULL_VECTOR_LEMMAS)
            for line in f:
                word, _, tf_idf = line.split()
                try:
                    pages_dict[page_num][NULL_VECTOR_LEMMAS.index(nlp(word)[0].lemma_)] = float(tf_idf)
                except Exception as e:
                    pass
    while True:
        request = input("Введите запрос: ")

        word_weight = len(request.split()) / len(NULL_VECTOR_LEMMAS)
        word_vector = [0] * len(NULL_VECTOR)
        for word in request.split():
            try:
                word_vector[NULL_VECTOR_LEMMAS.index(nlp(word)[0].lemma_)] = word_weight
            except Exception as e:
                pass

        result_array = []
        for key in pages_dict:
            page_vector = pages_dict.get(key)

            scalar_product = np.dot(word_vector, page_vector)
            similarity = scalar_product / (LA.norm(word_vector) * LA.norm(page_vector))
            result_array.append((key, similarity))

        print(sorted(result_array, key=lambda x: x[1], reverse=True))


main()
