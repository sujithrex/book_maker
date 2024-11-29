from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 
            'subtitle', 
            'author_name',
            'book_type', 
            'isbn',
            'description',
            'cover_image',
            'publisher_name',
            'publisher_location',
            'publisher_website',
            'publisher_address',
            'copyright_text',
            'rights_text',
            'lccn',
            'edition',
            'printing_info',
            'cover_designer',
            'illustrator',
            'version_number',
            'publication_date'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subtitle (optional)'}),
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name as it should appear in the book'}),
            'book_type': forms.Select(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ISBN (optional)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter book description'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'publisher_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter publisher name'}),
            'publisher_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter publisher location'}),
            'publisher_website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter publisher website'}),
            'publisher_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter publisher address'}),
            'copyright_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter copyright text'}),
            'rights_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter rights text'}),
            'lccn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Library of Congress Number'}),
            'edition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter edition'}),
            'printing_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter printing information'}),
            'cover_designer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cover designer name'}),
            'illustrator': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter illustrator name'}),
            'version_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter version number'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProjectForm, self).__init__(*args, **kwargs)
        
        # Make only essential fields required
        required_fields = ['title', 'author_name', 'book_type']
        for field in self.fields:
            if field not in required_fields:
                self.fields[field].required = False

        # Set initial author_name if creating new project
        if user and not self.instance.pk:
            self.fields['author_name'].initial = user.get_full_name() or user.username