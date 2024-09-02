from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserEditForm
from .models import UserProfile, Movie, Review, Category
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Movie
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category


def home(request):
    return render(request, 'home.html')

from django.contrib.auth import get_user_model

from django.contrib.auth import get_user_model
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            User = get_user_model()
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Create UserProfile linked to the newly created user
            UserProfile.objects.create(
                user=user,
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            return redirect('login')
        else:
            error = 'Passwords do not match'
            return render(request, 'register.html', {'error': error})
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('movie_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def movie_list(request):

    categories = Category.objects.all()


    query = request.GET.get('q')
    selected_category = request.GET.get('category')
    movies = Movie.objects.all()

    if query:
        movies = movies.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if selected_category:
        movies = movies.filter(category__id=selected_category)

    return render(request, 'movie_list.html', {'movies': movies, 'categories': categories, 'selected_category': selected_category})

@login_required()
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = Review.objects.filter(movie=movie).order_by('-id')  # Use 'id' or another field instead of 'created_at'
    return render(request, 'movie_detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def add_movie(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST['name']
        poster = request.FILES['poster']
        description = request.POST['description']
        actors = request.POST['actors']
        release_date = request.POST['release_date']
        youtube_link = request.POST['youtube_link']
        category_id = request.POST['category']


        category = Category.objects.get(id=category_id)


        movie = Movie.objects.create(
            name=name,
            poster=poster,
            description=description,
            actors=actors,
            release_date=release_date,
            youtube_link=youtube_link,
            category=category
        )
        movie.save()
        return redirect('movie_list')

    # Fetch all categories for the dropdown menu
    categories = Category.objects.all()
    return render(request, 'add_movie.html', {'categories': categories})

@login_required
def edit_user_profile(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)  # Correctly link to the UserProfile instance
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserEditForm(instance=user_profile)
    return render(request, 'edit_user_profile.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, Review


@login_required
def submit_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')

        if not rating or not review_text:
            messages.error(request, "Both rating and review are required.")
            return redirect('movie_detail', pk=movie_id)  # Use the correct keyword 'pk' instead of 'movie_id'

        # Create or update review
        review, created = Review.objects.get_or_create(
            user=user_profile,
            movie=movie,
            defaults={'rating': rating, 'review': review_text}
        )
        if not created:
            review.rating = rating
            review.review = review_text
            review.save()

        messages.success(request, "Review submitted successfully!")
        return redirect('movie_detail', pk=movie_id)  # Again, use 'pk'

    return render(request, 'submit_review.html', {'movie': movie})




@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        return redirect('movie_list')
    return render(request, 'user_profile.html', {'user': user})