from django import forms
from .models import Connection_Db
from .serialarduino import ArdComm

def db_list_4_tuple(*args):
    if len(args)==2:
        merged_list = [(args[0][i], args[1][i]) for i in range(0, len(args[0]))]
    else:
        try:
            merged_list = [(args[0][i].device, args[0][i].name) for i in range(0, len(args[0]))]
        except:
            merged_list = [(list(range(len(args[0])))[i], args[0][i]) for i in range(0, len(args[0]))]
    return tuple(merged_list)


LIST_OF_BAUDRATES = [300, 600, 1200, 2400, 4800, 9600, 14400,
                    19200, 28800, 38400, 57600, 115200, 200000]

BAUDRATES = db_list_4_tuple(LIST_OF_BAUDRATES, LIST_OF_BAUDRATES)
TIMEOUTS= db_list_4_tuple([i for i in range(6)])

Arduino_Port = ArdComm()

# Formular to connect the Arduino based on Connection_Db
class ConnectionForm(forms.ModelForm):
    oc_lab          = forms.ChoiceField(label = 'OC_Lab',
            widget  = forms.Select(attrs={'class': 'form-group custom-select'})
            )
    baudrate        = forms.ChoiceField(
            choices = BAUDRATES,
            widget  = forms.Select(attrs={'class': 'form-group custom-select'})
            )
    timeout         = forms.ChoiceField(
            choices = TIMEOUTS,
            widget  = forms.Select(attrs={'class': 'form-group custom-select'})
            )
    # State variables are then used with the context variables in .views
    state = {
        'connected' : False,
        'info'      : "",
        'messages'  : "",
        'error'     : "",
    }
    devices=[] #List of connected devices

    class Meta:
        model = Connection_Db
        exclude = ('chattext',)

    # Look for and list every Arduino connected
    def __init__(self, *args, **kwargs):
        super(ConnectionForm, self).__init__(*args, **kwargs)
        self.update()

    # Connect to the Arduino and wait for response also save the response in the DB
    def connect(self):
        # Look for the selected arduino in the list of obcjets that cointains the USB ports
        selected_port = list(filter(lambda x: x.device == self.cleaned_data['oc_lab'], self.devices))[0].device
        baudarate = self.cleaned_data['baudrate']
        timeout = int(self.cleaned_data['timeout'])
        self.state['messages'] = ""

        # Try to connect
        while self.state['messages'] == "":
            try:
                self.state['connected'] = Arduino_Port.connectArduino(selected_port, baudarate, timeout)
                self.state['messages'] += Arduino_Port.readArduino()
                self.state['info'] = "Connected to " + selected_port
            except:
                self.state['messages'] = "Connection Error"
        aux = self.save(commit=False)
        aux.chattext = self.state['messages']
        aux.save();
        return

    def update(self):
        self.devices = ArdComm.ArduinosConnected()
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


# Formular to send the Arduino based on Connection_Db
class ChatForm(forms.ModelForm):

    chattext        = forms.CharField(label="",
            required= False,
            widget  = forms.TextInput(attrs={
                        'class': "form-control overflow-y:scroll",
                        'type': "text",
                        'aria-describedby':"basic-addon2",
                        'style': "resize: none; background-color : #FEFEFE"
            })
    )

    class Meta:
        model = Connection_Db
        fields = ('chattext',)

    def send(self):
        message = self.cleaned_data['chattext']
        message = Arduino_Port.writeArduino(message)
        aux = Connection_Db.objects.last()
        aux.chattext += message
        aux.save()
        return message
