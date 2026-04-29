import graphene
from graphene_django import DjangoObjectType
from catering.models import Plato, Reserva


class PlatoType(DjangoObjectType):
    class Meta:
        model = Plato
        fields = ("id", "nombre", "descripcion", "precio",
                  "categoria", "disponible", "imagen_url")


class ReservaType(DjangoObjectType):
    class Meta:
        model = Reserva
        fields = ("id", "nombre_cliente", "email", "telefono",
                  "fecha_evento", "cantidad_personas", "mensaje")


class Query(graphene.ObjectType):
    platos               = graphene.List(PlatoType)
    platos_por_categoria = graphene.List(PlatoType, categoria=graphene.String(required=True))
    plato                = graphene.Field(PlatoType, id=graphene.ID(required=True))
    reservas             = graphene.List(ReservaType)

    def resolve_platos(self, info):
        return Plato.objects.filter(disponible=True)

    def resolve_platos_por_categoria(self, info, categoria):
        return Plato.objects.filter(categoria=categoria, disponible=True)

    def resolve_plato(self, info, id):
        return Plato.objects.get(pk=id)

    def resolve_reservas(self, info):
        return Reserva.objects.all().order_by('-creado_en')


class CrearPlato(graphene.Mutation):
    class Arguments:
        nombre      = graphene.String(required=True)
        descripcion = graphene.String()
        precio      = graphene.Float(required=True)
        categoria   = graphene.String(required=True)
        imagen_url  = graphene.String()

    plato = graphene.Field(PlatoType)

    def mutate(self, info, nombre, precio, categoria, descripcion="", imagen_url=""):
        plato = Plato.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            categoria=categoria,
            imagen_url=imagen_url
        )
        return CrearPlato(plato=plato)


class CrearReserva(graphene.Mutation):
    class Arguments:
        nombre_cliente    = graphene.String(required=True)
        email             = graphene.String(required=True)
        telefono          = graphene.String(required=True)
        fecha_evento      = graphene.Date(required=True)
        cantidad_personas = graphene.Int(required=True)
        mensaje           = graphene.String()

    reserva = graphene.Field(ReservaType)

    def mutate(self, info, nombre_cliente, email, telefono,
               fecha_evento, cantidad_personas, mensaje=""):
        reserva = Reserva.objects.create(
            nombre_cliente=nombre_cliente,
            email=email,
            telefono=telefono,
            fecha_evento=fecha_evento,
            cantidad_personas=cantidad_personas,
            mensaje=mensaje
        )
        return CrearReserva(reserva=reserva)


class EliminarReserva(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    mensaje = graphene.String()

    def mutate(self, info, id):
        try:
            reserva = Reserva.objects.get(pk=id)
            reserva.delete()
            return EliminarReserva(mensaje="Reserva eliminada correctamente")
        except Reserva.DoesNotExist:
            return EliminarReserva(mensaje="La reserva no existe")


class Mutation(graphene.ObjectType):
    crear_plato      = CrearPlato.Field()
    crear_reserva    = CrearReserva.Field()
    eliminar_reserva = EliminarReserva.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)