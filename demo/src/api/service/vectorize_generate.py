import os
import spacy

from api.models import VectorizeModel


class VectorizeGenerate:
    def __init__(self, path_to_lemmas, path_to_tokens, path_tf_idf_tokens, path_tf_idf_lemmas):
        self.nlp = spacy.load("ru_core_news_sm")
        self.path_to_lemmas = path_to_lemmas
        self.path_to_tokens = path_to_tokens
        self.path_tf_idf_lemmas = path_tf_idf_lemmas
        self.path_tf_idf_tokens = path_tf_idf_tokens
        self.lemmas = []
        self.pages_dict = {}

    @staticmethod
    def read_lemmas(path_to_lemmas):
        lemmas = []
        with open(path_to_lemmas, 'r', encoding='utf-8') as file:
            for line in file:
                lemmas_split = line.split(" ")
                lemmas.append(lemmas_split[0])

        return lemmas

    @staticmethod
    def read_tf_idf(path_lemmas_tf_idf, lemmas, nlp):
        for file in os.listdir(path_lemmas_tf_idf):
            with open(f"{path_lemmas_tf_idf}/{file}", 'r', encoding="utf-8") as f:
                page_num = file.split("_")[1].strip(".txt")
                page_array = [0] * len(lemmas)

                for line in f:
                    line_split = line.split(" ")
                    word = line_split[0]
                    try:
                        page_array[lemmas.index(nlp(word)[0].lemma_)] = float(line_split[2])
                    except Exception as e:
                        pass

                obj, created = VectorizeModel.objects.update_or_create(name=file, vector=page_array, page_number=page_num)
            print(f'ready {file}')

    def vectorize_pages(self):
        self.lemmas = self.read_lemmas(self.path_to_lemmas)
        self.read_tf_idf(self.path_tf_idf_lemmas, self.lemmas, self.nlp)