import re

from oad.merge import dict_merge
from oad import openapi, OpenAPIDoc


class SanicOpenAPIDoc(OpenAPIDoc):

    def add_method_handler(self, uri, tags, method_name, handler):
        if hasattr(handler, '__openapi__'):
            self.paths[uri][method_name] = dict_merge(
                handler.__openapi__.documentation, {'tags': tags})
            self.schemas.update(handler.__openapi__.schemas)

    def to_dict(self, app, url_prefix='/', tag_blueprints=True):
        methods = {'get', 'post', 'put', 'patch', 'delete'}

        for uri, route in app.router.routes_all.items():
            if not uri.startswith(url_prefix):
                continue

            uri_parsed = uri[len(url_prefix):]
            if not uri_parsed or uri_parsed[0] != '/':
                uri_parsed = '/' + uri_parsed

            parameters = []

            for parameter in route.parameters:
                uri_parsed = re.sub(
                    '<%s.*?>' % parameter.name,
                    '{%s}' % parameter.name,
                    uri_parsed
                )

                parameters.append({
                    '$ref': '#/components/parameters/%s' % parameter.name,
                })

                if parameter.name not in self.parameters:
                    self.add_parameter(parameter.name)

            self.paths[uri_parsed] = dict()

            tags = list()
            if tag_blueprints:
                for blueprint in app.blueprints.values():
                    if hasattr(blueprint, 'routes'):
                        for blueprint_route in blueprint.routes:
                            if blueprint_route.handler == route.handler:
                                tags.append(blueprint.name)

            if hasattr(route.handler, 'view_class'):
                view = route.handler.view_class

                if hasattr(view, '__openapi__'):
                    self.paths[uri_parsed] = dict_merge(
                        self.paths[uri_parsed],
                        view.__openapi__.documentation
                    )
                    self.schemas.update(view.__openapi__.schemas)

                for method_name in methods & set(dir(view)):
                    self.add_method_handler(
                        uri_parsed, tags,
                        method_name, getattr(view, method_name)
                    )

                if parameters and self.paths[uri_parsed]:
                    self.paths[uri_parsed] = dict_merge(
                        self.paths[uri_parsed],
                        {'parameters': parameters},
                    )
            else:
                for method_name in methods & set(map(str.lower, route.methods)):
                    self.add_method_handler(
                        uri_parsed, tags,
                        method_name, route.handler
                    )

                    if parameters and method_name in self.paths[uri_parsed]:
                        self.paths[uri_parsed][method_name] = dict_merge(
                            self.paths[uri_parsed][method_name],
                            {'parameters': parameters},
                        )

            if not self.paths[uri_parsed]:
                del self.paths[uri_parsed]

        return self.doc
