from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator


from canteros import settings


class SuperUserRequiredMixin(object):
    """
    View mixin which requires that the authenticated user is a super user
    (i.e. `is_superuser` is True).
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error( request, 'No tienes Permiso para realizar esta accion.')
            return redirect(settings.LOGIN_URL)
        return super(SuperUserRequiredMixin, self).dispatch(request, *args, **kwargs)
