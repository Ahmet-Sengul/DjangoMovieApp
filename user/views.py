from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Oturum açıldı')
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, 'Hatalı kullanıcı adı veya parola!')
            return redirect('login')
    else:
        return render(request, 'user/login.html')

def register(request):
    if request.method == 'POST':
        #get form values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']
        #is password == repassword ?
        if password == repassword:
            #is username is alredy taken ?
            if User.objects.filter(username = username).exists():
                messages.add_message(request, messages.WARNING, 'Bu kullanıcı adı daha önce alınmış.')
                return redirect('register')
            else:
                if User.objects.filter(email = email).exists():
                    messages.add_message(request, messages.WARNING, 'Bu email daha önce kayıt olunmuş..')
                    return redirect('register')
                else:
                    #is every thing is ok? let's submit user then
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'Hesap başarıyla oluşturuldu.')
                    return redirect('login')
        else:
            messages.add_message(request, messages.WARNING, 'Parolalar eşleşmiyor.')
            return redirect('register')
    else:
        return render(request, 'user/register.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.add_message(request, messages.SUCCESS, 'Oturumunuz başarıyla kapatılmıştır.')
    return redirect('index')
