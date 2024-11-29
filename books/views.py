from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Chapter, ProjectVersion, Asset
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.template.loader import render_to_string, get_template
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import tempfile
from pathlib import Path
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import html
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, NextPageTemplate, PageBreakIfNotEmpty
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate
from .forms import ProjectForm

def home(request):
    return render(request, 'books/home.html')

@login_required
def dashboard(request):
    projects = Project.objects.filter(author=request.user).order_by('-updated_at')
    paginator = Paginator(projects, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/dashboard.html', {'page_obj': page_obj})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(user=request.user)
    return render(request, 'books/project_form.html', {'form': form})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    chapters = project.chapters.all()
    return render(request, 'books/project_detail.html', {
        'project': project,
        'chapters': chapters
    })

@login_required
def chapter_edit(request, project_pk, chapter_pk=None):
    project = get_object_or_404(Project, pk=project_pk, author=request.user)
    chapter = None if chapter_pk is None else get_object_or_404(Chapter, pk=chapter_pk, project=project)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        order = request.POST.get('order')
        
        if chapter is None:
            chapter = Chapter.objects.create(
                project=project,
                title=title,
                content=content,
                order=order
            )
        else:
            chapter.title = title
            chapter.content = content
            chapter.order = order
            chapter.save()
            
        messages.success(request, 'Chapter saved successfully!')
        return redirect('project_detail', pk=project.pk)
    
    return render(request, 'books/chapter_form.html', {
        'project': project,
        'chapter': chapter
    })

@login_required
@require_POST
def chapter_delete(request, project_pk, chapter_pk):
    project = get_object_or_404(Project, pk=project_pk, author=request.user)
    chapter = get_object_or_404(Chapter, pk=chapter_pk, project=project)
    chapter.delete()
    messages.success(request, 'Chapter deleted successfully!')
    return JsonResponse({'status': 'success'})

@login_required
def asset_upload(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, author=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        asset_type = request.POST.get('asset_type')
        file = request.FILES.get('file')
        description = request.POST.get('description')
        
        Asset.objects.create(
            project=project,
            title=title,
            asset_type=asset_type,
            file=file,
            description=description
        )
        messages.success(request, 'Asset uploaded successfully!')
        return redirect('project_detail', pk=project.pk)
    
    return render(request, 'books/asset_form.html', {'project': project})

@login_required
def pdf_settings(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, author=request.user)
    return render(request, 'books/pdf_settings.html', {'project': project})

def create_page_template(doc, id, page_number_format):
    def page_number_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_num = canvas.getPageNumber()
        if page_number_format == 'roman':
            page_text = 'i' * page_num if page_num <= 3 else str(page_num - 3)
        else:
            page_text = str(page_num - 3)
        canvas.drawCentredString(doc.pagesize[0]/2, 0.5*inch, page_text)
        canvas.restoreState()

    frame = Frame(
        doc.leftMargin, 
        doc.bottomMargin,
        doc.width,
        doc.height,
        id='normal'
    )
    return PageTemplate(id=id, frames=[frame], onPage=page_number_footer)

@login_required
def export_pdf(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, author=request.user)
    chapters = Chapter.objects.filter(project=project).order_by('order')
    
    # Prepare the context
    context = {
        'project': project,
        'chapters': chapters,
    }
    
    # Render the HTML template
    template = get_template('books/pdf_template.html')
    html = template.render(context)

    # Configure WeasyPrint with font configuration
    font_config = FontConfiguration()
    
    # Create PDF using WeasyPrint with the provided CSS
    pdf_file = HTML(string=html).write_pdf(
        stylesheets=[],  # CSS is included in the template
        font_config=font_config,
        presentational_hints=True
    )
    
    # Create response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{project.title}.pdf"'
    response.write(pdf_file)
    
    return response

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project, user=request.user)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project, user=request.user)
    return render(request, 'books/project_form.html', {'form': form, 'project': project})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'books/project_delete.html', {'project': project})

def generate_pdf(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    chapters = Chapter.objects.filter(project=project).order_by('order')
    
    # Calculate page numbers
    pages = {
        'front_matter': ['i', 'ii', 'iii'],  # Title, Copyright, TOC pages
        'chapters': []
    }
    
    # Calculate chapter page numbers and store chapter data
    current_page = 1  # Start chapters from page 1
    for chapter in chapters:
        # Estimate pages based on content length (rough estimate)
        content_length = len(chapter.content)
        pages_for_chapter = max(1, content_length // 2000)  # Assume ~2000 chars per page
        
        # Store the chapter data
        pages['chapters'].append({
            'id': chapter.id,
            'title': chapter.title,
            'content': chapter.content,  # Store content directly
            'start_page': current_page,
            'estimated_pages': pages_for_chapter
        })
        current_page += pages_for_chapter
    
    # Prepare the context
    context = {
        'project': project,
        'chapters': chapters,
        'include_toc': True,
        'pages': pages,
    }
    
    # Render the HTML template
    template = get_template('books/pdf_template.html')
    html = template.render(context)

    # Create a PDF from the HTML
    pdf_file = HTML(string=html).write_pdf(presentational_hints=True)
    
    # Create the HTTP response with PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{project.title}.pdf"'
    
    return response

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(user=request.user)
    return render(request, 'books/project_form.html', {'form': form})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project, user=request.user)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project, user=request.user)
    return render(request, 'books/project_form.html', {'form': form, 'project': project})

