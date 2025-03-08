from django import forms

from brewsreviews.models import BlogPost


class BlogPostForm(forms.ModelForm):
    """
    Form to edit a blog post
    """

    class Meta:
        model = BlogPost
        fields = (
            "title",
            "tea",
            "content",
        )
