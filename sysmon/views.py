from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .templatetags.sysmon_tags import SysMon


def issuperuser(user):
    return user.is_superuser


@login_required
@user_passes_test(issuperuser)
def sysmon_as_json(request):
    data = SysMon.build_context_dict(static=True)
    # print(data)  #FTR
    # assert isinstance(data, dict)
    return JsonResponse(data)