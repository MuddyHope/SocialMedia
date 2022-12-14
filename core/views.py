from audioop import reverse
from datetime import datetime
from winreg import REG_QWORD
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import messages, auth
from .models import FollowerCount, LikePost, Profile,Post
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.

@login_required(login_url= 'signin')
def index(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    feed_list = Post.objects.all()[::-1]   #-1 is added for latest first
    return render(request, 'index.html', {'user_profile': user_profile, 'feed_list' : feed_list})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request, "Email already in use")
                return redirect("signin.html")
            elif User.objects.filter(username = username).exists():
                messages.info(request, "User name taken")
                return render(request, "signup")
            else:
                user = User.objects.create_user(username = username, email = email, password = password)
                user.save()
                #log user in and redirect to settings page
                
                user_login = auth.authenticate(username = username, password = password)
                auth.login(request, user_login)

                #create a profile object for the new user
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()

                return redirect('setting')
        else:
            messages.info(request, "password doesn't match")
            return redirect('signup.html')


    else:
        return render(request , 'signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Wrong credentials")
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')


@login_required(login_url= 'signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url = 'signin')
def settings(request):
    user_profile = Profile.objects.get(user = request.user)  #user is from Profile Model
    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']    
            location = request.POST['location']
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('setting')
    
    return render(request, 'setting.html', {'user_profile':user_profile})


@login_required(login_url = "signin")
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        print(user)
        image_upload = request.FILES.get('image_upload')
        image_caption = request.POST['image_caption']
        user_post = Post.objects.create(username = user, image = image_upload, caption = image_caption)
        user_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url= 'signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id = post_id)

    #if the currently logged in user has liked the post or not
    like_filter = LikePost.objects.filter(post_id = post_id, username = username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id = post_id, username = username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
    else:
        like_filter.delete()
        post.no_of_likes -=1 
        post.save()
    return redirect('/')

@login_required(login_url= 'signin')
def profile(request, pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)
    feed_list = Post.objects.filter(username = pk)
    feed_length = len(feed_list)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'feed_list': feed_list,
        'feed_length' : feed_length    
    }
    return render(request, 'profile.html', context)

@login_required(login_url= 'signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        print(user, follower)

        #user is the new_following profile, follower is the current_follower profile
        if follower == user:
                return redirect('setting')
        
        if FollowerCount.objects.filter(follower= follower, username = user).first():
            delete_follower = FollowerCount.objects.get(follower = follower, username = user)
            delete_follower.delete()
            #print(FollowerCount.username())
            return redirect('/profile/'+ user, {'Follower_count': FollowerCount})
        else:
            new_follower = FollowerCount.objects.create(follower = follower, username = user)
            new_follower.save()
            #print(FollowerCount.username())
            return redirect('/profile/' + user,{'Follower_count': FollowerCount})
        


    else:
        return redirect(request, 'profile')