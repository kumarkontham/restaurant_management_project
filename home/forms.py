from django import forms
class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=100,required=True,label="your name")
    email = forms.EmailField(required=True,label="Your email")
    message = forms.CharField(width=forms.Textarea,required = True, label ="Your message")
class FeedbackForm(forms.ModelForm):
    model = Feedback
    