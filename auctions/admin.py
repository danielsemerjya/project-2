from django.contrib import admin
from auctions.models import Listing, User, Bid, Comment, Watch

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "status")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id","username", "email")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing_id", "user_id", "price")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing_id", "user_id", "text")

class WatchAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "auction")

# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watch, WatchAdmin)