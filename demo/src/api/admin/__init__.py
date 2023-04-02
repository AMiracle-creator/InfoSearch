from django.contrib import admin

from api.admin.VectorizeAdmin import VectorizeAdmin, InvertedIndexAdmin, HtmlInfoAdmin
from api.models import VectorizeModel, InvertedIndex, HtmlInfoModel

admin.site.register(VectorizeModel, VectorizeAdmin)
admin.site.register(InvertedIndex, InvertedIndexAdmin)
admin.site.register(HtmlInfoModel, HtmlInfoAdmin)