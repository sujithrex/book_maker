from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Project(models.Model):
    BOOK_TYPES = [
        ('novel', 'Novel'),
        ('textbook', 'Textbook'),
        ('comic', 'Comic'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=200, blank=True, null=True)
    book_type = models.CharField(max_length=20, choices=BOOK_TYPES)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    
    # New fields for book metadata
    publisher_name = models.CharField(max_length=200, blank=True, null=True)
    publisher_location = models.CharField(max_length=200, blank=True, null=True)
    publisher_website = models.URLField(blank=True, null=True)
    publisher_address = models.TextField(blank=True, null=True)
    copyright_text = models.TextField(blank=True, null=True)
    rights_text = models.TextField(blank=True, null=True)
    lccn = models.CharField(max_length=50, blank=True, null=True, verbose_name="Library of Congress Number")
    edition = models.CharField(max_length=50, blank=True, null=True)
    printing_info = models.CharField(max_length=200, blank=True, null=True)
    cover_designer = models.CharField(max_length=200, blank=True, null=True)
    illustrator = models.CharField(max_length=200, blank=True, null=True)
    version_number = models.CharField(max_length=20, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

class PDFSettings(models.Model):
    PAGE_SIZES = [
        ('A4', 'A4 (210x297mm)'),
        ('A5', 'A5 (148x210mm)'),
        ('LETTER', 'Letter (216x279mm)'),
        ('CUSTOM', 'Custom Size'),
    ]
    
    COLUMN_CHOICES = [
        (1, 'Single Column'),
        (2, 'Two Columns'),
        (3, 'Three Columns'),
    ]
    
    PAGE_NUMBERING = [
        ('NONE', 'No Page Numbers'),
        ('SIMPLE', 'Simple Numbers'),
        ('CHAPTER', 'Chapter-based (1-1, 1-2)'),
        ('ROMAN', 'Roman Numerals'),
    ]

    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='pdf_settings')
    page_size = models.CharField(max_length=10, choices=PAGE_SIZES, default='A4')
    custom_width = models.FloatField(null=True, blank=True, help_text='Width in mm')
    custom_height = models.FloatField(null=True, blank=True, help_text='Height in mm')
    margin_top = models.FloatField(default=25.4, help_text='Top margin in mm')
    margin_right = models.FloatField(default=25.4, help_text='Right margin in mm')
    margin_bottom = models.FloatField(default=25.4, help_text='Bottom margin in mm')
    margin_left = models.FloatField(default=25.4, help_text='Left margin in mm')
    columns = models.IntegerField(choices=COLUMN_CHOICES, default=1)
    column_spacing = models.FloatField(default=12.7, help_text='Space between columns in mm')
    
    # Headers and Footers
    header_text = models.CharField(max_length=200, blank=True)
    footer_text = models.CharField(max_length=200, blank=True)
    include_page_numbers = models.CharField(max_length=10, choices=PAGE_NUMBERING, default='SIMPLE')
    
    # Chapter Formatting
    chapter_start_new_page = models.BooleanField(default=True)
    chapter_title_font_size = models.IntegerField(default=24)
    chapter_title_spacing = models.FloatField(default=25.4, help_text='Space after chapter title in mm')
    
    # Table of Contents
    generate_toc = models.BooleanField(default=True)
    include_index = models.BooleanField(default=False)
    
    # Advanced Settings
    include_bleed_marks = models.BooleanField(default=False)
    bleed_size = models.FloatField(default=3, help_text='Bleed size in mm')
    include_trim_marks = models.BooleanField(default=False)
    
    def __str__(self):
        return f"PDF Settings for {self.project.title}"

class Chapter(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    content = RichTextField()
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title} - {self.title}"

class ProjectVersion(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-version_number']

    def __str__(self):
        return f"{self.project.title} - Version {self.version_number}"

class Asset(models.Model):
    ASSET_TYPES = [
        ('image', 'Image'),
        ('table', 'Table'),
        ('chart', 'Chart'),
        ('other', 'Other'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='assets')
    title = models.CharField(max_length=200)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    file = models.FileField(upload_to='assets/')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.project.title} - {self.title}"
