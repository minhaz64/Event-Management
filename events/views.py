from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.utils.timezone import now
from datetime import date
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, LoginForm, CategoryForm





def home_view(request):
    search_query= request.GET.get('search', '')

    events = Event.objects.select_related('category').prefetch_related('participants').order_by('-date')
    if search_query:
        events = events.filter(name__icontains=search_query)

    return render(request, "home.html",{
        "search_query": search_query,
        "events": events,
        "h_page" : True
    })





def profile_view(request):
    if 'participant_id' not in request.session:
        return redirect('signin')
    
    user = get_object_or_404(Participant, pk=request.session['participant_id'])
    return render(request, "profile.html",{
        "user": user, 
        "h_page": False
    })


def signup_view(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = ParticipantForm()
    return render(request, "sign_up.html",{
        "form": form, 
        "h_page" : False
        })

def signin_view(request):
    if request.method == "POST":
        form =LoginForm(request.POST)
        if form.is_valid():
            email= form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = Participant.objects.get(email= email, password= password)
                request.session['participant_id'] = user.id
                request.session['participant_name'] = user.name
                return redirect('home')
            
            except Participant.DoesNotExist:
                pass
    else:
        form = LoginForm()
    return render(request, "sign_in.html",{
        "form": form, 
        "h_page" : False
    })


def signout_view(request):
    request.session.flush()
    return redirect('signin')


def join_event(request, pk):
    if 'participant_id' not in request.session:
        return redirect('signin')
    event= get_object_or_404(Event, pk=pk)
    participant = get_object_or_404(Participant, pk=request.session['participant_id'])
    event.participants.add(participant)
    return redirect('event_details', pk=pk)


def leave_event(request, pk):
    if 'participant_id' not in request.session:
        return redirect('signin')
    event= get_object_or_404(Event, pk=pk)
    participant = get_object_or_404(Participant, pk=request.session['participant_id'])
    event.participants.remove(participant)
    return redirect('event_details', pk=pk)


def remove_participant(request, event_id, participant_id):
    event= get_object_or_404(Event, pk=event_id)
    if event.host_id != request.session.get('participant_id'):
        return redirect('event_details', pk=event_id)
    participant= get_object_or_404(Participant, pk=participant_id)
    event.participants.remove(participant)
    return redirect('event_details', pk=event_id)


def event_list(request):
    search_query =request.GET.get('search', '')
    events = Event.objects.select_related('category').prefetch_related('participants')

    # Search
    if search_query:
        events =events.filter(Q(name__icontains=search_query)|Q(location__icontains= search_query))

    category_id = request.GET.get('category')
    if category_id and category_id.isdigit():
        events = events.filter(category_id= category_id)

    start_date = request.GET.get('start_date')
    end_date= request.GET.get('end_date')
    if start_date and end_date:
        events =events.filter(date__gte=start_date, date__lte=end_date)

    categories = Category.objects.all()
    return render(request, "event_page.html",{
        "events": events, 
        "categories": categories, 
        "h_page" : False
    })

def event_create(request):
    if 'participant_id' not in request.session:
        return redirect('signin')

    if request.method =="POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host_id= request.session['participant_id']
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()

    categories = Category.objects.all()
    return render(request, "event_create.html",{
        "form": form,
        "h_page" : False,
        "categories": categories,
        })



def event_edit(request, pk):
    event= get_object_or_404(Event, pk=pk)
    current_user = get_object_or_404(Participant, pk=request.session.get('participant_id'))

    if event.host_id != request.session.get('participant_id') and not current_user.is_admin:
        return redirect('event_list')

    if request.method =="POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('organizer_dashboard')
    else:
        form = EventForm(instance=event)

    categories = Category.objects.all()  
    return render(request, "event_create.html",{
        "form": form,
        "categories": categories,
        "event": event,
        "is_edit": True,
        "h_page": False,
    })


def event_delete(request, pk):
    event= get_object_or_404(Event, pk=pk)
    current_user = get_object_or_404(Participant, pk=request.session.get('participant_id'))
    
    if event.host_id != request.session.get('participant_id') and not current_user.is_admin:
        return redirect('event_list')
    
    event.delete()
    return redirect('organizer_dashboard')




def event_details(request, pk):
    event = get_object_or_404(Event.objects.prefetch_related('participants', 'category'), pk=pk)
    is_host = event.host_id == request.session.get('participant_id')

    user_joined = False
    if request.session.get('participant_id'):
        user_joined = event.participants.filter(id=request.session['participant_id']).exists()

    return render(request, "eventDetails.html",{
        "event": event,
        "is_host": is_host,
        "user_joined": user_joined,
        "h_page" : False
        })



def category_list(request):
    if request.method =="POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('category_list')
    else:
        form= CategoryForm()

    categories = Category.objects.all()
    return render(request, "category.html",{
        "form": form,
        "categories": categories,
        "h_page" : False
    })


def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, "category_form.html",{
        "form": form,
        "h_page" : False,
    })


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')


def organizer_dashboard(request):
    if 'participant_id' not in request.session:
        return redirect('signin')


    today=date.today()
    participant_id = request.session['participant_id']

    current_user =get_object_or_404(Participant, pk=participant_id)

    events = Event.objects.all().select_related('category').prefetch_related('participants')
    
    total_events= events.count()
    total_participants = Participant.objects.filter(events__in=events).distinct().count()
    upcoming_events = events.filter(date__gt=today).count()
    past_events = events.filter(date__lt=today).count()
    today_events = events.filter(date=today)


    filter_type = request.GET.get("type","all")
    if filter_type == "upcoming":
        events = events.filter(date__gt=today)
    elif filter_type == "past":
        events = events.filter(date__lt=today)
    elif filter_type == "today":
        events = today_events

    today_participants = Participant.objects.filter(events__in=today_events).distinct().count()
    stats ={
        "total_events": total_events,
        "total_participants": total_participants,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "today_participants": today_participants,
    }
    return render(request,"org_dash.html",{
        "events": events,
        "stats": stats,
        "today_events": today_events,
        "current_user": current_user,
        "h_page": False,
    })
