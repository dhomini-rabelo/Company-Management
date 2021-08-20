from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("Campos adicionais", {"fields": ("idade", "foto", "telefone_pessoal", "telefone_comercial", "cpf", "empresario")}),
    )
    list_display = 'icon', 'username', 'first_name', 'telefone_pessoal'
    list_display_links = 'username', 'first_name'
