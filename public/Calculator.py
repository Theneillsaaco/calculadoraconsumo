#  Calculadora de Consumo Eléctrico - Centro Escolar

from dataclasses import dataclass, field
from typing import List
import json

# Tarifa eléctrica por defecto (CUP/kWh) - ajustable
TARIFA_DEFAULT = 0.09


@dataclass
class AireAcondicionado:
    nombre: str
    cantidad: int
    capacidad_btu: int        # BTU del equipo (ej. 12000 = 1 ton)
    horas_dia: float
    dias_semana: int = 5
    eer: float = 9.0          # Energy Efficiency Ratio (BTU/W) 

    @property
    def potencia_kw(self) -> float:
        """Potencia en kW de UN equipo"""
        return (self.capacidad_btu / self.eer) / 1000

    @property
    def consumo_dia_kwh(self) -> float:
        return self.potencia_kw * self.horas_dia * self.cantidad

    @property
    def consumo_semana_kwh(self) -> float:
        return self.consumo_dia_kwh * self.dias_semana

    @property
    def consumo_mes_kwh(self) -> float:
        return self.consumo_semana_kwh * 4.33  # promedio semanas/mes


@dataclass
class Espacio:
    nombre: str
    horario_inicio: float     # hora decimal (7 = 7:00, 7.5 = 7:30)
    horario_fin: float
    aires: List[AireAcondicionado] = field(default_factory=list)
    dias_semana: int = 5
    tipo_tgm: str = ""        # TGM 3, AUX, etc.

    @property
    def horas_operacion(self) -> float:
        return self.horario_fin - self.horario_inicio

    @property
    def consumo_dia_kwh(self) -> float:
        return sum(a.consumo_dia_kwh for a in self.aires)

    @property
    def consumo_semana_kwh(self) -> float:
        return sum(a.consumo_semana_kwh for a in self.aires)

    @property
    def consumo_mes_kwh(self) -> float:
        return sum(a.consumo_mes_kwh for a in self.aires)

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "horario": f"{self.horario_inicio:.0f}:00 – {self.horario_fin:g}:{'00' if self.horario_fin == int(self.horario_fin) else '30'}",
            "horas_operacion": self.horas_operacion,
            "tipo_tgm": self.tipo_tgm,
            "aires": [
                {
                    "descripcion": f"{a.cantidad}x {a.capacidad_btu} BTU",
                    "potencia_unitaria_kw": round(a.potencia_kw, 3),
                    "potencia_total_kw": round(a.potencia_kw * a.cantidad, 3),
                }
                for a in self.aires
            ],
            "consumo_dia_kwh": round(self.consumo_dia_kwh, 2),
            "consumo_semana_kwh": round(self.consumo_semana_kwh, 2),
            "consumo_mes_kwh": round(self.consumo_mes_kwh, 2),
        }


# BTU estándar por tamaño de unidad
BTU_MAP = {
    12: 12000,   # 1 tonelada
    16: 18000,   # 1.5 toneladas  ← tus unidades de 16
    21: 24000,   # 2 toneladas    ← tus unidades de 21
    24: 24000,
    36: 36000,
}


def calcular_centro(tarifa: float = TARIFA_DEFAULT, dias_semana: int = 5) -> dict:
    """
    Calcula el consumo de todos los espacios del centro.
    Parámetros ajustables desde la UI.
    """

    espacios = [
        Espacio(
            nombre="Salón de Maestros",
            horario_inicio=7,
            horario_fin=16.5,
            tipo_tgm="TGM 3",
            dias_semana=dias_semana,
            aires=[
                AireAcondicionado("Split 21", cantidad=2, capacidad_btu=BTU_MAP[21],
                                  horas_dia=9.5, dias_semana=dias_semana),
            ]
        ),
        Espacio(
            nombre="Caja",
            horario_inicio=7,
            horario_fin=18.5,
            tipo_tgm="TGM 3",
            dias_semana=dias_semana,
            aires=[
                AireAcondicionado("Split 16", cantidad=3, capacidad_btu=BTU_MAP[16],
                                  horas_dia=11.5, dias_semana=dias_semana),
            ]
        ),
        Espacio(
            nombre="Dirección",
            horario_inicio=7,
            horario_fin=20,
            tipo_tgm="Midea Confort Time",
            dias_semana=dias_semana,
            aires=[
                AireAcondicionado("Split 16", cantidad=2, capacidad_btu=BTU_MAP[16],
                                  horas_dia=13, dias_semana=dias_semana),
            ]
        ),
        Espacio(
            nombre="Salón de Informática",
            horario_inicio=0,
            horario_fin=1,
            tipo_tgm="AUX",
            dias_semana=dias_semana,
            aires=[
                AireAcondicionado("Split 21", cantidad=1, capacidad_btu=BTU_MAP[21],
                                  horas_dia=1, dias_semana=dias_semana),
            ]
        ),
        Espacio(
            nombre="Salón Multiusos",
            horario_inicio=0,
            horario_fin=5,
            tipo_tgm="Gree",
            dias_semana=dias_semana,
            aires=[
                AireAcondicionado("Gree 21", cantidad=2, capacidad_btu=BTU_MAP[21],
                                  horas_dia=5, dias_semana=dias_semana),
            ]
        ),
    ]

    total_dia = sum(e.consumo_dia_kwh for e in espacios)
    total_semana = sum(e.consumo_semana_kwh for e in espacios)
    total_mes = sum(e.consumo_mes_kwh for e in espacios)

    return {
        "espacios": [e.to_dict() for e in espacios],
        "totales": {
            "consumo_dia_kwh": round(total_dia, 2),
            "consumo_semana_kwh": round(total_semana, 2),
            "consumo_mes_kwh": round(total_mes, 2),
            "costo_dia": round(total_dia * tarifa, 2),
            "costo_semana": round(total_semana * tarifa, 2),
            "costo_mes": round(total_mes * tarifa, 2),
        },
        "parametros": {
            "tarifa": tarifa,
            "dias_semana": dias_semana,
        }
    }


# Punto de entrada cuando Pyodide lo ejecuta
def run(tarifa=TARIFA_DEFAULT, dias_semana=5):
    result = calcular_centro(float(tarifa), int(dias_semana))
    return json.dumps(result)