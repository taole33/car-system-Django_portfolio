from carmanage.models import Car, Clash , Scrap
from django import forms
from django.contrib.auth.models import User
import bootstrap_datepicker_plus as datetimepicker

 

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('region','bunruinum','hiragana','number','price','leaseorbuy','distance')

class SearchForm(forms.Form):
    region = forms.CharField(label="ナンバー（地名）",required=False,)
    bunruinum = forms.CharField(label="ナンバー（分類番号）",required=False,)
    hiragana = forms.CharField(label="ナンバー（ひらがな）",required=False,)
    number = forms.CharField(label="ナンバー（４桁）", required=False,)
    price = forms.IntegerField(label="取得価格",required=False,)
    distance = forms.IntegerField(label="購入時走行距離",required=False,)

class ClashForm(forms.ModelForm):
    class Meta:
        model = Clash
        fields = ('car','driver','detail','clashday')
        widgets = {
            'clashday': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
                )
                }

class ScrapForm(forms.ModelForm):
    class Meta:
        model = Scrap
        fields = ('car','scrap','scrapday')
        widgets = {
            'scrapday': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                }
                )
                }
