import re

from oad.merge import dict_merge


class OpenAPIDoc:

    def __init__(self, *args, **kwargs):
        """ OpenAPI documentation
        https://swagger.io/docs/specification/about/
        """

        self.paths = dict()
        self.schemas = dict()
        self.parameters = dict()
        self.responses = dict()
        self.security_schemes = dict()
        self.tags = list()

        self.components = dict(
            schemas=self.schemas,
            parameters=self.parameters,
            responses=self.responses,
            securitySchemes=self.security_schemes,
        )

        self.doc = dict_merge({
            'openapi': '3.0.0',
            'info': {
                'title': '',
                'description': '',
                'termsOfService': '',
                'contact': {
                    'name': '',
                    'url': '',
                    'email': '',
                },
                'license': {
                    'name': '',
                    'url': '',
                },
                'version': '',
            },
            'tags': self.tags,
            'paths': self.paths,
            'components': self.components,
        }, kwargs)

    def add_method_handler(self, uri, tags, method_name, handler):
        if hasattr(handler, '__openapi__'):
            self.paths[uri][method_name] = dict_merge(
                handler.__openapi__.documentation, {'tags': tags})
            self.schemas.update(handler.__openapi__.schemas)

    def add_tag(self, name: str, documentation: dict = None):
        """ Add tag info
        https://swagger.io/docs/specification/grouping-operations-with-tags/
        """

        self.tags.append(dict_merge({
            'name': name,
        }, documentation or {}))
        return self

    def add_security(self, name: str, type: str, documentation: dict = None):
        """ Add security
        https://swagger.io/docs/specification/authentication/
        """

        self.security_schemes[name] = dict_merge({
            'type': type,
        }, documentation or {})
        return self

    def add_server(self, url, documentation: dict = None):
        """ Add server info
        https://swagger.io/docs/specification/api-host-and-base-path/
        """

        self.doc = dict_merge(self.doc, {
            'servers': [dict_merge({
                'url': url,
            }, documentation or {})],
        })
        return self

    def add_parameter(self, name, documentation: dict = None):
        """ Add path parameters
        https://swagger.io/docs/specification/serialization/
        """

        self.parameters[name] = dict_merge({
            'name': name,
            'in': 'path',
            'required': True,
            'schema': {'type': 'string'},
        }, documentation or {})
        return self

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
