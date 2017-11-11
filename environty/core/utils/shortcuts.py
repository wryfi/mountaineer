from django.http import Http404

from environty.core.models import replace_slug


def _get_queryset(klass):
    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    return klass


def get_slug_or_404(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    kwargs = replace_slug(kwargs)
    try:
        return queryset.get(*args, **kwargs)
    except AttributeError:
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    except queryset.model.DoesNotExist:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)