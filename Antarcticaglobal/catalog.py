import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from model import db_session, Department as DepartmentModel, User as EmployeeModel

class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )

class User(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )

class SearchResult(graphene.Union):
    class Meta:
        types = (Department, User)        
class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_employees = SQLAlchemyConnectionField(User.connection)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(Department.connection)

schema = graphene.Schema(query=Query)