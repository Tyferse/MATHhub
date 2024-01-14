import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .forms import LoginForm, UserRegistrationForm
from register.models import ProfileInfo, LivePlace, ChosenIntegral, \
    Subscription


def user_login_register(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user_form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # HttpResponceRedirect
                    return HttpResponseRedirect('acc/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        
        if user_form.is_valid():
            password = user_form.cleaned_data['password']
            new_user = User.objects.create_user(
                username=user_form.cleaned_data['login'],
                password=password,
                email=user_form.cleaned_data['email'])
            
            live_place = LivePlace(
                place=user_form.cleaned_data['live_place'])
            live_place.save()
            
            # integral = ChosenIntegral(
            #     integral=request.POST['inlineOptions'])
            # integral.save()
            #
            print(user_form.cleaned_data['is_math'])
            profile = ProfileInfo(user=new_user,
                                  is_math=user_form
                                  .cleaned_data['is_math'],
                                  live_place=live_place)
            profile.save()
            for integral in request.POST.getlist('inlineOptions'):
                profile.chosen_integrals.add(
                    ChosenIntegral.objects.get(integral=int(integral)))
            
            login(request, new_user)
            return HttpResponseRedirect('acc/')
            # return render(request, 'index.html',
            #               {
            #                   'new_user': new_user,
            #                   'form': LoginForm(),
            #                   'user_form': UserRegistrationForm()
            #               }
        
        if ('HTTP_X_REQUESTED_WITH' in request.META
            and request.META['HTTP_X_REQUESTED_WITH']
                == 'XMLHttpRequest'):
            email = request.POST.get('email')
            
            if email:  # Проверка наличия email
                subscriber, created = (Subscription.objects
                                       .get_or_create(email=email))
                
                if created:
                    return JsonResponse(
                        {'message': 'Спасибо за подписку!'})
                else:
                    return JsonResponse(
                        {'message': 'Вы уже подписаны.'})
            else:
                return JsonResponse(
                    {'message': 'Пожалуйста, введите email.'})
        else:
            return JsonResponse({'message': 'Ошибка запроса.'})
    else:
        form = LoginForm()
        user_form = UserRegistrationForm()
    
    return render(request, 'index.html',
                  {'form': form, 'user_form': user_form})
