import strawberry as sb


@sb.type
class Query: ...


@sb.type
class Mutation: ...


schema = sb.Schema(query=Query, mutation=Mutation)
