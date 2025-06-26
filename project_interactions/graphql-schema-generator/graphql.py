# Mock GraphQL types for testing

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

class GraphQLSchema:
    def __init__(self, query=None, mutation=None, subscription=None, types=None):
        self.query_type = query
        self.mutation_type = mutation
        self.subscription_type = subscription
        self.types = types or []

class GraphQLObjectType:
    def __init__(self, name, fields, description=None):
        self.name = name
        self.fields = fields
        self.description = description

class GraphQLField:
    def __init__(self, type, args=None, resolve=None):
        self.type = type
        self.args = args or {}
        self.resolve = resolve

class GraphQLString:
    pass

class GraphQLInt:
    pass

class GraphQLFloat:
    pass

class GraphQLBoolean:
    pass

class GraphQLID:
    pass

class GraphQLList:
    def __init__(self, of_type):
        self.of_type = of_type

class GraphQLNonNull:
    def __init__(self, of_type):
        self.of_type = of_type

class GraphQLScalarType:
    def __init__(self, name, description=None, serialize=None, parse_value=None, parse_literal=None):
        self.name = name
        self.description = description
        self.serialize = serialize or (lambda x: x)
        self.parse_value = parse_value or (lambda x: x)
        self.parse_literal = parse_literal or (lambda x: x)

class GraphQLEnumType:
    pass

class GraphQLArgument:
    def __init__(self, type):
        self.type = type

class GraphQLInputObjectType:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

class GraphQLUnionType:
    pass

class GraphQLInterfaceType:
    pass

def print_schema(schema):
    """Mock schema printer"""
    output = []
    if schema.query_type:
        output.append(f"type Query {{\n")
        for field_name, field in schema.query_type.fields.items():
            output.append(f"  {field_name}: String\n")
        output.append("}\n")
    return "".join(output)