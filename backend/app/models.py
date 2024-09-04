import uuid
from decimal import Decimal
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel,Session,create_engine,select
import datetime
from .cpf import generate_cpf
from sqlalchemy import LargeBinary,Column
import base64

class TreinadorBase(SQLModel):
    telefone: str | None = Field(max_length=11,default=None,unique=True,foreign_key= "telefone.telefone")
    name: str | None = Field(default=None, max_length=255)
    especialidade: str | None = Field(default=None, max_length=255)

# Properties to receive via API on update, all are optional
class TreinadorUpdate(TreinadorBase):
    telefone: str | None = Field(max_length=11,default=None,unique=True,foreign_key= "telefone.telefone")
    especialidade: str | None = Field(default=None, min_length=8, max_length=40)

    
class Treinador(TreinadorBase, table=True):
    id: str = Field(default=None, primary_key=True,max_length=11)

class TreinadorPublic(TreinadorBase):
    telefone: str | None = Field(max_length=11,default=None,unique=True,foreign_key= "telefone.telefone")
    name: str | None = Field(default=None, max_length=255)
    especialidade: str | None = Field(default=None, max_length=255)

class TreinadoresPublic(SQLModel):
    data: list[TreinadorPublic]
    count: int
    
class TreinadorCreate(TreinadorBase):
    id: str = Field(default=None, primary_key=True,max_length=11)
    telefone: str | None = Field(default=None, unique=True,max_length=11)
    name: str | None = Field(default=None, max_length=255)
    especialidade: str | None = Field(default=None, max_length=255)
class TelefoneBase(SQLModel):
    telefone: str = Field(default=None, primary_key=True,max_length=11)

class Telefone(TelefoneBase,table=True):
    pass

class TelefoneCreate(TelefoneBase):
    telefone: str = Field(default=None, primary_key=True,max_length=11)

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    birthdate: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    cpf: str = Field(default=generate_cpf(),unique=True,max_length=11)
    password: str = Field(min_length=8, max_length=40)
    email: EmailStr = Field(unique=True, index=True, max_length=255)

class UserRegister(SQLModel):
    cpf: str = Field(default=generate_cpf(),unique=True,max_length=11)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    birthdate: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    cpf: str = Field(default=generate_cpf(),unique=True,max_length=11)
    hashed_password: str

    # items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    email: str
    birthdate: datetime.datetime
    name: str


class TelefonePublic(Telefone):
    telefone: str

class TelefonesPublic(SQLModel):
    data: list[TelefonePublic]
    count: int
    
# class ItemsPublic(SQLModel):
#     data: list[ItemPublic]
#     count: int

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# # Shared properties
# class ItemBase(SQLModel):
#     title: str = Field(min_length=1, max_length=255)
#     description: str | None = Field(default=None, max_length=255)


# # Properties to receive on item creation
# class ItemCreate(ItemBase):
#     pass


# # Properties to receive on item update
# class ItemUpdate(ItemBase):
#     title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
# class Item(ItemBase, table=True):
    # id: uuid.UUID = Field(default_factory=None, primary_key=True)
    # title: str = Field(max_length=255)
# # Database model, database table inferred from class name
# class Item(ItemBase, table=True):
#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     title: str = Field(max_length=255)
#     owner_id: uuid.UUID = Field(
#         foreign_key="user.id", nullable=False, ondelete="CASCADE"
#     )
#     owner: User | None = Relationship(back_populates="items")

# # Properties to return via API, id is always required
# class ItemPublic(ItemBase):
#     id: uuid.UUID
#     owner_id: uuid.UUID


# class ItemsPublic(SQLModel):
#     data: list[ItemPublic]
#     count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)

##########LUCAS###########################

class RefeicaoBase(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    calorias: int | None = Field(default=None)

class Refeicao(RefeicaoBase,table=True):
    id: int = Field(default_factory=None, primary_key=True)
    
class RefeicaoCreate(RefeicaoBase):
    id: int

class RefeicaoPublic(Refeicao):
    name: str
    calorias: int

class RefeicoesPublic(SQLModel):
    data: list[RefeicaoPublic]
    count: int

class DietaBase(SQLModel):
    id_ref_manha: int | None = Field(default=None, foreign_key="refeicao.id")
    id_ref_tarde: int | None = Field(default=None, foreign_key="refeicao.id")
    id_ref_noite: int | None = Field(default=None, foreign_key="refeicao.id")

class Dieta(DietaBase,table=True):
    id: int = Field(default_factory=None, primary_key=True)

class DietaCreate(DietaBase):
    id: int


class DietaPublic(Dieta):
    id: int
    id_ref_manha: int
    id_ref_tarde: int
    id_ref_noite: int
    
class DietasPublic(SQLModel):
    data: list[DietaPublic]
    count: int

class PlanoBase(SQLModel):
    id: int | None = Field(default_factory=None, primary_key=True)
    id_user: uuid.UUID = Field(default_factory=uuid.uuid4, foreign_key="user.id")
    id_dieta: int | None = Field(default_factory=None)
    id_sessao_treino: int | None = Field(default_factory=None)
    id_treinador: int | None = Field(default_factory=None)
    id_avaliacao : int | None = Field(default_factory = None)
    local: str | None = Field(default_factory=None)

class PlanoCreate(PlanoBase):
    id_dieta: int | None = Field(default_factory=None)
    id_sessao_treino: int | None = Field(default_factory=None)
    id_treinador: int | None = Field(default_factory=None)
    id_avaliacao : int | None = Field(default_factory = None)
    local: str | None = Field(default_factory=None)



class PlanoUpdate(PlanoBase):
    id_dieta: int | None = Field(default_factory=None)
    id_sessao_treino: int | None = Field(default_factory=None)
    id_treinador: int | None = Field(default_factory=None)
    id_avaliacao : int | None = Field(default_factory = None)
    local: str | None = Field(default_factory=None)

class Plano(PlanoBase, table=True):
    pass
class PlanoPublic(PlanoBase):
    pass

class PlanosPublic(SQLModel):
    data: list[PlanoPublic]
    count: int


class AvaliacaoBase(SQLModel):
    data_avaliacao: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    peso: float = Field(default = 0.0)
    altura: float = Field(default = 0.0)
    perc_gordura: float = Field(default = 0.0)
    
class AvaliacaoCreate(AvaliacaoBase):
    id: int | None = Field(default=None,primary_key=True) 


class AvaliacaoUpdate(AvaliacaoBase):
    data_avaliacao: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    peso: float = Field(default = 0.0)
    altura: float = Field(default = 0.0)
    perc_gordura: float = Field(default = 0.0)


class Avaliacao(AvaliacaoBase, table=True):
    id: int | None = Field(default=None,primary_key=True) 

class AvaliacaoPublic(AvaliacaoBase):
    id: int


class AvaliacoesPublic(SQLModel):
    data: list[AvaliacaoPublic]
    count: int
    
class ShapeBase(SQLModel):
    nome_foto: str = Field(primary_key=True)
class Shape(ShapeBase, table=True):
    foto: bytes | None = Field(default=None, sa_column=Column(LargeBinary))
class ShapeCreate(ShapeBase):
    pass
class ShapeDelete(Shape):
    pass

class ShapePublic(Shape):
    nome_foto: str
    foto: str | None = None  # Use str to store base64 encoded string

    @classmethod
    def from_orm(cls, shape):
        # Base64 encode the binary data
        foto_encoded = base64.b64encode(shape.foto).decode('utf-8') if shape.foto else None
        return cls(nome_foto=shape.nome_foto, foto=foto_encoded)

class ShapesPublic(SQLModel):
    data: list[ShapePublic]
    count: int
