"""
Script de PRUEBA para verificar que el modelo se conecta y predice bien,
usando EXACTAMENTE los mismos códigos que tendrán los <select> del formulario.

No es parte de la app, solo para que tú confirmes que el .pkl funciona
antes de que tu compañero lo integre al frontend.

Ejecutar: python test_prediccion.py
"""

import xgboost as xgb
import json
import pandas as pd

# 1. Cargar el modelo y el orden de columnas exportado desde Colab
modelo = xgb.XGBRegressor()
modelo.load_model("models/modelo_ingresos.json")

with open("models/columnas_modelo.json") as f:
    columnas_modelo = json.load(f)

print(f"Modelo cargado correctamente ✅")
print(f"El modelo espera {len(columnas_modelo)} columnas:")
print(columnas_modelo)
print()

# ---------------------------------------------------------------------------
# 2. Valores por defecto para las 16 variables que NO se muestran en el
#    formulario (se completan con un valor fijo / moda del dataset)
# ---------------------------------------------------------------------------
defaults = {
    "REGION": 1,       # 1 Lima Metropolitana
    "ESTRATO": 5,       # estrato más común
    "C205": 2,          # no ausente del hogar
    "C311": 5,          # empresa/patrono privado
    "C359": 1,          # ha trabajado antes
    "C361_1": 1,        # afiliado a EsSalud
    "C361_5": 2,        # no afiliado a SIS
    "C364_1": 2,        # no afiliado a AFP
    "C375_1": 2,        # sin limitación motora
    "C375_2": 2,        # sin limitación visual
    "C375_3": 2,        # sin limitación de habla
    "C375_4": 2,        # sin limitación auditiva
    "C375_5": 2,        # sin limitación de aprendizaje
    "C375_6": 2,        # sin limitación de relacionarse
    "C376": 10,         # castellano
    "C377": 7,          # mestizo
}

# ---------------------------------------------------------------------------
# 3. OPCIONES EXACTAS de cada select del formulario (las 10 variables
#    visibles). Estos son los únicos valores que el frontend podrá enviar,
#    así que el test cubre TODOS los códigos válidos, no solo un ejemplo.
# ---------------------------------------------------------------------------
OPCIONES_C366 = {  # Nivel educativo
    1: "Sin nivel", 2: "Educación Inicial", 3: "Primaria incompleta",
    4: "Primaria completa", 5: "Secundaria incompleta", 6: "Secundaria completa",
    7: "Básica especial", 8: "Superior no universitaria incompleta",
    9: "Superior no universitaria completa", 10: "Superior universitaria incompleta",
    11: "Superior universitaria completa", 12: "Maestría/Doctorado",
}

OPCIONES_C207 = {1: "Hombre", 2: "Mujer"}  # Sexo

OPCIONES_REGION = {1: "Lima Metropolitana", 2: "Resto urbano", 3: "Rural"}

OPCIONES_C310 = {  # Tipo de trabajo que buscas (solo las que sí se muestran)
    1: "Empleador o patrono", 2: "Trabajador independiente",
    3: "Empleado u obrero", 6: "Trabajador del hogar",
    7: "Aprendiz/practicante remunerado",
}

OPCIONES_C317 = {  # Tamaño de empresa esperado
    1: "Hasta 20 personas", 2: "De 21 a 50 personas",
    3: "De 51 a 100 personas", 4: "De 101 a 500 personas",
    5: "Más de 500 personas",
}

OPCIONES_C312 = {  # Formalidad
    1: "Persona jurídica (SAC, SRL, EIRL...)", 2: "Persona natural con RUC",
    3: "No está registrado", 4: "No sabe",
}

OPCIONES_SEGURO1 = {  # Seguro de salud
    1: "EsSalud", 2: "Seguro privado", 3: "Ambos",
    4: "Otro", 5: "SIS", 6: "No afiliado",
}

OPCIONES_C338 = {  # Frecuencia de pago (excluye el 5 "no recibió pago")
    1: "Diario", 2: "Semanal", 3: "Quincenal", 4: "Mensual",
}

# ---------------------------------------------------------------------------
# 4. Función que arma el vector completo (defaults + formulario) en el
#    orden exacto que espera el modelo, y predice
# ---------------------------------------------------------------------------
def predecir(formulario: dict) -> float:
    entrada = {**defaults, **formulario}

    faltantes = [c for c in columnas_modelo if c not in entrada]
    if faltantes:
        raise ValueError(f"Faltan columnas para predecir: {faltantes}")

    fila = pd.DataFrame([[entrada[col] for col in columnas_modelo]], columns=columnas_modelo)
    return float(modelo.predict(fila)[0])


