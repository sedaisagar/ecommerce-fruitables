from django.contrib.sites.models import Site
from django.conf import settings

class UriUtils:

    @staticmethod
    def build_custom_uri(rev_path):
        site = Site.objects.get_current()
        # building absolute uri without request information
        
        # request.build_absolute_uri(rev_path)
        return f"{settings.REQUEST_SCHEME}://{site.domain}{rev_path}"