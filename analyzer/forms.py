from django import forms

PLATFORM_CHOICES = [
    ("seo", "General SEO"),
    ("youtube", "YouTube"),
    ("instagram", "Instagram"),
    ("linkedin", "LinkedIn"),
    ("facebook", "Facebook"),
    ("twitter", "X / Twitter"),
    ("tiktok", "TikTok"),
    ("pinterest", "Pinterest"),
]


class SEOForm(forms.Form):
    platform = forms.ChoiceField(choices=PLATFORM_CHOICES, label="Platform")
    content = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6, "placeholder": "Enter your topic, keyword, or content idea..."}),
        label="Content",
        max_length=2000,
    )


class GrammarForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 8, "placeholder": "Paste your text here for grammar correction..."}),
        label="Text",
        max_length=5000,
    )
