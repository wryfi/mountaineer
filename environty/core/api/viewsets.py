from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from environty.core.utils.slug import replace_slug


class SlugModelViewSet(ModelViewSet):
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        if lookup_url_kwarg == 'slug':
            self.kwargs = replace_slug(self.kwargs)
            self.lookup_field = 'uuid'
            lookup_url_kwarg = 'uuid'

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj