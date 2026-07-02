from fasthtml.common import *  # noqa: F403
from dotenv import load_dotenv
import os
import json
import xgboost as xgb
import pandas as pd

load_dotenv()

app, rt = fast_app(secret_key=os.environ.get("SESSION_SECRET"))
app = app

# --- Carga del modelo (una sola vez, al iniciar la app) ---
modelo = xgb.XGBRegressor()
modelo.load_model("models/modelo_ingresos.json")

with open("models/columnas_modelo.json") as f:
    columnas_modelo = json.load(f)

# --- Valores por defecto para las 16 variables ocultas ---
defaults = {
    "REGION": 1, "ESTRATO": 5, "C205": 2, "C311": 5, "C359": 1,
    "C361_1": 1, "C361_5": 2, "C364_1": 2,
    "C375_1": 2, "C375_2": 2, "C375_3": 2, "C375_4": 2, "C375_5": 2, "C375_6": 2,
    "C376": 10, "C377": 7,
}

def predecir_ingreso(formulario: dict) -> tuple[float, float, float]:
    entrada = {**defaults, **formulario}
    fila = pd.DataFrame([[entrada[col] for col in columnas_modelo]], columns=columnas_modelo)
    prediccion = float(modelo.predict(fila)[0])
    return prediccion, prediccion * 0.85, prediccion * 1.15

def navbar():
    return Nav(
        Div(
            # Banda roja superior estilo gob.pe
            Div(
                Div(
                    I(cls="fa-solid fa-landmark"),
                    Span(" República del Perú"),
                    cls="gov-band-inner"
                ),
                cls="gov-band"
            ),
            # Navbar principal
            Div(
                A(
                    Div(
                        Div(
                            Span("MI", cls="logo-mi"),
                            Span("ingreso", cls="logo-ingreso"),
                            Span("Peru", cls="logo-peru"),
                            cls="logo-text"
                        ),
                        P("Estimador salarial con IA · INEI - ENAHO", cls="logo-sub"),
                        cls="logo-content"
                    ),
                    href="/", cls="logo"
                ),
                Div(
                    A(I(cls="fa-solid fa-house"), Span(" Inicio"), href="#hero", cls="nav-link"),
                    A(I(cls="fa-solid fa-circle-info"), Span(" Cómo funciona"), href="#como-funciona", cls="nav-link"),
                    A(I(cls="fa-solid fa-calculator"), Span(" Predictor"), href="#predictor", cls="nav-link"),
                    A(I(cls="fa-solid fa-envelope"), Span(" Contacto"), href="#contacto", cls="nav-link"),
                    cls="nav-links"
                ),
                cls="nav-inner"
            ),
            cls="navbar-wrapper"
        ),
        cls="navbar"
    )

def hero():
    return Section(
        Div(
            Div(
                Div(
                    Span(I(cls="fa-solid fa-robot"), " Modelo de ML · Perú 2026", cls="eyebrow"),
                    H1(
                        "Predice tu ",
                        Span("ingreso mensual", cls="highlight"),
                        " con inteligencia artificial"
                    ),
                    P("Ingresa tus datos y nuestro modelo entrenado con datos reales del INEI te estima tu rango salarial en segundos.", cls="hero-sub"),
                    Div(
                        A(I(cls="fa-solid fa-play"), " Probar ahora", href="#predictor", cls="btn-primary"),
                        A(I(cls="fa-solid fa-circle-question"), " ¿Cómo funciona?", href="#como-funciona", cls="btn-ghost"),
                        cls="hero-actions"
                    ),
                    # Badges institucionales
                    Div(
                        Span(I(cls="fa-solid fa-shield-halved"), " Datos oficiales INEI", cls="badge"),
                        Span(I(cls="fa-solid fa-graduation-cap"), " Proyecto académico", cls="badge"),
                        cls="badges"
                    ),
                    cls="hero-text"
                ),
                Div(
                    Div(
                        Div(
                            I(cls="fa-solid fa-bullseye stat-icon"),
                            Div(
                                Span("Precisión del modelo", cls="stat-label"),
                                Span("87.4%", cls="stat-value"),
                                cls="stat-info"
                            ),
                            cls="stat-card"
                        ),
                        Div(
                            I(cls="fa-solid fa-database stat-icon"),
                            Div(
                                Span("Registros entrenados", cls="stat-label"),
                                Span("120K+", cls="stat-value"),
                                cls="stat-info"
                            ),
                            cls="stat-card"
                        ),
                        Div(
                            I(cls="fa-solid fa-file-lines stat-icon"),
                            Div(
                                Span("Fuente de datos", cls="stat-label"),
                                Span("ENAHO · INEI", cls="stat-value"),
                                cls="stat-info"
                            ),
                            cls="stat-card"
                        ),
                        cls="stats-grid"
                    ),
                    cls="hero-visual"
                ),
                cls="hero-inner"
            ),
        ),
        id="hero", cls="hero"
    )

