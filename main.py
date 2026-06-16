from fasthtml.common import *  # noqa: F403

app, rt = fast_app()

def navbar():
    return Nav(
        Div(
            A(
                Span("MI", cls="logo-accent"),
                Span("ingresoPeru"),
                href="/", cls="logo"
            ),
            Div(
                A("Inicio", href="#hero", cls="nav-link"),
                A("Cómo funciona", href="#como-funciona", cls="nav-link"),
                A("Predictor", href="#predictor", cls="nav-link"),
                A("Contacto", href="#contacto", cls="nav-link"),
                cls="nav-links"
            ),
            cls="nav-inner"
        ),
        cls="navbar"
    )

def hero():
    return Section(
        Div(
            Div(
                P("Modelo de ML · Perú 2026", cls="eyebrow"),
                H1(
                    "Predice tu ",
                    Span("ingreso mensual", cls="highlight"),
                    " con inteligencia artificial"
                ),
                P("Ingresa tus datos y nuestro modelo entrenado con datos reales del INEI te estima tu rango salarial en segundos.", cls="hero-sub"),
                Div(
                    A("Probar ahora", href="#predictor", cls="btn-primary"),
                    A("¿Cómo funciona?", href="#como-funciona", cls="btn-ghost"),
                    cls="hero-actions"
                ),
                cls="hero-text"
            ),
            Div(
                Div(
                    Div(
                        Span("Precisión del modelo", cls="stat-label"),
                        Span("87.4%", cls="stat-value"),
                        cls="stat-card"
                    ),
                    Div(
                        Span("Registros entrenados", cls="stat-label"),
                        Span("120K+", cls="stat-value"),
                        cls="stat-card"
                    ),
                    Div(
                        Span("Fuente de datos", cls="stat-label"),
                        Span("ENAHO · INEI", cls="stat-value"),
                        cls="stat-card"
                    ),
                    cls="stats-grid"
                ),
                cls="hero-visual"
            ),
            cls="hero-inner"
        ),
        id="hero", cls="hero"
    )

def como_funciona():
    pasos = [
        ("01", "Ingresa tus datos", "Llena el formulario con tu nivel educativo, rubro, experiencia y región."),
        ("02", "El modelo analiza", "Nuestro modelo de regresión entrenado en Google Colab procesa tu perfil."),
        ("03", "Obtén tu estimación", "Recibe tu rango salarial estimado y percentil dentro de tu sector."),
    ]
    return Section(
        Div(
            P("Proceso", cls="eyebrow"),
            H2("Simple, rápido y transparente"),
            Div(
                *[
                    Div(
                        Span(num, cls="step-num"),
                        H3(titulo),
                        P(desc),
                        cls="step-card"
                    )
                    for num, titulo, desc in pasos
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
            P("Predictor", cls="eyebrow"),
            H2("Calcula tu ingreso estimado"),
            Div(
                Div(
                    Div(
                        Label("Nivel educativo", For="educacion"),
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
                        Label("Sector laboral", For="sector"),
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
                        Label("Años de experiencia", For="experiencia"),
                        Input(type="number", id="experiencia", name="experiencia", placeholder="Ej: 5", min="0", max="50"),
                        cls="field"
                    ),
                    Div(
                        Label("Región", For="region"),
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
                        Label("Horas semanales", For="horas"),
                        Input(type="number", id="horas", name="horas", placeholder="Ej: 40", min="1", max="80"),
                        cls="field"
                    ),
                    Div(
                        Label("Sexo", For="sexo"),
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
                    Span("Predecir ingreso"),
                    cls="btn-primary btn-full",
                    hx_post="/predecir",
                    hx_include="closest div",
                    hx_target="#resultado",
                    hx_swap="innerHTML"
                ),
                Div(
                    P("Completa el formulario y presiona el botón para ver tu estimación.", cls="resultado-placeholder"),
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
                A(
                    Span("MI", cls="logo-accent"),
                    Span("ingresoPeru"),
                    href="/", cls="logo"
                ),
                P("Modelo de machine learning para estimación salarial basado en datos del INEI - ENAHO.", cls="footer-desc"),
                cls="footer-brand"
            ),
            Div(
                P("Proyecto académico desarrollado con FastHTML + Google Colab.", cls="footer-note"),
                P("© 2026 MiingresoPeru", cls="footer-copy"),
                cls="footer-meta"
            ),
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

            Link(rel='preconnect', href='https://fonts.googleapis.com'),
            Link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin=''),
            Link(
                rel='stylesheet',
                href='https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500&display=swap'
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
                // Smooth scroll
                document.querySelectorAll('a[href^="#"]').forEach(a => {
                    a.addEventListener('click', e => {
                        e.preventDefault();
                        document.querySelector(a.getAttribute('href'))?.scrollIntoView({ behavior: 'smooth' });
                    });
                });
                // Navbar scroll effect
                window.addEventListener('scroll', () => {
                    document.querySelector('.navbar').classList.toggle('scrolled', window.scrollY > 40);
                });
            """)
        )
    )

@rt('/predecir')
async def post(educacion: str = "", sector: str = "", experiencia: str = "0",
               region: str = "", horas: str = "40", sexo: str = "1"):
    # Aquí irá la llamada a tu modelo en Google Colab vía ngrok
    # Por ahora retorna un mock
    try:
        exp = int(experiencia)
        edu_val = int(educacion) if educacion else 0
        base = 950 + (edu_val * 400) + (exp * 80)
        rango_min = int(base * 0.85)
        rango_max = int(base * 1.15)
        return Div(
            Div(
                P("Ingreso mensual estimado", cls="res-label"),
                P(f"S/ {rango_min:,} — S/ {rango_max:,}", cls="res-value"),
                cls="res-main"
            ),
            P("⚠️ Estimación preliminar · El modelo real se conectará a Google Colab.", cls="res-note"),
            cls="resultado-content"
        )
    except:
        return P("Completa todos los campos para obtener tu estimación.", cls="res-error")

serve()