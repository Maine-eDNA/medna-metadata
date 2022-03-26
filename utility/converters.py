# https://docs.djangoproject.com/en/4.0/topics/http/urls/#registering-custom-path-converters
# URL filter tags eg <float>
class FloatUrlParameterConverter:
    regex = '/^[-+]?[0-9]*\.?[0-9]+$/'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)
