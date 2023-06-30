import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def validate_password(password):
    if len(password) < 8:
        raise ValidationError(_("Password must be at least 8 characters long."))
    
    if not re.search(r'\d', password):
        raise ValidationError(_("Password must contain at least one number."))
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(_("Password must contain at least one special character."))
