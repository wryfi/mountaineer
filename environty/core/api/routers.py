from rest_framework_nested import routers


class ExtensibleRouter(routers.DefaultRouter):
    def extend(self, router):
        """ Simple extensible router
        Pass in a SimpleRouter instance containing route definitions.
        """
        self.registry.extend(router.registry)
