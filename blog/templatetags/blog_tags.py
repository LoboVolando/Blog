from django import template
from ..models import Post
from django.db.models import Count

from django.utils.safestring import mark_safe  # для использования MarkDown
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog\post\latest_posts.html')  # инклюзивный тэг
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}  # возвращают только словари


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')  # регистрация фильтра
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
