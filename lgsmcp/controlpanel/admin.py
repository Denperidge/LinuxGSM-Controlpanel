from django import forms  # forms class to base GameserverCreationForm & GameserverChangeForm from
from django.contrib import admin  # Import admin to register Gameserver & GameServerAdmin 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  # Import BaseUserAdmin to base GameserverAdmin from
from .models import Gameserver, GameserverManager  # Import models

# Modules used during importing 
import csv
import requests

# Get all available servers from LGSM master branch
def get_serverlist():
    csv_url = 'https://raw.githubusercontent.com/GameServerManagers/LinuxGSM/master/lgsm/data/serverlist.csv'
    servers = []
    
    with requests.Session() as req:
        download = req.get(csv_url)  # Download csv
        
        decoded = download.content.decode('utf-8')  # Encode csv

        csvreader = csv.reader(decoded.splitlines(), delimiter=',')  # Interpet csv
        data = list(csvreader)  # Iterate over it as a list
        for server in data:
            servers.append(tuple((server[1], server[1])))  # Add server names to servers (e.g. nmrihserver)

    return servers  # Return array of tuples with server names
serverlist = get_serverlist()  # Put the tuple array in a variable


# Used in /admin/controlpanel/gameserver/ & /admin/controlpanel/gameserver/add/
class GameserverForm(forms.ModelForm):
    class Meta:
        model = Gameserver
        fields = ('linux_username', 'lgsm_servername', 'password1', 'password2')

    lgsm_servername = forms.ChoiceField(choices=serverlist)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_linux_username(self):
        # TODO check for existing user
        return self.cleaned_data.get('linux_username')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Check that passwords match
        gameserver = super().save(commit=False)  # Prepare gameserver
        # Set identifier to linux_username/lgsm_servername
        gameserver.identifier = self.cleaned_data.get('linux_username')+"/"+self.cleaned_data.get('lgsm_servername')
        gameserver.set_password(self.cleaned_data["password1"])  # Hash password
        if commit:
            gameserver.save()  # Save the gameserver unless commit == false
        return gameserver

# /admin/controlpanel/gameserver/
class GameserverAdmin(BaseUserAdmin):
    form = GameserverForm
    add_form = GameserverForm

    list_display = ('identifier',)
    list_filter = ('identifier',)

    # Fieldsets for /admin/controlpanel/gameserver/{{id}}/change/
    fieldsets = (
        (None, {'fields': ('lgsm_servername', 'linux_username', 'password1', 'password2')}),
    )
    # Fieldsets for /admin/controlpanel/gameserver/add/
    add_fieldsets = (
        (None, {'fields': ('lgsm_servername', 'linux_username', 'password1', 'password2')}),
    )
    
    search_fields = ('identifier',)
    ordering = ('identifier',)
    filter_horizontal = ()


admin.site.register(Gameserver, GameserverAdmin)
