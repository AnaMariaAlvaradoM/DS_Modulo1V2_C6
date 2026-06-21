from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class PrediccionCancelacion(Base):
    __tablename__ = "predicciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_pedido: Mapped[str] = mapped_column(String(20))
    categoria: Mapped[str] = mapped_column(String(50))
    valor_pedido: Mapped[float] = mapped_column(Float)
    prob_cancelacion: Mapped[float] = mapped_column(Float)
    prediccion: Mapped[bool] = mapped_column(Boolean)      # True = se cancelará
    modelo_version: Mapped[str] = mapped_column(String(20))
    creado_en: Mapped[datetime] = mapped_column(DateTime)

engine = create_engine("sqlite:///rappi_produccion.db", echo=False)

Base.metadata.create_all(engine)

print("[modelos_db.py] Tabla lista en rappi_produccion.db")