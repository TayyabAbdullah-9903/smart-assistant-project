from django.shortcuts import render, redirect, get_object_or_404
from manuals.models import Manual
from chatbot.models import ChatQuery
from .forms import ManualUploadForm

def portal_home(request):
    manuals = Manual.objects.all().order_by("-id")
    queries = ChatQuery.objects.all().order_by("-id")[:10]
    return render(request, "portal/index.html", {"manuals": manuals, "queries": queries})

def manual_detail(request, pk):
    manual = get_object_or_404(Manual, pk=pk)
    queries = ChatQuery.objects.filter(manual=manual)
    return render(request, "portal/manual_detail.html", {"manual": manual, "queries": queries})

def upload_manual(request):
    if request.method == "POST":
        form = ManualUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("portal_home")
    else:
        form = ManualUploadForm()
    return render(request, "portal/upload_manual.html", {"form": form})
