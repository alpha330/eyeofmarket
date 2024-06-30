from django import forms
from shop.models import ProductModel, ProductImageModel
from django.core.exceptions import ValidationError


class ProductForm(forms.ModelForm):

    class Meta:
        model = ProductModel
        fields = [
            "category",
            "title",
            "slug",
            "image",
            "description",
            "brief_description",
            "stock",
            "status",
            "price",
            "is_featured",
            "discount_percent",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['slug'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['brief_description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['id'] = 'ckeditor'
        self.fields['stock'].widget.attrs['class'] = 'form-control'
        self.fields['stock'].widget.attrs['type'] = 'number'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['discount_percent'].widget.attrs['class'] = 'form-control'
        self.fields['is_featured'].widget.attrs['class'] = 'form-check-input'

    def clean_is_featured(self):
        is_featured = self.cleaned_data.get('is_featured', False)
        if is_featured:
            featured_count = ProductModel.objects.filter(is_featured=True).exclude(id=self.instance.id).count()
            if featured_count >= 3:
                raise ValidationError("فقط سه محصول می‌توانند به عنوان ویژه انتخاب شوند.")
        return is_featured


class ProductImageForm(forms.ModelForm):

    class Meta:
        model = ProductImageModel
        fields = [
            "file",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['accept'] = 'image/png, image/jpg, image/jpeg'
