from django import forms
from .models import Connection_Db
from monitor.models import Monitor_Db
import serial.tools.list_ports
from printrun.printcore import printcore
from django.contrib.auth.models import User

def db_list_4_tuple(*args):
    merged_list = []
    if len(args) == 2:
            for i in range(0, len(args[0])):
                merged_list.append((args[0][i], args[1][i]))
    else:
        try:
            for i in range(0, len(args[0])):
                merged_list.append((args[0][i].device, args[0][i].name))
        except:
            for i in range(0, len(args[0])):
                merged_list.append((list(range(len(args[0])))[i], args[0][i]))
    return tuple(merged_list)


LIST_OF_BAUDRATES = [
                    300, 600, 1200, 2400, 4800, 9600, 14400,
                    19200, 28800, 38400, 57600, 115200, 200000
                    ]

BAUDRATES = db_list_4_tuple(LIST_OF_BAUDRATES, LIST_OF_BAUDRATES)
TIMEOUTS = db_list_4_tuple([i for i in range(6)])

OC_LAB = printcore()


# Formular to connect the Arduino based on Connection_Db
class ConnectionForm(forms.ModelForm):
    oc_lab = forms.ChoiceField(
            label='OC_Lab',
            widget=forms.Select(attrs={'class': 'form-group custom-select','id':'chat-message-input'})
            )
    baudrate = forms.ChoiceField(
            choices=BAUDRATES,
            widget=forms.Select(attrs={'class': 'form-group custom-select'})
            )
    timeout = forms.ChoiceField(
            choices=TIMEOUTS,
            widget=forms.Select(attrs={'class': 'form-group custom-select'})
            )
    auth_id = None
    # State variables are then used with the context variables in .views
    state = {
        'connected': False,
        'info': "",
        'messages': "",
        'error': "",
    }
    devices = []  # List of connected devices

    class Meta:
        model = Connection_Db
        exclude = ('chattext',)

    # Look for and list every Arduino connected
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.auth_id = kwargs.pop('user')
        super(ConnectionForm, self).__init__(*args, **kwargs)
        self.update()

    # Connect to the Arduino and wait for response also save the response in the DB

    def update(self):
        self.devices = DevicesConnected()
        if not self.devices:
            self.devices = ['Plug an OC-Lab']
        self.fields['oc_lab'].choices = db_list_4_tuple(self.devices)
        return

    def clean_oc_lab(self, *args, **kwargs):
        oc_lab = self.cleaned_data.get('oc_lab')
        choices = self.fields['oc_lab'].choices
        if 'Plug an OC-Lab' in choices[0]:
            raise forms.ValidationError('Please connect an OC-Lab')
        return oc_lab

    def clean_monitor(self, *args, **kwargs):
        monitor = Monitor_Db()
        monitor.save()
        return monitor

    def clean_auth_id(self, *args, **kwargs):
        auth_id = self.auth_id
        return auth_id

    def clean(self, *args, **kwargs):
        selected_port = list(filter(lambda x: x.device == self.cleaned_data['oc_lab'], self.devices))[0].device
        selected_baudarate = int(self.cleaned_data['baudrate'])
        timeout = int(self.cleaned_data['timeout'])
        try:
            OC_LAB.connect(port=selected_port, baud=selected_baudarate)
        except:
            raise forms.ValidationError('Imposible to connect to {}'.format(selected_port))


# Formular to send the Arduino based on Connection_Db
class ChatForm(forms.ModelForm):

    chattext = forms.CharField(
            label="",
            required=False,
            widget=forms.TextInput(attrs={
                        'class': "form-control overflow-y:scroll",
                        'type': "text",
                        'aria-describedby': "basic-addon2",
                        'style': "resize: none; background-color : #FEFEFE"
            })
    )

    # method to send to the connected OC_LAB
    def send(self):
        message = self.cleaned_data['chattext']
        OC_LAB.send_now(message)
        return message

def DevicesConnected():
    list = []
    a = serial.tools.list_ports.comports()
    for devices in a:
        if str(devices.description) != 'n/a':
            list.append(devices)
    return list
