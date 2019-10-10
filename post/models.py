from django.db import models


# Create your models here.

class Novel(models.Model):
    class Meta:
        db_table = 'novel'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, null=False)
    desc = models.TextField(null=False)
    author = models.CharField(max_length=16, null=False)
    noveltype = models.CharField(max_length=16, null=False)
    tags = models.CharField(max_length=255, null=True)

    def __repr__(self):
        return '<Novel {} {} {} {}>'.format(self.id, self.noveltype, self.title, self.author)

    __str__ = __repr__


class Text(models.Model):
    class Meta:
        db_table = 'text'

    id = models.AutoField(primary_key=True)
    content = models.TextField(null=False)

    def __repr__(self):
        return '<Text {} {}>'.format(self.id, self.content[:20])

    __str__ = __repr__


class Chapter(models.Model):
    class Meta:
        db_table = 'chapter'

    id = models.AutoField(primary_key=True)
    c_title = models.CharField(max_length=256, null=False)
    words = models.IntegerField()
    ctime = models.IntegerField()
    novel = models.ForeignKey(Novel)
    content = models.ForeignKey(Text)

    def __repr__(self):
        return '<Chapter {} >'.format(self.id)

    __str__ = __repr__
