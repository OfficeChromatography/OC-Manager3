from django.shortcuts import render
from .serialarduino import ArdComm
from .forms import ConnectionForm, ChatForm
from .models import Connection_Db
from django.views import View



Arduino_Port = ArdComm(baudrate=115200, timeout=1)

my_context = {
    'object': [],
    'message': "",
    'connected': "False",
    'device': "",
    'baudrate': "",
    'received': "",
    'errormsg': "",
}
context = {
    'monitor':""
}
blank = my_context

# OLD CODE
# def connection_view(request):
#     if request.method == 'GET':
#         my_context['object'] = []
#         my_context['object'] = ArdComm.ArduinosConnected()
#         if not my_context['object']:
#             Arduino_Port.closeArduino()
#             for i in my_context:
#                 my_context[i]=""
#             my_context['connected']= "False"
#
#     if request.method == 'POST':
#         error=0
#         if 'port_selected' in request.POST:
#             selected = request.POST.get('port_selected')
#             if selected == "Choose...":
#                 my_context['message'] = "Please select port"
#                 my_context['connected'] = "False"
#             else:
#                 print(str(type(selected))+selected)
#                 my_context['received'] = ""
#                 error = 0
#                 while my_context['received'] == "":
#                     try:
#
#                         my_context['connected'] = str(Arduino_Port.connectArduino(selected))
#                         my_context['received'] += Arduino_Port.readArduino()
#                         my_context['baudrate'] = Arduino_Port.baudrate
#                         my_context['device'] = Arduino_Port.name
#                         my_context['message'] = "Connected to " + my_context['device']
#                     except:
#                         my_context['errormsg'] = "Connection Error 1"
#         if "usermsg" in request.POST:
#             my_context['received'] += Arduino_Port.writeArduino(request.POST.get("usermsg"))
#     return render(request, "connection.html", my_context)


# NEW CODE
# def connection_view(request):
#     connectionset   = ConnectionForm(request.POST or None, initial={'baudrate':'115200', 'timeout':'2'})
#     commandsend     = ChatForm(request.POST or None)
#
#     if request.method == 'GET':
#         context['connectionset']    =   connectionset
#         context['commandsend']      =   commandsend
#
#     if request.method == 'POST':
#         if ('oc_lab' in request.POST) and (connectionset.is_valid()):
#             context['monitor'] = ""
#             connectionset.connect()
#             aux = connectionset.save(commit=False)
#             aux.chattext = connectionset.state['messages']
#             aux.save()
#             context['monitor'] += update_monitor()
#             context['connectionset']    =   connectionset
#
#         elif commandsend.is_valid():
#             commandsend.send()
#             context['monitor'] += update_monitor()
#             context['commandsend']      =   commandsend
#
#     return render(request, "test.html", context)

def update_monitor():
    actual_text = Connection_Db.objects.last().chattext
    return actual_text

# Really New Code
class Connection_test(View):

    context = {
        'connectionset': ConnectionForm(initial={'baudrate':'115200', 'timeout':'2'}),
        'commandsend'  : ChatForm(),
        'monitor': ""
    }

    def get(self, request):
        return render(request, "test.html", self.context)

    def post(self, request):
        if ('oc_lab' in request.POST):
            self.context['connectionset'] = ConnectionForm(request.POST)
            if self.context['connectionset'].is_valid():
                self.context['monitor'] = ""
                self.context['connectionset'].connect()

                aux = self.context['connectionset'].save(commit=False)
                aux.chattext = self.context['connectionset'].state['messages']
                aux.save()

                self.context['monitor'] = update_monitor()
                self.context['connectionset']    =  self.context['connectionset']
        else:
            self.context['commandsend'] = ChatForm(request.POST)
            if self.context['commandsend'].is_valid():
                self.context['commandsend'].send()
                self.context['monitor'] = update_monitor()
                self.context['commandsend'] = ChatForm()
        return render(request, "test.html", self.context)
