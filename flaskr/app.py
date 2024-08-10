from flaskr import create_app
from .modelos import db, Cancion, Usuario, Album, Medio

app = create_app('default')
app_context = app.app_context()
app_context.push()


db.init_app(app)
db.create_all()


with app.app_context():
    u = Usuario(nombre='Juan', contrasena='123456')
    a = Album(titulo='prueba', anio=1999, descripcion='texto', medio=Medio.CD)
    c = Cancion(titulo='mi cancion', minutos=1, segundos=15, interprete = 'Juanito')
    u.albumes.append(a)
    a.canciones.append(c)
    db.session.add(u)
    db.session.add(c)
    db.session.commit()
    #print(Usuario.query.all())
    #print(Usuario.query.all()[0].albumes)
    print(Album.query.all())
    print(Album.query.all()[0].canciones)
    print(Cancion.query.all())
    db.session.delete(a)
    #db.session.delete(u)
    #print(Usuario.query.all())
    #print(Album.query.all())
    print(Album.query.all())
    print(Cancion.query.all())


#prueba

# with app.app_context():
#     c = Cancion(titulo="Prueba", minutos=2, segundos=25, interprete="Prueba1")
#     c2 = Cancion(titulo="Prueba2", minutos=3, segundos=26, interprete="Prueba2")
#     db.session.add(c)
#     db.session.add(c2)
#     db.session.commit()
#     print(Cancion.query.all())
