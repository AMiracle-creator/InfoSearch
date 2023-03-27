import spacy

from collections import defaultdict
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

nlp = spacy.load("ru_core_news_sm")
docs_ids = set()
indexes = defaultdict(set)
stopwords = stopwords.words("russian")
dict_index = {}


def write_results(result):
    with open('result.txt', 'a', encoding='utf-8') as file:
        file.write(result + '\n')

def write_index():
    with open('inverted_index.txt', 'a', encoding='utf-8') as file:
        result_content = ''
        for key, value in dict_index.items():
            result_content += f'{key} '
            for index in value:
                result_content += f'{index} '
            result_content += f'\n'
        file.write(result_content)

def generate_indexes():
    for i in range(1, 101):
        docs_ids.add(i)
        with open("../task_2/html/выкачка_" + str(i), encoding='utf-8') as file:
            html = BeautifulSoup(file, features="html.parser")
            process(nlp(str(html.get_text(" ").lower().strip())), i)
    write_index()


def check_for_russia_letter(word):
    alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с",
                "т",
                "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]

    for letter in word:
        if letter not in alphabet:
            return False
    return True


def check_for_rules_token(token):
    if token.text not in stopwords \
            and token.is_alpha \
            and not token.like_num \
            and not token.is_punct \
            and check_for_russia_letter(token.text):
        return True

    return False


def process(doc, doc_id):
    for item in doc:
        if check_for_rules_token(item):
            indexes[item.lemma_].add(doc_id)

            if item.text not in dict_index:
                dict_index[item.text] = []

            if item.text in dict_index and doc_id not in dict_index[item.text]:
                dict_index[item.text].append(doc_id)


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
