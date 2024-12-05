from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def post_list(request):
    return render(request, "blog/list.html")
@login_required
def post_detail(request, id):
    return render(request, "blog/details.html")