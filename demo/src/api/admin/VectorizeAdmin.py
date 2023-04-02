from django.contrib.admin import ModelAdmin


class VectorizeAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = (
        "name",
    )


class InvertedIndexAdmin(ModelAdmin):
    list_display = (
        "id",
        "token",
    )
    search_fields = (
        "token",
    )

class HtmlInfoAdmin(ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    search_fields = (
        "title",
    )