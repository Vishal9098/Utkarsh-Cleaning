from .models import Cart


def cart_count(request):
    count = 0
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            session_key = request.session.session_key
            if session_key:
                cart = Cart.objects.get(session_key=session_key)
            else:
                cart = None
        if cart:
            count = cart.get_item_count()
    except Cart.DoesNotExist:
        pass
    return {'cart_count': count}
