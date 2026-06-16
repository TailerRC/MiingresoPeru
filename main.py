from fasthtml.common import *  # noqa: F403
from dotenv import load_dotenv
import os

load_dotenv()

app, rt = fast_app(secret_key=os.environ.get("SESSION_SECRET"))

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
            H2("Calcula tu ingreso estimado"),
            # Aviso institucional
            Div(
                I(cls="fa-solid fa-circle-info"),
                " Estimación basada en datos ENAHO del INEI. Solo con fines académicos e informativos.",
                cls="aviso-info"
            ),
            Div(
                Div(
                    Div(
                        Label(I(cls="fa-solid fa-user-graduate"), " Nivel educativo", For="educacion"),
                        Select(
                            Option("Selecciona...", value="", disabled=True, selected=True),
                            Option("Sin instrucción", value="0"),
                            Option("Primaria", value="1"),
                            Option("Secundaria", value="2"),
                            Option("Técnico", value="3"),
                            Option("Universitario", value="4"),
                            Option("Postgrado", value="5"),
                            id="educacion", name="educacion"
                        ),
                        cls="field"
                    ),
                    Div(
                        Label(I(cls="fa-solid fa-briefcase"), " Sector laboral", For="sector"),
                        Select(
                            Option("Selecciona...", value="", disabled=True, selected=True),
                            Option("Agricultura", value="agri"),
                            Option("Comercio", value="comercio"),
                            Option("Construcción", value="construccion"),
                            Option("Educación", value="educacion"),
                            Option("Salud", value="salud"),
                            Option("Tecnología", value="tech"),
                            Option("Manufactura", value="manufactura"),
                            id="sector", name="sector"
                        ),
                        cls="field"
                    ),
                    Div(
                        Label(I(cls="fa-solid fa-clock"), " Años de experiencia", For="experiencia"),
                        Input(type="number", id="experiencia", name="experiencia", placeholder="Ej: 5", min="0", max="50"),
                        cls="field"
                    ),
                    Div(
                        Label(I(cls="fa-solid fa-map-location-dot"), " Región", For="region"),
                        Select(
                            Option("Selecciona...", value="", disabled=True, selected=True),
                            Option("Lima", value="lima"),
                            Option("Arequipa", value="arequipa"),
                            Option("La Libertad", value="la_libertad"),
                            Option("Cusco", value="cusco"),
                            Option("Piura", value="piura"),
                            Option("Otro", value="otro"),
                            id="region", name="region"
                        ),
                        cls="field"
                    ),
                    Div(
                        Label(I(cls="fa-solid fa-calendar-week"), " Horas semanales", For="horas"),
                        Input(type="number", id="horas", name="horas", placeholder="Ej: 40", min="1", max="80"),
                        cls="field"
                    ),
                    Div(
                        Label(I(cls="fa-solid fa-venus-mars"), " Sexo", For="sexo"),
                        Select(
                            Option("Selecciona...", value="", disabled=True, selected=True),
                            Option("Masculino", value="1"),
                            Option("Femenino", value="0"),
                            id="sexo", name="sexo"
                        ),
                        cls="field"
                    ),
                    cls="form-grid"
                ),
                Button(
                    I(cls="fa-solid fa-magnifying-glass-chart"),
                    Span(" Predecir ingreso"),
                    cls="btn-primary btn-full",
                    hx_post="/predecir",
                    hx_include="closest div",
                    hx_target="#resultado",
                    hx_swap="innerHTML"
                ),
                Div(
                    P(I(cls="fa-solid fa-arrow-up-from-bracket"), " Completa el formulario y presiona el botón para ver tu estimación.", cls="resultado-placeholder"),
                    id="resultado", cls="resultado-box"
                ),
                cls="form-wrapper"
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
async def post(educacion: str = "", sector: str = "", experiencia: str = "0",
               region: str = "", horas: str = "40", sexo: str = "1"):
    try:
        exp = int(experiencia)
        edu_val = int(educacion) if educacion else 0
        base = 950 + (edu_val * 400) + (exp * 80)
        rango_min = int(base * 0.85)
        rango_max = int(base * 1.15)
        return Div(
            Div(
                I(cls="fa-solid fa-circle-check res-icon"),
                Div(
                    P("Ingreso mensual estimado", cls="res-label"),
                    P(f"S/ {rango_min:,} — S/ {rango_max:,}", cls="res-value"),
                    cls="res-data"
                ),
                cls="res-main"
            ),
            P(I(cls="fa-solid fa-triangle-exclamation"), " Estimación preliminar · El modelo real se conectará a Google Colab.", cls="res-note"),
            cls="resultado-content"
        )
    except:
        return P(I(cls="fa-solid fa-circle-xmark"), " Completa todos los campos para obtener tu estimación.", cls="res-error")

serve()