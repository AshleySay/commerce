from django import forms

class NewListingForm(forms.Form):
    title = forms.CharField(label="Title:")
    description = forms.CharField(widget=forms.Textarea,
        label="Describe the item:")
    starting_bid = forms.DecimalField(decimal_places=2,
        label="Starting bid: ($USD)")
    image = forms.URLField(label="URL of your image:")
    category = forms.CharField(label="Item category:")


class NewBidForm(forms.Form):
    bid = forms.DecimalField(decimal_places=2,
        label="Bid:")