def como_funciona():
    pasos = [
        ("fa-solid fa-pen-to-square", "Ingresa tus datos", "Llena el formulario con tu nivel educativo, rubro, experiencia y región."),
        ("fa-solid fa-microchip", "El modelo analiza", "Nuestro modelo de regresión entrenado en Google Colab procesa tu perfil."),
        ("fa-solid fa-chart-bar", "Obtén tu estimación", "Recibe tu rango salarial estimado y percentil dentro de tu sector."),
    ]
    return Section(
        Div(
            Span(I(cls="fa-solid fa-gears"), " Proceso", cls="eyebrow"),
            H2("Simple, rápido y transparente"),
            Div(
                *[
                    Div(
                        Div(
                            I(cls=icono),
                            cls="step-icon-wrap"
                        ),
                        H3(titulo),
                        P(desc),
                        cls="step-card"
                    )
                    for icono, titulo, desc in pasos
                ],
                cls="steps-grid"
            ),
            cls="section-inner"
        ),
        id="como-funciona", cls="section section-alt"
    )

def predictor():
    return Section(
        Div(
            Span(I(cls="fa-solid fa-calculator"), " Predictor", cls="eyebrow"),
            H2("Simula tu ingreso potencial"),
            # Aviso institucional
            Div(
                I(cls="fa-solid fa-circle-info"),
                " Proyección basada en datos EPEN del INEI sobre personas con perfil similar. No representa un ingreso garantizado.",
                cls="aviso-info"
            ),
            Form(
                Div(
                    # Nivel educativo — C366
                    Div(
                        Label(I(cls="fa-solid fa-user-graduate"), " Nivel educativo", For="educacion"),
                        Select(
                            Option("Selecciona...", value="", disabled=True, selected=True),
                            Option("Sin nivel", value="1"),
                            Option("Educación Inicial", value="2"),
                            Option("Primaria incompleta", value="3"),
                            Option("Primaria completa", value="4"),
                            Option("Secundaria incompleta", value="5"),
                            Option("Secundaria completa", value="6"),
                            Option("Básica especial", value="7"),
                            Option("Superior no universitaria incompleta", value="8"),
                            Option("Superior no universitaria completa", value="9"),
                            Option("Superior universitaria incompleta", value="10"),
                            Option("Superior universitaria completa", value="11"),
                            Option("Maestría/Doctorado", value="12"),
                            id="educacion", name="educacion", required=True
                        ),
                        cls="field"
                    ),
                    # Edad — C208
                    Div(
                        Label(I(cls="fa-solid fa-calendar-day"), " Edad", For="edad"),
                        Input(type="number", id="edad", name="edad", placeholder="Ej: 28", min="14", max="98", required=True),
                        cls="field"
                    ),
                    # Sexo — C207
                    Div(
                        Label(I(cls="fa-solid fa-venus-mars"), " Sexo", For="sexo"),
                        Select(
                            Option("Selecciona...", value="", disabled=True, selected=True),
                            Option("Hombre", value="1"),
                            Option("Mujer", value="2"),
                            id="sexo", name="sexo", required=True
                        ),
                        cls="field"
                    ),
                    # Región — REGION
                    Div(
                        Label(I(cls="fa-solid fa-map-location-dot"), " ¿En qué región buscas trabajo?", For="region"),
                        Select(
                            Option("Selecciona...", value="", disabled=True, selected=True),
                            Option("Lima Metropolitana", value="1"),
                            Option("Resto urbano", value="2"),
                            Option("Rural", value="3"),
                            id="region", name="region", required=True
                        ),
                        cls="field"
                    ),
                    # Tipo de trabajo — C310
                    Div(
                        Label(I(cls="fa-solid fa-briefcase"), " ¿Qué tipo de trabajo buscas?", For="trabajo"),
                        Select(
                            Option("Selecciona...", value="", disabled=True, selected=True),
                            Option("Empleador o patrono", value="1"),
                            Option("Trabajador independiente", value="2"),
                            Option("Empleado u obrero", value="3"),
                            Option("Trabajador del hogar", value="6"),
                            Option("Aprendiz/practicante remunerado", value="7"),
                            id="trabajo", name="trabajo", required=True
                        ),
                        cls="field"
                    ),
                    # Tamaño de empresa — C317
                    Div(
                        Label(I(cls="fa-solid fa-building"), " ¿En qué tamaño de empresa te gustaría trabajar?", For="empresa"),
                        Select(
                            Option("Selecciona...", value="", disabled=True, selected=True),
                            Option("Hasta 20 personas", value="1"),
                            Option("De 21 a 50 personas", value="2"),
                            Option("De 51 a 100 personas", value="3"),
                            Option("De 101 a 500 personas", value="4"),
                            Option("Más de 500 personas", value="5"),
                            id="empresa", name="empresa", required=True
                        ),
                        cls="field"
                    ),
                    # Formalidad — C312
                    Div(
                        Label(I(cls="fa-solid fa-file-contract"), " ¿Te interesa que sea formal (con RUC/planilla)?", For="formalidad"),
                        Select(
                            Option("Selecciona...", value="", disabled=True, selected=True),
                            Option("Sí, persona jurídica (SAC, SRL, EIRL...)", value="1"),
                            Option("Sí, persona natural con RUC", value="2"),
                            Option("No, prefiero informal", value="3"),
                            Option("No sabe / me es indiferente", value="4"),
                            id="formalidad", name="formalidad", required=True
                        ),
                        cls="field"
                    ),
                    # Seguro de salud — SEGURO1
                    Div(
                        Label(I(cls="fa-solid fa-notes-medical"), " ¿A qué seguro de salud te gustaría acceder?", For="seguro"),
                        Select(
                            Option("Selecciona...", value="", disabled=True, selected=True),
                            Option("EsSalud", value="1"),
                            Option("Seguro privado de salud", value="2"),
                            Option("Ambos", value="3"),
                            Option("Otro", value="4"),
                            Option("Seguro Integral de Salud (SIS)", value="5"),
                            Option("No afiliado", value="6"),
                            id="seguro", name="seguro", required=True
                        ),
                        cls="field"
                    ),
                    # Horas semanales — C318_T / whoraT
                    Div(
                        Label(I(cls="fa-solid fa-calendar-week"), " ¿Cuántas horas a la semana planeas trabajar?", For="horas"),
                        Input(type="number", id="horas", name="horas", placeholder="Ej: 40", min="1", max="80", required=True),
                        cls="field"
                    ),
                    # Frecuencia de pago — C338
                    Div(
                        Label(I(cls="fa-solid fa-money-bill-wave"), " ¿Cómo prefieres que te paguen?", For="pago"),
                        Select(
                            Option("Selecciona...", value="", disabled=True, selected=True),
                            Option("Diario", value="1"),
                            Option("Semanal", value="2"),
                            Option("Quincenal", value="3"),
                            Option("Mensual", value="4"),
                            id="pago", name="pago", required=True
                        ),
                        cls="field"
                    ),
                    cls="form-grid"
                ),
                Button(
                    I(cls="fa-solid fa-magnifying-glass-chart"),
                    Span(" Simular ingreso"),
                    cls="btn-primary btn-full",
                    type="submit"
                ),
                Div(
                    P(I(cls="fa-solid fa-arrow-up-from-bracket"), " Completa el formulario y presiona el botón para ver tu proyección.", cls="resultado-placeholder"),
                    id="resultado", cls="resultado-box"
                ),
                hx_post="/predecir",
                hx_target="#resultado",
                hx_swap="innerHTML",
                cls="form-wrapper", id="predictor-form"
            ),
            cls="section-inner"
        ),
        id="predictor", cls="section"
    )

