from django.db import models
from mongoengine import *

# Create your models here.

class Documment(EmbeddedDocument):
    nomDoc = IntField()
    nbrFreq = IntField()

class Mot(EmbeddedDocument):
    nomMot = StringField(required=True)
    freqCol = IntField()
    nbrDoc = IntField()
    docs = ListField(EmbeddedDocumentField(Documment))

class MotCol(EmbeddedDocument):
    mots = ListField(EmbeddedDocumentField(Mot))
    cols = ListField(EmbeddedDocumentField(Mot))
    
class FilInverse(Document):
    # nbrDoc = IntField()
    filinverse = EmbeddedDocumentField(MotCol)
    colloc = ListField(StringField())
    stopConcepts = ListField(StringField())
    documents = ListField(StringField())

class FileInverse(Document):
    # nbrDoc = IntField()
    filinverse = EmbeddedDocumentField(MotCol)
    colloc = ListField(StringField())
    stopConcepts = ListField(StringField())
    documents = ListField(StringField())

class ChartDoc(Document):
    indexDoc = IntField()
    score = DecimalField()