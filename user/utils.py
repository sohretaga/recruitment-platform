from user.models import CustomUser


def manage_user_type_for_details(request, username:str, user_type:str) -> dict:
    user_exists = CustomUser.objects.filter(username=username).exists()
    user_is_superuser = False
    if user_exists:
        user_is_superuser = CustomUser.objects.get(username=username).is_superuser

    if request.user.is_superuser or user_is_superuser:
        params = {
            'username': username,
        }
    else:
        params = {
            'username': username,
            'user_type': user_type
        }
    
    return params