def footer():
    return Footer(
        Div(
            Div(
                Span("MI", cls="logo-mi"),
                Span("ingreso", cls="logo-ingreso"),
                Span("Peru", cls="logo-peru"),
                cls="footer-logo"
            ),
            P("Modelo de machine learning para estimación salarial basado en datos del INEI - ENAHO.", cls="footer-desc"),
            Div(
                Span(I(cls="fa-solid fa-code"), " FastHTML + Google Colab", cls="footer-tag"),
                Span(I(cls="fa-solid fa-database"), " INEI · ENAHO", cls="footer-tag"),
                Span(I(cls="fa-solid fa-flask"), " Proyecto académico", cls="footer-tag"),
                cls="footer-tags"
            ),
            P(I(cls="fa-regular fa-copyright"), " 2026 MiingresoPeru — Solo con fines académicos", cls="footer-copy"),
            cls="footer-inner"
        ),
        cls="footer"
    )

@rt('/')
def get():
    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Title("MiingresoPeru — Predice tu ingreso con IA"),
            Script(src="https://unpkg.com/htmx.org@1.9.12"), 
            Link(rel='stylesheet', href='/static/fontawesome/css/all.min.css'),
            Link(rel='preconnect', href='https://fonts.googleapis.com'),
            Link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin=''),
            Link(
                rel='stylesheet',
                href='https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;600;700&family=Merriweather:wght@700&display=swap'
            ),
            Link(rel='stylesheet', href='/static/css/style.css')
        ),
        Body(
            navbar(),
            hero(),
            como_funciona(),
            predictor(),
            footer(),
            Script("""
                document.querySelectorAll('a[href^="#"]').forEach(a => {
                    a.addEventListener('click', e => {
                        e.preventDefault();
                        document.querySelector(a.getAttribute('href'))?.scrollIntoView({ behavior: 'smooth' });
                    });
                });
                window.addEventListener('scroll', () => {
                    document.querySelector('.navbar').classList.toggle('scrolled', window.scrollY > 10);
                });
                // Scroll reveal
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
                }, { threshold: 0.1 });
                document.querySelectorAll('.step-card, .stat-card, .form-wrapper').forEach(el => observer.observe(el));
            """)
        )
    )

