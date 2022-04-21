# https://docs.djangoproject.com/en/4.0/topics/http/urls/#registering-custom-path-converters
# URL filter tags eg <float>

class FloatConverter:
    # ./utility/converters.py:4:25: W605 invalid escape sequence '\.'
    # TODO TEST <FLOAT> - to remove error added r' to regex
    regex = r'[-+]?[0-9]*\.?[0-9]+'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)
