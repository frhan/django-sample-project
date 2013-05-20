from django.contrib.markup.templatetags.markup import markdown
from django.db import models

# Create your models here.
from tagging.fields import TagField
from tagging.models import Tag


class Entity(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        unique_for_date = 'pub_date',
        help_text = 'Automatically built from the title.')
    body_html = models.TextField(blank = True)
    body_markdown = models.TextField(blank=True)
    pub_date = models.DateTimeField('Date Published')
    tags = TagField()
    enable_comments = models.BooleanField(default=True)
    PUB_STATUS = ((0,'draft',(1,'published')))
    status = models.IntegerField(choices = PUB_STATUS, default = 0)


    class Meta():
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
        verbose_name_plural = 'entities'

    def __unicode__(self):
        return u'%s'%(self.title)

    def get_absolute_url(self):
        return '/%s/%s/'%(self.pub_date.strftime("Y/%b/%d").lower(),self.slug)

    def save(self):
        self.body_html = markdown(self.body_markdown, safe_mode = False)

        super(Entity,self).save()

    def get_previous_published(self):
        return  self.get_previous_by_pub_date(status__exact = 1)

    def get_next_published(self):
        return self.get_next_by_pub_date(status__exact = 1)

    def get_tags(self):
        return  Tag.objects.get_for_object(self)






