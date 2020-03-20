class APILoggingMixin:

    def dispatch(self, request, *args, **kwargs):
        r = super().dispatch(request, *args, **kwargs)
        return r[0]
