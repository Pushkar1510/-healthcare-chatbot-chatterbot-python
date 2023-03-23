from email import message
from django.shortcuts import render
from matplotlib.pyplot import flag
from sqlalchemy import false, true
from .forms import MsgForm, SympForm
import datetime
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ChatterBotCorpusTrainer
import wikipedia
from .helpfun import symptom_extractor

unimessage = list()

chatbot = ChatBot(**settings.CHATTERBOT)

# trainer = ChatterBotCorpusTrainer(chatbot)

# trainer.train('./symptoms.yaml')

flagi = 5

def home(request):
    return render(request, 'thebot/index.html')

def about(request):
    return render(request, 'thebot/about.html')

def chatarea(request):
    flagi = 5
    today = datetime.datetime.now()
    time = today.strftime('%H:%M')
    if request.method == 'POST' and 'sympsub' in request.POST:
        print("1")
        sympform = SympForm(request.POST)
        if sympform.is_valid():
            symptoms = sympform.cleaned_data.get("symptom_field")
            print(symptoms)
            joined_sym = ",".join(symptoms)
            pred = symptom_extractor(symptoms)
            print(pred)
            unimessage.append(joined_sym)
            unimessage.append(pred)
        sympform = SympForm()
        form = MsgForm()
        return render(request, 'thebot/chat.html', {'form': form, 'unimessage':unimessage, 'time':time, 'flagi':flagi, 'sympform':sympform})
    elif request.method == "POST":
        print("2")
        form = MsgForm(request.POST)

        if form.is_valid():
            msg = form.cleaned_data.get('message')
            resp = chatbot.get_response(msg)
            if resp.text == "symptoms":
                sympform = SympForm()
                flagi = 10
                print("inside antimage")
                unimessage.append(msg)
                unimessage.append("Ok tell me the symptoms")
                form = MsgForm()
                return render(request, 'thebot/chat.html', {'form': form, 'unimessage':unimessage, 'time':time, 'flagi':flagi, 'sympform':sympform})
            print(msg)
            print(resp)
            print(resp.confidence)
            if resp.confidence <=0.8:
                query = msg.replace("?", "")
                words = query.split()
                summary = 'No idea'
                if(words[0].lower()=="what" and words[1]=="is"):
                    if words[2]=="a":
                        words = " ".join(words[3:])
                    else:
                        words = " ".join(words[2:])
                    try:
                        summary = wikipedia.summary(words, sentences = 1)
                    except:
                        print('Wikipedia Exception')
                    
                resp = summary
            unimessage.append(msg)
            unimessage.append(resp)
        
        form = MsgForm()
        
        return render(request, 'thebot/chat.html', {'form': form, 'unimessage':unimessage, 'time':time, 'flagi':flagi})
    else:
        form = MsgForm()
        return render(request, 'thebot/chat.html', {'form': form, 'time':time,'unimessage':unimessage, 'flagi':flagi})