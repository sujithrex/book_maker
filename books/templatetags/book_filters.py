from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_chapter_by_id(chapters, chapter_id):
    for chapter in chapters:
        if chapter.id == chapter_id:
            return chapter
    return None 