from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# -----------------------------------User--------------------------------------------------


class User(db.Model):

    # Este atributo tablename, sirve para ser referenciado desde otra clase, a la tabla que debe apuntar
    __tablename__ = 'user'

    # Atributos de la clase User
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # relacion con la lista de favoritos, de sus planetas o characteres
    favorites: Mapped[list["Favorite"]] = relationship(
        'Favorite', back_populates='user', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


# ---------------------------Planet---------------------------------------------------
class Planet(db.Model):

    # nombre de la tabla a la que referencia
    __tablename__ = 'planet'

    # Atributos de la clase planeta
    id_planet: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    img_link: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=True)

    def serialize(self):
        return {
            "id_planet": self.id_planet,
            "planet_name": self.name
        }

# ----------------------------Character----------------------------------------------------------


class Character(db.Model):

    # nombre de la tabla a la que referencia
    __tablename__ = 'character'

    # Atributos de la clase planeta
    id_character: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    img_link: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=True)

    def serialize(self):
        return {
            "id_characater": self.id_character,
            "character_name": self.name
        }


# ---------------------------------Favorites--------------------------------------------------------
class Favorite(db.Model):

    __tablename__ = 'favorite'

    # Atributos de la clase
    id_fav: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Apunta siempre al usuario del favorito
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    # Puede contener un planeta o un character como favorito, puede ser null porque esa fila puede estar asociada a un caracter
    planet_id: Mapped[int] = mapped_column(
        ForeignKey('planet.id_planet'), nullable=True)

    # Tambien puede ser un character
    character_id: Mapped[int] = mapped_column(
        ForeignKey('character.id_character'), nullable=True)

    # Relaciones, para que se pueda acceder desde otras clases a esta

    # Permite la relacion con usuario, para que se pueda acceder desde favorito a usuario, y se sincronizen
    # LAs tabals automaticamente
    user = relationship('User', back_populates='favorites')

    # En este caso, solo neceitamos la info del planeta desde Favorite no desde planeta, por eso se hace la relacion
    planet = relationship('Planet')

    # De igual forma en caracter esto permite que se pueda hacer desde user:
    # Se pueda acceder a datos de caracter desde user.favorites.character.name por ejemplo.
    character = relationship('Character')
