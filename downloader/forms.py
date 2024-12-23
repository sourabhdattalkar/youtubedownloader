from django import forms

class YouTubeDownloadForm(forms.Form):
    url = forms.URLField(label="YouTube URL", widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter YouTube video URL',
    }))
