from .models import User, Listing, Bid, Watch
from django.db.models import Max, F

def highest_bid(listing_id):
    # return highest bid query for input listing_id
    b = Bid.objects.annotate(
    highest=Max('listing_id__listing__price')
    ).filter(
    price=F('highest'))
    listing = Listing.objects.get(id=listing_id)
    
    for i in b:
        if i.listing_id == listing:
            b = i
    return b
