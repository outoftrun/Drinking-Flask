import datetime
from mongoengine import Document
from mongoengine import DateTimeField, StringField, ReferenceField, ListField, FileField, ImageField


mindate = datetime.date(datetime.MINYEAR, 1, 1)


class ContactGroup(Document):
    name = StringField(max_length=60, required=True, unique=True,default="my cats")

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name





class Tags(Document):
    meta = {'allow_inheritance': True,}

    name = StringField(max_length=60, required=True, unique=True)

    def __unicode__(self):
        return self.name


class Sequences(Document):
    name = StringField(max_length=60, required=True)
    creator = StringField(max_length=60)
    date = DateTimeField()
    # personal_phone = StringField(max_length=20)
    # personal_celphone = StringField(max_length=20)
    contact_group = ReferenceField(ContactGroup, required=True)

    tags = ListField(ReferenceField(Tags))
    comment = StringField(max_length=60, required=True)
    def month_year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, date.month, 1) or mindate

    def year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, 1, 1)

    def __repr__(self):
        return "%s : %s\n" % (self.name, self.contact_group)
