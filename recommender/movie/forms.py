from django import forms
from movie.models import Genre, Movie
from genre_recommender import get_movie_recommendations

class GenreForm(forms.Form):
	genre1 = forms.CharField(label="Preference 1", max_length=20, required=False)
	genre2 = forms.CharField(label="Preference 2", max_length=20, required=False)
	genre3 = forms.CharField(label="Preference 3", max_length=20, required=False)

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
		genres = Genre.objects.filter(pk__in=[int(self.cleaned_data['genre1']), int(self.cleaned_data['genre2']), int(self.cleaned_data['genre3'])])
		return Movie.objects.filter(movielensID__in=get_movie_recommendations(genres, n)).order_by('-popularity')

	@staticmethod
	def get_choices():
		pks = []
		names = []
		for genre in Genre.objects.all():
			pks.append(genre.pk)
			names.append('---------------' if genre.name == '(no genres listed)' else genre.name)
		return zip(pks, names)
