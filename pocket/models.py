from django.contrib.auth import get_user_model

def get_sentinel_user():
    result=get_user_model().objects.get_or_create(
        username="DELETED-ACCOUNT"
    )
    sentinel_user,created=result[0],result[1]
    return sentinel_user