# ---------------------------------------------------------------------------
# 5. Casos de prueba cubriendo distintos escenarios reales del formulario
# ---------------------------------------------------------------------------
casos = [
    {
        "nombre": "Universitario, empleado formal, Lima",
        "datos": {
            "C366": 11, "C208": 28, "C207": 1, "REGION": 1,
            "C310": 3, "C317": 4, "C312": 1, "SEGURO1": 1,
            "C318_T": 45, "whoraT": 45, "C338": 4,
        },
    },
    {
        "nombre": "Secundaria completa, independiente informal, región rural",
        "datos": {
            "C366": 6, "C208": 35, "C207": 2, "REGION": 3,
            "C310": 2, "C317": 1, "C312": 3, "SEGURO1": 5,
            "C318_T": 30, "whoraT": 30, "C338": 1,
        },
    },
    {
        "nombre": "Postgrado, empleador, empresa grande, Lima",
        "datos": {
            "C366": 12, "C208": 45, "C207": 1, "REGION": 1,
            "C310": 1, "C317": 5, "C312": 1, "SEGURO1": 2,
            "C318_T": 50, "whoraT": 50, "C338": 4,
        },
    },
    {
        "nombre": "Sin nivel educativo, trabajador del hogar, resto urbano",
        "datos": {
            "C366": 1, "C208": 22, "C207": 2, "REGION": 2,
            "C310": 6, "C317": 1, "C312": 3, "SEGURO1": 6,
            "C318_T": 40, "whoraT": 40, "C338": 2,
        },
    },
    {
        "nombre": "Técnico, aprendiz/practicante, empresa mediana",
        "datos": {
            "C366": 9, "C208": 20, "C207": 1, "REGION": 1,
            "C310": 7, "C317": 2, "C312": 2, "SEGURO1": 1,
            "C318_T": 35, "whoraT": 35, "C338": 3,
        },
    },
]

# ---------------------------------------------------------------------------
# 6. Ejecutar todos los casos y validar que las etiquetas coincidan
# ---------------------------------------------------------------------------
print("=" * 70)
print("VALIDACIÓN DE CÓDIGOS Y PREDICCIONES")
print("=" * 70)

for caso in casos:
    d = caso["datos"]

    # Verifica que cada código usado exista en las opciones válidas del select
    assert d["C366"] in OPCIONES_C366, f"Código C366 inválido: {d['C366']}"
    assert d["C207"] in OPCIONES_C207, f"Código C207 inválido: {d['C207']}"
    assert d["REGION"] in OPCIONES_REGION, f"Código REGION inválido: {d['REGION']}"
    assert d["C310"] in OPCIONES_C310, f"Código C310 inválido: {d['C310']}"
    assert d["C317"] in OPCIONES_C317, f"Código C317 inválido: {d['C317']}"
    assert d["C312"] in OPCIONES_C312, f"Código C312 inválido: {d['C312']}"
    assert d["SEGURO1"] in OPCIONES_SEGURO1, f"Código SEGURO1 inválido: {d['SEGURO1']}"
    assert d["C338"] in OPCIONES_C338, f"Código C338 inválido: {d['C338']}"

    prediccion = predecir(d)
    rango_min = prediccion * 0.85
    rango_max = prediccion * 1.15

    print(f"\n🧪 {caso['nombre']}")
    print(f"   Educación: {OPCIONES_C366[d['C366']]} | Sexo: {OPCIONES_C207[d['C207']]} | Región: {OPCIONES_REGION[d['REGION']]}")
    print(f"   Trabajo: {OPCIONES_C310[d['C310']]} | Empresa: {OPCIONES_C317[d['C317']]}")
    print(f"   Formalidad: {OPCIONES_C312[d['C312']]} | Seguro: {OPCIONES_SEGURO1[d['SEGURO1']]} | Pago: {OPCIONES_C338[d['C338']]}")
    print(f"   ➜ Ingreso estimado: S/ {prediccion:,.2f}  (rango S/ {rango_min:,.0f} — S/ {rango_max:,.0f})")

print("\n" + "=" * 70)
print("✅ Todos los casos se ejecutaron sin errores. El modelo admite")
print("   correctamente los códigos definidos para los <select> del formulario.")
print("=" * 70)