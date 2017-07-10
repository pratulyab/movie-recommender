from django import forms
from movie.models import Genre, Movie

class GenreForm(forms.Form):
	genre1 = forms.CharField(label="Priority 1", max_length=20, required=False)
	genre2 = forms.CharField(label="Priority 2", max_length=20, required=False)
	genre3 = forms.CharField(label="Priority 3", max_length=20, required=False)

	def __init__(self, *args, **kwargs):
		super(GenreForm, self).__init__(*args, **kwargs)
		self.fields['genre1'].widget = forms.Select(choices=self.get_choices())
		self.fields['genre2'].widget = forms.Select(choices=self.get_choices())
		self.fields['genre3'].widget = forms.Select(choices=self.get_choices())
	'''
	def clean(self, *args, **kwargs):
		genre1 = self.cleaned_data.get('genre1')
		genre2 = self.cleaned_data.get('genre2')
		genre3 = self.cleaned_data.get('genre3')
		if not (genre1 and genre2 and genre3):
			raise forms.ValidationError('Atleast one genre is required.')
		return self.cleaned_data
	'''
	def get_recommendations(self, n=5):
		return Movie.objects.all()[:n]

	@staticmethod
	def get_choices():
		pks = []
		names = []
		for genre in Genre.objects.all():
			pks.append(genre.pk)
			names.append('---------------' if genre.name == '(no genres listed)' else genre.name)
		return zip(pks, names)
