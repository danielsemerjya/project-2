from django import forms

DEMO_CHOICES =( 
    ("Sport", "Sport"), 
    ("Food", "Food"), 
    ("Lifestyle", "Lifestyle"), 
    ("IT", "IT"), 
)

class create_form(forms.Form):
    title = forms.CharField(label="New listing title")
    text = forms.CharField(label="Text-based description", widget=forms.Textarea)
    start_bid = forms.FloatField(label="Starting bid")
    url = forms.CharField(label="Link for item photo (size 600x600px)")
    category = forms.TypedChoiceField(choices = DEMO_CHOICES, coerce=str, empty_value="Lifestyle")

    title.widget.attrs.update({'class': 'form-control'})
    text.widget.attrs.update({'class': 'form-control'})
    start_bid.widget.attrs.update({'class': 'form-control'})
    url.widget.attrs.update({'class': 'form-control'})
    category.widget.attrs.update({'class': 'form-control'})


class bid_form(forms.Form):
    bid_up=forms.FloatField(label='Your bid', )
    listing_id=forms.FloatField(label="listing_id", widget=forms.HiddenInput())

class new_comment(forms.Form):
    text=forms.CharField(label='Your comment', initial="Comment")
    listing_id=forms.FloatField(label="listing_id", widget=forms.HiddenInput())
  