@rt('/predecir')
async def post(educacion: str = "", edad: str = "", sexo: str = "", region: str = "",
                trabajo: str = "", empresa: str = "", formalidad: str = "",
                seguro: str = "", horas: str = "40", pago: str = ""):
    print("=" * 50)
    print("DATOS RECIBIDOS DEL FORMULARIO:")
    print(f"educacion={educacion!r}, edad={edad!r}, sexo={sexo!r}, region={region!r}")
    print(f"trabajo={trabajo!r}, empresa={empresa!r}, formalidad={formalidad!r}")
    print(f"seguro={seguro!r}, horas={horas!r}, pago={pago!r}")

    try:
        formulario = {
            "C366": int(educacion),
            "C208": int(edad),
            "C207": int(sexo),
            "REGION": int(region),
            "C310": int(trabajo),
            "C317": int(empresa),
            "C312": int(formalidad),
            "SEGURO1": int(seguro),
            "C318_T": int(horas),
            "whoraT": int(horas),
            "C338": int(pago),
        }
        print(f"Vector armado: {formulario}")

        prediccion, rango_min, rango_max = predecir_ingreso(formulario)
        print(f"✅ Predicción exitosa: S/ {prediccion:,.2f} (rango {rango_min:,.0f}-{rango_max:,.0f})")

        return Div(
            Div(
                I(cls="fa-solid fa-circle-check res-icon"),
                Div(
                    P("Ingreso mensual estimado", cls="res-label"),
                    P(f"S/ {rango_min:,.0f} — S/ {rango_max:,.0f}", cls="res-value"),
                    cls="res-data"
                ),
                cls="res-main"
            ),
            P(I(cls="fa-solid fa-triangle-exclamation"), " Proyección basada en datos EPEN del INEI. No representa un ingreso garantizado.", cls="res-note"),
            cls="resultado-content"
        )
    except (ValueError, KeyError) as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        return P(I(cls="fa-solid fa-circle-xmark"), " Completa todos los campos para obtener tu estimación.", cls="res-error")
    
if __name__ == "__main__":
    serve()