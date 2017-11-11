from django.http import Http404


def get_slug_or_404(cls, slug):
    try:
        return cls.objects.get(slug=slug)
    except Exception as ex:
        raise Http404('No %s matches the given query.' % cls._meta.object_name)
