from app import settings


__all__ = ["prepare_post_data", ]


def prepare_post_data(**kwargs):
    """
    Returns:
        dict: dict, prepared to use as body in POST request.

    """
    group = kwargs.get('group', '')
    faculty = kwargs.get('faculty', '')
    teacher = kwargs.get('teacher', '')
    sdate = kwargs.get('date_from', '')
    edate = kwargs.get('date_to', '')

    post_data = {
        'faculty': faculty,
        'teacher': teacher.encode(settings.BASE_ENCODING),
        'group': group.encode(settings.BASE_ENCODING),
        'sdate': sdate.encode(settings.BASE_ENCODING),
        'edate': edate.encode(settings.BASE_ENCODING),
        'n': 700
    }

    return post_data
