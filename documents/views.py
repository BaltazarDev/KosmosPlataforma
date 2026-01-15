from django.shortcuts import render

# Create your views here.
def document_list(request):
    return render(request, 'documents/document_list.html')
