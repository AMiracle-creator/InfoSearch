import spacy

from collections import defaultdict
from nltk.corpus import stopwords
from bs4 import BeautifulSoup


nlp = spacy.load("ru_core_news_sm")
docs_ids = set()
indexes = defaultdict(set)
stopwords = stopwords.words("russian")


def write_results(result):
    with open('result.txt', 'a', encoding='utf-8') as file:
        file.write(result + '\n')


def generate_indexes():
    for i in range(1, 101):
        docs_ids.add(i)
        with open("loads/выкачка_" + str(i)) as file:
            html = BeautifulSoup(file, features="html.parser")
            process(nlp(str(html.get_text(" ").lower().strip())), i)


def process(doc, doc_id):
    for item in doc:
        if item.is_alpha and not item.like_num and not item.is_punct and item.text not in stopwords:
            indexes[item.lemma_].add(doc_id)


def or_query(first, second):
    result = f'Files matching OR query {indexes[first].union(indexes[second])}'
    write_results(result)

    return result


def and_query(first, second):
    result = f"Files matching AND query {indexes[first].intersection(indexes[second])}"
    write_results(result)

    return result


def not_query(word):
    result = f"Files matching NOT query {docs_ids - indexes[word]}"
    write_results(result)

    return result


def main():
    generate_indexes()
    first_word = "политика"
    second_word = "кино"
    print(or_query(first_word, second_word))
    print(and_query(first_word, second_word))
    print(not_query(first_word))


if __name__ == '__main__':
    main()