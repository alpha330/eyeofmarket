from django import forms
from shop.models import ProductCategoryModel
from django.core.exceptions import ValidationError

class ProductGroupForm(forms.ModelForm):

    class Meta:
        model = ProductCategoryModel
        fields = [
            "title",
            "slug",
            "is_featured"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['slug'].widget.attrs['class'] = 'form-control'
        self.fields['is_featured'].widget.attrs['class'] = 'form-check-input'

    def clean_is_featured(self):
        is_featured = self.cleaned_data.get('is_featured', False)
        if is_featured:
            featured_count = ProductCategoryModel.objects.filter(is_featured=True).exclude(id=self.instance.id).count()
            if featured_count >= 3:
                raise ValidationError("فقط سه دسته‌بندی می‌توانند به عنوان ویژه انتخاب شوند.")
        return is_featured

