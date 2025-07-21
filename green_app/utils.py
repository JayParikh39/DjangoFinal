from django.utils.timezone import now

def update_user_visit_session(request):
    num_visits = request.session.get('num_visits', 0)
    last_visit = request.session.get('last_visit', 'First visit this session')
    request.session['num_visits'] = num_visits + 1
    request.session['last_visit'] = now().strftime('%Y-%m-%d %H:%M:%S')
    return {
        'num_visits': num_visits + 1,
        'last_visit': last_visit
    } 