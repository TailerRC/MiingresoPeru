# MiingresoPeru
### Simulador predictivo de ingresos para la página del gobierno peruano
**Universidad Ricardo Palma — Curso: Inteligencia Artificial**

---

## Descripción

MiingresoPeru es una aplicación web que proyecta el ingreso mensual potencial de una persona en Perú según el tipo de trabajo al que aspira. Utiliza un modelo de Machine Learning (XGBoost) entrenado con datos reales de la **Encuesta Permanente de Empleo Nacional (EPEN)** del INEI, y fue desarrollado como proyecto académico del curso de Inteligencia Artificial.

A diferencia de una calculadora tradicional que exige el trabajo actual de la persona, MiingresoPeru funciona como un **simulador de escenarios**: el usuario indica su nivel educativo, edad, región y el tipo de empleo al que aspira (categoría ocupacional, tamaño de empresa, formalidad, horas y frecuencia de pago deseadas), y el modelo devuelve un rango de ingreso mensual estimado en soles. Esto lo hace útil tanto para personas empleadas que quieren comparar escenarios, como para personas desempleadas que buscan orientación sobre cuánto podrían ganar.

---

## Tecnologías

| Capa | Herramienta |
|---|---|
| Frontend / Backend | FastHTML (Python) |
| Modelo ML | XGBoost (scikit-learn / xgboost) |
| Entrenamiento | Google Colab |
| Datos | EPEN (Encuesta Permanente de Empleo Nacional) · INEI |
| Estilos | CSS personalizado · Font Awesome |

---

## Variables del modelo

El modelo fue entrenado con 26 variables predictoras extraídas del diccionario de datos EPEN. Las 10 con mayor peso en la predicción (~77% de la importancia total) son las que se muestran en el formulario:

| Variable | Descripción | Importancia |
|---|---|---|
| C366 | Nivel educativo alcanzado | 18.4% |
| C310 | Categoría ocupacional (empleador, independiente, empleado...) | 14.9% |
| C317 | Tamaño de la empresa/negocio | 11.5% |
| SEGURO1 | Sistema de seguro de salud | 10.9% |
| C208 | Edad | 5.9% |
| C375_1 | Limitación motora permanente | 5.1% |
| C312 | Formalidad del negocio (registro SUNAT) | 4.9% |
| C318_T | Horas trabajadas por semana | 3.5% |
| C338 | Frecuencia de pago | 3.5% |
| whoraT | Horas totales trabajadas | 3.5% |

Las 16 variables restantes (REGION, ESTRATO, sexo, seguros específicos, discapacidad detallada, etnicidad, etc.) se completan automáticamente en el backend con valores por defecto o la moda del dataset, sin mostrarse al usuario.

---

## Estructura del proyecto

```
MIINGRESOPERU/
├── models/
│   └── modelo_ingresos.pkl      # Modelo entrenado exportado desde Colab
├── static/
│   ├── css/
│   └── fontawesome/
├── dataset/                     # Dataset EPEN
├── .env
├── main.py
├── requirements.txt
└── README.md
```

---

## Cómo ejecutar

```powershell
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la aplicación
uvicorn main:app --reload --port 5001

# 3. Abrir en el navegador
http://localhost:5001
```

---

## Notas

- Esta herramienta ofrece una **proyección estimada**, no un ingreso garantizado, y es solo con fines académicos e informativos.

---

*Universidad Ricardo Palma · 2026*