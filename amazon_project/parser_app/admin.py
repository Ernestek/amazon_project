from django.contrib import admin

from parser_app.models import Links, ReviewsInfo


@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    list_display = ('link', 'status',)


@admin.register(ReviewsInfo)
class ReviewsInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'text', 'date', 'count_stars')
