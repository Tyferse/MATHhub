from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'type': "text",
               'required': "",
               'placeholder': "Логин",
               'aria-label': "Логин"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control",
               'type': "password",
               'required': "",
               'placeholder': "Пароль",
               'aria-label': "Пароль"}))


class UserRegistrationForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'type': "text",
        'placeholder': "Логин",
        'aria-label': "Логин"}),
        max_length=180,
        required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'type': "password",
        'placeholder': "Пароль",
        'aria-label': "Пароль"}),
        max_length=100,
        required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'type': "password",
        'placeholder': "Повторите пароль",
        'aria-label': "Повторите пароль"}),
        max_length=100,
        required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': "form-control",
        'type': "email",
        'placeholder': "Адрес электронной почты",
        'aria-label': "Адрес электронной почты"}), required=False)
    is_math = forms.BooleanField(
        label="Математик?", widget=forms.CheckboxInput(
            attrs={
                'class': "form-check-input",
                'type': "checkbox",
                'name': "is_m",
                'value': "true",
                'aria-label': "Математик?",
                'id': "check2"}), required=False)
    
    OPTIONS = (
        ("Отсутствует", "Отсутствует"),
        ("Кампус", "Кампус"),
        ("Город", "Город"),
        ("Подвал", "Подвал"),
        ("Под мостом", "Под мостом")
    )
    live_place = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-select",
                   'id': "inputGroupSelect02"}),
        choices=OPTIONS)

    # class Meta:
    #     model = User
    #     fields = ('username', 'password', 'password2',
    #               'email', 'notdiff', 'live_place')
    #     widgets = {
    #         'username': forms.CharField(widget=forms.TextInput(
    #             attrs={
    #                 'class': "form-control",
    #                 'type': "text",
    #                 'placeholder': "Логин",
    #                 'aria-label': "Логин"}),
    #             required=True),
    #         'password': forms.CharField(widget=forms.PasswordInput(
    #             attrs={
    #                 'class': "form-control",
    #                 'type': "password",
    #                 'placeholder': "Пароль",
    #                 'aria-label': "Пароль"}),
    #             required=True),
    #         'email': forms.EmailField(widget=forms.EmailInput(
    #             attrs={
    #                 'class': "form-control",
    #                 'type': "email",
    #                 'placeholder': "Адрес электронной почты",
    #                 'aria-label': "Адрес электронной почты"}),
    #             required=False)
    #     }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        
        return cd['password2']
