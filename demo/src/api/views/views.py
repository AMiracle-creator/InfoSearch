import os
from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from api.service.genertate_inverted_index import InvertedIndexService
from api.service.parse_html import ParseHtml
from api.service.search_pages import search_pages
from api.service.vectorize_generate import VectorizeGenerate
from demo.settings import BASE_DIR


def main_page(request):
    if request.method == 'POST':
        search = request.POST.get('search')

        return custom_redirect('search', kwargs={'search': search})
    return render(request, "index.html")


def custom_redirect(url_name, kwargs):
    url = reverse(url_name)
    params = urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


def result_search(request):
    context = {
        "pages": [],
        "search": ''
    }

    if request.method == 'POST':
        search = request.POST.get('search')

        if search != '':
            result = search_pages(search)
            context["pages"] = result
            context["search"] = search

        return render(request, 'output.html', context)

    queryDict = dict(request.GET)
    search = ""

    try:
        search = queryDict['search'][0]
    except KeyError as e:
        search = ''

    if search != '':
        result = search_pages(search)
        context["pages"] = result
        context["search"] = search

    return render(request, 'output.html', context)


def generate_page(request):
    path_to_lemmas = os.path.join(BASE_DIR, 'api/static/lemmas.txt')
    path_to_tokens = os.path.join(BASE_DIR, 'api/static/tokens.txt')
    path_tf_idf_lemmas = os.path.join(BASE_DIR, 'api/static/lemmas')
    path_tf_idf_tokens = os.path.join(BASE_DIR, 'api/static/tokens')

    vectorize_generate = VectorizeGenerate(path_to_lemmas=path_to_lemmas,
                                           path_to_tokens=path_to_tokens,
                                           path_tf_idf_lemmas=path_tf_idf_lemmas,
                                           path_tf_idf_tokens=path_tf_idf_tokens)

    vectorize_generate.vectorize_pages()
    return render(request, "generate_vectors.html")


def generate_index(request):
    path_to_index = os.path.join(BASE_DIR, 'api/static/inverted_index.txt')

    generate_index_service = InvertedIndexService(path_to_index)

    generate_index_service.generate()
    return render(request, "generate_index.html")


def parse_html(request):
    path_to_html = os.path.join(BASE_DIR, 'api/static/html')
    path_to_sites = os.path.join(BASE_DIR, 'api/static/sites.txt')

    parse_html = ParseHtml(path_to_html, path_to_sites)
    parse_html.set_sites_dict()
    parse_html.parse_site()

    return render(request, "generate_html.html")
