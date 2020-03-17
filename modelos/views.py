from django.shortcuts import render, redirect
from django.forms import modelformset_factory, ModelForm
from .models import Author, Book


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title',]

# Create your views here.
def index(request):
    context = {}
    BookFormSet = modelformset_factory(Book, form=BookForm)
    if request.method == 'POST':
        author_form = AuthorForm(request.POST)
        formset = BookFormSet(request.POST, request.FILES, queryset=Book.objects.none())
        print('\n')
        print(' post: ',request.POST)
        print('files: ', request.FILES)
        print('\n')
        print('\n author: ', author_form.is_valid())
        print('\n books: ', formset.is_valid())
        if author_form.is_valid() and formset.is_valid():
            a = author_form.save(commit=False)
            a.save()
            books = formset.save(commit=False)
            for book in books:
                book.author = a
                book.save()
            return redirect('/')
    else:
        author_form = AuthorForm()
        formset = BookFormSet(queryset=Book.objects.none())
    context['formset'] = formset
    context['form'] = author_form
    return render(request, 'libreria.html', context)

def agregar_autor(request):
    
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/add_autor/')
    else:
        form = AuthorForm()
    
    return render(request, 'agregar_autor.html', {'form':form})