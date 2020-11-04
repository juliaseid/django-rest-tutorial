from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(
                    full=True, **options)
        self = formatter 

        super(Snippet, self).save(*args, **kwargs)

class SubSnip(models.Model):
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    code = models.TextField()
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    linenos = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='subsnippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(
            style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)

