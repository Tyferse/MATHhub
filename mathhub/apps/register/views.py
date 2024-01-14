from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from .models import ProfileInfo, LivePlace, ChosenIntegral


@transaction.atomic
def acc(request):
    prof = get_object_or_404(ProfileInfo, user_id=request.user)
    # live_place = get_object_or_404(LivePlace, id=prof.live_place.id)
    integrals = prof.chosen_integrals.all()
    li = len(integrals)
    if li == 1:
        integrals = integrals.first()
    
    return render(request, 'login/auth_success.html',
                  {
                      'is_mathematician': prof.is_math,
                      'place': prof.live_place,
                      'integrals': integrals,
                      'int_count': li
                  })
