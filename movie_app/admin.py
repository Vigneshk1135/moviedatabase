from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, Movie, Review, Category

admin.site.register(Category)

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = ('name', 'release_date')
    search_fields = ('name', 'description')

admin.site.register(Movie, MovieAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')

admin.site.register(UserProfile, UserProfileAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating')
    search_fields = ('user__username', 'movie__name')

admin.site.register(Review, ReviewAdmin)