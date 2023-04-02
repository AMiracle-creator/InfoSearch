import spacy

from api.models import InvertedIndex


class InvertedIndexSearch:
    def __init__(self):
        self.nlp = spacy.load("ru_core_news_sm")

    def search_pages(self, query):
        pages_union = []

        words = []

        try:
            words = [self.nlp(word.lower()).text for word in query.split(" ")]
        except Exception as e:
            pass

        inverted_indexes = InvertedIndex.objects.filter(token__in=words)

        pages = [page_array.pages for page_array in inverted_indexes]

        for page in pages:

            if len(pages_union) == 0:
                pages_union = page
            else:
                pages_union = list(set(pages_union) | set(page))

        return pages_union


class InvertedIndexService:
    def __init__(self, path):
        self.path_inverted_index = path

    def generate(self):
        with open(self.path_inverted_index, 'r', encoding='utf-8') as file:
            for line in file:
                line_split = line.strip("\n").strip('').split(" ")

                pages = [int(i) for i in line_split[1:] if i != '']

                obj, created = InvertedIndex.objects.update_or_create(token=line_split[0], pages=pages)
