import os

from bs4 import BeautifulSoup
from django.db import transaction

from api.models import HtmlInfoModel


class ParseHtml:
    def __init__(self, path_to_html, path_to_sites):
        self.path_to_html = path_to_html
        self.path_to_sites = path_to_sites
        self.sites = dict()

    @staticmethod
    def parse_tags(soup, name_tag,kwargs_name, attrs, kwargs, content=True, get_attr=''):
        try:
            meta_tag = soup.find(name=name_tag, attrs=attrs)

            if content:
                if meta_tag.string is not None:
                    kwargs[kwargs_name] = meta_tag.string
                else:
                    kwargs[kwargs_name] = ''

            else:
                if meta_tag.get(get_attr) is not None:
                    kwargs[kwargs_name] = meta_tag.get(get_attr)
                else:
                    kwargs[kwargs_name] = ''
        except Exception as e:
            kwargs[kwargs_name] = ''

        return kwargs

    def set_sites_dict(self):
        with open(self.path_to_sites, 'r', encoding='utf-8') as file:
            for line in file:
                line_split = line.strip('\n').split(" ")

                self.sites[int(line_split[0])] = line_split[3]

    def parse_site(self):
        with transaction.atomic():
            for file in os.listdir(self.path_to_html):
                with open(f'{self.path_to_html}/{file}', 'r', encoding='utf-8') as content:
                    page_num = file.split("_")[1].strip(".txt")
                    soup = BeautifulSoup(content, 'lxml')

                    kwargs = dict()

                    kwargs['page_number'] = int(page_num)

                    kwargs = self.parse_tags(soup, name_tag='title', kwargs_name="title", attrs={}, kwargs=kwargs)

                    if kwargs.get('title') == '':
                        kwargs['title'] = self.sites[int(page_num)]

                    kwargs['href'] = self.sites[int(page_num)]

                    kwargs = self.parse_tags(soup,
                                             name_tag='meta',
                                             kwargs_name="description",
                                             attrs={'name': 'description'},
                                             kwargs=kwargs,
                                             content=False,
                                             get_attr='content')

                    obj, created = HtmlInfoModel.objects.update_or_create(**kwargs)

                    print(f'ready {obj.href}')
