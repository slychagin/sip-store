from banners.models import BackgroundBanner


def bgr_banner(request):
    """Get Background banner to set on different pages"""
    try:
        banner = BackgroundBanner.objects.all()[0]
    except IndexError:
        banner = ''
    return dict(background_banner=banner)
