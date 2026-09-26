from django import forms
from django.contrib.auth.models import User

from .models import ACTIONS, AREAS, StaffAccess

TEXT = {'class': 'text-input'}


class StaffUserForm(forms.ModelForm):
    password = forms.CharField(label='رمز عبور', required=False, widget=forms.PasswordInput(attrs=TEXT))
    note = forms.CharField(label='توضیح', required=False, widget=forms.TextInput(attrs=TEXT))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']

    def __init__(self, *args, **kwargs):
        self.access = kwargs.pop('access', None)
        super().__init__(*args, **kwargs)
        for name in ['username', 'first_name', 'last_name', 'email']:
            self.fields[name].widget.attrs.update(TEXT)
        self.fields['username'].label = 'نام کاربری'
        self.fields['first_name'].label = 'نام'
        self.fields['last_name'].label = 'نام خانوادگی'
        self.fields['email'].label = 'ایمیل'
        self.fields['is_active'].label = 'حساب فعال باشد'
        if self.instance.pk is None:
            self.fields['password'].required = True
        else:
            self.fields['password'].help_text = 'اگر خالی بماند رمز قبلی حفظ می شود'
        if self.access is not None:
            self.fields['note'].initial = self.access.note
        for area, area_label in AREAS:
            for action, action_label in ACTIONS:
                field = forms.BooleanField(required=False, label=action_label)
                field.area = area
                field.area_label = area_label
                field.action = action
                self.fields[self.perm_name(area, action)] = field
                if self.access is not None and self.access.has(area, action):
                    self.fields[self.perm_name(area, action)].initial = True

    @staticmethod
    def perm_name(area, action):
        return 'perm_%s_%s' % (area, action)

    def permission_rows(self):
        rows = []
        for area, area_label in AREAS:
            rows.append({
                'area': area,
                'label': area_label,
                'fields': [self[self.perm_name(area, action)] for action, _ in ACTIONS],
            })
        return rows

    def selected_codes(self):
        codes = []
        for area, _ in AREAS:
            for action, _ in ACTIONS:
                if self.cleaned_data.get(self.perm_name(area, action)):
                    codes.append('%s:%s' % (area, action))
        return codes

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        taken = User.objects.filter(username=username)
        if self.instance.pk:
            taken = taken.exclude(pk=self.instance.pk)
        if taken.exists():
            raise forms.ValidationError('این نام کاربری قبلا ثبت شده است')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        user.save()
        access, _ = StaffAccess.objects.get_or_create(user=user)
        access.set_codes(self.selected_codes())
        access.note = self.cleaned_data.get('note', '')
        access.save()
        return user
