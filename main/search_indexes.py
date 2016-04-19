import datetime
from haystack import indexes
from main.models import ScholarContactProfile, FAQEntry

class ScholarContactProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    # For autocomplete
    # content_auto = indexes.EdgeNgramField(model_attr='content')

    def get_model(self):
        return ScholarContactProfile

class FAQEntryIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document = True, use_template = True)
	def get_model(self):
		return FAQEntry
