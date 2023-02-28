from sales.forms import SubscribeForm


def subscribe_form(request):
    """Render Subscribe form in footer"""
    return dict(subscribe_form=SubscribeForm())
