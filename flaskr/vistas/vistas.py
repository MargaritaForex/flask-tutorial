from flask_restful import Resource
from ..modelos import db, Cancion, CancionSchema, Usuario, Album
from flask import request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token

cancion_schema = CancionSchema()

class VistaCanciones(Resource):

    def get(self):
        return [cancion_schema.dump(ca) for ca in Cancion.query.all()]
    
    def post(self):
        nueva_cancion = Cancion(titulo=request.json['titulo'],\
                                minutos=request.json['minutos'],\
                                segundos=request.json['segundos'],\
                                interprete=request.json['interprete'])
        
        db.session.add(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)
    

class VistaCancion(Resource):

    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion))
    
    def put(self, id_cancion):
      cancion = Cancion.query.get_or_404(id_cancion)
      cancion.titulo = request.json.get('titulo', cancion.titulo)
      cancion.minutos = request.json.get('minutos', cancion.minutos)
      cancion.segundos = request.json.get('segundos', cancion.segundos)
      cancion.interprete = request.json.get('interprete', cancion.interprete)
      db.session.commit()
      return cancion_schema.dump(cancion)
    
    def delete(self, id_cancion):
      cancion = Cancion.query.get_or_404(id_cancion)
      db.session.delete(cancion)
      db.session.commit()
      return {'mensaje': 'usuario creado exitosamente', 'token de acceso': token_de_acceso}, 204
    
class VistaSignIn(Resource):
   
   def post(self):
      nuevo_usuario = Usuario(nombre=request.json["nombre,"], contrasena=request.json["contrasena"])
      token_de_acceso = create_access_token(identity=request.json['nombre'])
      db.session.add(nuevo_usuario)
      db.session.commit()
      return 'Usuario creado exitosamente', 201
   
   def put(self, id_usuario):
      usuario = Usuario.query.get_or_404(id_usuario)
      usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
      db.session.commit()

class VistaAlbumUsuario(Resource):
   
   @jwt_required()
   def post(self, id_usuario):
      nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"])
      usuario = Usuario.query.get_or_404(id_usuario)
      Usuario.albumes.append(nuevo_album)

      try:
         db.session.commit()
      except IntegrityError:
         db.session.rollback()
         return 'El usuario ya tiene un album con dicho nombre'
      return album_chema.dump(nuevo_album)
   

   @jwt_required()
   def get(self, id_usuario):
      usuario = Usuario.query.get_or_404(id_usuario)
      return [album_chema.dump(al) for al in usuario.albumes]
   
class VistaCancionAlbum(Resource):
   
   def post(self, id_album):
