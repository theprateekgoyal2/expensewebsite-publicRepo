from django import forms

class ExpenseUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File',
                               help_text='The CSV file should contain data in the format: amount, date, description, category'
                               )

