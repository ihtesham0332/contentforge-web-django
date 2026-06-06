import json
import threading
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SEOForm, GrammarForm
from .models import AnalysisHistory
from . import api_client


def _warmup():
    t = threading.Thread(target=api_client.warmup, daemon=True)
    t.start()

PLATFORM_ICONS = [
    ("youtube", "YouTube", "play-btn-fill"),
    ("instagram", "Instagram", "camera-fill"),
    ("linkedin", "LinkedIn", "linkedin"),
    ("facebook", "Facebook", "facebook"),
    ("twitter", "X / Twitter", "twitter-x"),
    ("tiktok", "TikTok", "music-note-beamed"),
    ("pinterest", "Pinterest", "pin-map-fill"),
    ("seo", "General SEO", "search-heart-fill"),
]


def home(request):
    _warmup()
    return render(request, "home.html", {"platforms": PLATFORM_ICONS})


def _get_token(request):
    profile = getattr(request.user, "profile", None)
    return profile.hf_token if profile and profile.hf_token else ""


@login_required
def dashboard(request):
    _warmup()
    recent = AnalysisHistory.objects.filter(user=request.user)[:6]
    return render(request, "analyzer/dashboard.html", {"recent": recent, "platforms": PLATFORM_ICONS})


@login_required
def seo_input(request, platform=None):
    initial = {"platform": platform or "seo"}
    if request.method == "POST":
        form = SEOForm(request.POST)
        if form.is_valid():
            plat = form.cleaned_data["platform"]
            content = form.cleaned_data["content"]
            token = _get_token(request)
            func = api_client.FUNCTIONS.get(plat)
            if not func:
                messages.error(request, "Invalid platform selected.")
                return redirect("seo_input")
            result = func(content, token)
            record = AnalysisHistory.objects.create(
                user=request.user,
                platform=plat,
                input_text=content,
                result=result,
            )
            return redirect("seo_results", pk=record.pk)
    else:
        form = SEOForm(initial=initial)
    return render(request, "analyzer/seo_input.html", {"form": form, "platforms": PLATFORM_ICONS})


@login_required
def seo_results(request, pk):
    record = get_object_or_404(AnalysisHistory, pk=pk, user=request.user)
    result = record.result
    error = result.get("error")
    return render(request, "analyzer/seo_results.html", {
        "record": record,
        "result": result,
        "error": error,
        "result_json": json.dumps(result, indent=2),
    })


@login_required
def grammar_input(request):
    if request.method == "POST":
        form = GrammarForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            token = _get_token(request)
            result = api_client.analyze_grammar(text, token)
            record = AnalysisHistory.objects.create(
                user=request.user,
                platform="grammar",
                input_text=text,
                result=result,
            )
            return redirect("grammar_results", pk=record.pk)
    else:
        form = GrammarForm()
    return render(request, "analyzer/grammar_input.html", {"form": form})


@login_required
def grammar_results(request, pk):
    record = get_object_or_404(AnalysisHistory, pk=pk, user=request.user)
    result = record.result
    error = result.get("error")
    return render(request, "analyzer/grammar_results.html", {
        "record": record,
        "result": result,
        "error": error,
        "result_json": json.dumps(result, indent=2),
    })


@login_required
def history_list(request):
    platform_filter = request.GET.get("platform", "")
    qs = AnalysisHistory.objects.filter(user=request.user)
    if platform_filter:
        qs = qs.filter(platform=platform_filter)
    page = int(request.GET.get("page", 1))
    per_page = 20
    total = qs.count()
    records = qs[(page - 1) * per_page: page * per_page]
    total_pages = (total + per_page - 1) // per_page
    return render(request, "analyzer/history.html", {
        "records": records,
        "page": page,
        "total_pages": total_pages,
        "page_range": range(1, total_pages + 1),
        "platform_filter": platform_filter,
    })


@login_required
def history_detail(request, pk):
    record = get_object_or_404(AnalysisHistory, pk=pk, user=request.user)
    return render(request, "analyzer/history_detail.html", {
        "record": record,
        "result_json": json.dumps(record.result, indent=2),
    })
