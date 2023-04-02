import os

from api.models import VectorizeModel, HtmlInfoModel
from api.service.genertate_inverted_index import InvertedIndexSearch
from api.service.vectorize_search import VectorizeSearch
from demo.settings import BASE_DIR


def search_pages(search):
    path_to_lemmas = os.path.join(BASE_DIR, 'api/static/lemmas.txt')
    path_to_tokens = os.path.join(BASE_DIR, 'api/static/tokens.txt')

    inverted_index_search = InvertedIndexSearch()

    pages_num = inverted_index_search.search_pages(search)

    pages_vector = VectorizeModel.objects.filter(page_number__in=pages_num)

    vectorize_search = VectorizeSearch(path_to_lemmas=path_to_lemmas,
                                       path_to_tokens=path_to_tokens,
                                       pages_vectors=pages_vector)

    result = vectorize_search.search(f'{search}'.lower())

    result_pages = [int(page[0]) for page in result]

    html_pages = HtmlInfoModel.objects.filter(page_number__in=result_pages)

    return html_pages
