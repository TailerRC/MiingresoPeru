# MiingresoPeru
### Propuesta de calculadora predictiva de ingresos para la página del gobierno peruano
**Universidad Ricardo Palma — Curso: Inteligencia Artificial**

---

## Descripción

MiingresoPeru es una aplicación web que estima el ingreso mensual de un trabajador peruano a partir de su perfil laboral y educativo. Utiliza un modelo de Machine Learning (XGBoost / Random Forest) entrenado con datos reales de la **Encuesta Nacional de Hogares (ENAHO)** del INEI, y fue desarrollada como proyecto académico del curso de Inteligencia Artificial.

El usuario ingresa datos como nivel educativo, sector laboral, experiencia, región y horas semanales, y el modelo devuelve un rango salarial estimado en soles.

---

## Tecnologías

| Capa | Herramienta |
|---|---|
| Frontend / Backend | FastHTML (Python) |
| Modelo ML | XGBoost · Random Forest (scikit-learn) |
| Entrenamiento | Google Colab |
| Datos | ENAHO 2025 · INEI |
| Estilos | CSS personalizado · Font Awesome |

---

## Estructura del proyecto

```
MIINGRESOPERU/
├── models/
│   └── modelo_ingresos.pkl      # Modelo entrenado exportado desde Colab
├── static/
│   ├── css/
│   └── fontawesome/
├── dataset/                     # Dataset ENAHO (no incluido en repo)
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

- Los datos del ENAHO no se incluyen en el repositorio por su tamaño.
- El modelo `.pkl` debe generarse desde el notebook de Google Colab y colocarse en la carpeta `models/`.
- Esta herramienta es solo con fines académicos e informativos.

---

*Universidad Ricardo Palma · 2026*