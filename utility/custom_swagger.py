from drf_yasg.inspectors import SwaggerAutoSchema
# https://stackoverflow.com/questions/64185352/how-to-tag-whole-viewset-in-drf-yasg


class CustomAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = self.overrides.get('tags', None) or getattr(self.view, 'swagger_tags', [])
        if not tags:
            tags = [operation_keys[0]]
        return