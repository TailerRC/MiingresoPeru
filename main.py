# =====================================================================
# PROYECTO ACADÉMICO: MIINGRESOPERU (UNIVERSIDAD RICARDO PALMA)
# Estimador Salarial basado en la Encuesta Permanente de Empleo (EPEN)
# =====================================================================

from fasthtml.common import *  # noqa: F403
from dotenv import load_dotenv
import os

load_dotenv()

# Inicialización de FastHTML - pico=False previene conflictos con nuestros estilos custom.css
app, rt = fast_app(pico=False, secret_key=os.environ.get("SESSION_SECRET", "mi_secreto_seguro_urp_2026"))

# =====================================================================
# 1. DATOS MOCKUP (Mocking) - LÓGICA DE SIMULACIÓN IA
# =====================================================================
def simular_modelo_ia_epen(datos_recibidos: dict) -> dict:
    """
    Simula la predicción del modelo de Machine Learning entrenado con el EPEN (INEI).
    Calcula un ingreso mensual estimado realista a partir de los inputs recibidos
    y devuelve un diccionario estructurado.
    """
    try:
        c366 = int(datos_recibidos.get('c366', 6))  # Nivel educativo (default: Sec. Completa)
    except ValueError:
        c366 = 6

    try:
        c208 = int(datos_recibidos.get('c208', 30))  # Edad (default: 30)
    except ValueError:
        c208 = 30

    c207 = datos_recibidos.get('c207', '1')        # Sexo (1 = Hombre, 2 = Mujer)
    region = datos_recibidos.get('region', '1')      # Región (1 = Lima Metropolitana, 2 = Resto Urbano, 3 = Rural)
    c310 = datos_recibidos.get('c310', '3')        # Tipo de trabajo (default: Empleado/obrero)
    c317 = datos_recibidos.get('c317', '1')        # Tamaño de empresa (default: Hasta 20 personas)
    c312 = datos_recibidos.get('c312', '1')        # Formalidad buscada (default: Sí, formal PJ)
    seguro1 = datos_recibidos.get('seguro1', '5')    # Seguro de salud (default: SIS)
    
    try:
        whoraT = int(datos_recibidos.get('whoraT', 40))  # Horas semanales (default: 40)
    except ValueError:
        whoraT = 40

    c338 = datos_recibidos.get('c338', '4')        # Frecuencia de pago (default: Mensual)

    # Lógica de estimación basada en factores de mercado peruano reales
    # Salario Mínimo Vital base aproximado: S/ 1025
    base = 1025.0

    # 1. Multiplicador de Nivel Educativo (c366)
    educ_multipliers = {
        1: 0.0,    # Sin nivel
        2: 0.05,   # Educación Inicial
        3: 0.10,   # Primaria incompleta
        4: 0.20,   # Primaria completa
        5: 0.35,   # Secundaria incompleta
        6: 0.65,   # Secundaria completa
        7: 0.50,   # Básica especial
        8: 1.00,   # Sup. no univ. incompleta
        9: 1.40,   # Sup. no univ. completa
        10: 1.70,  # Sup. univ. incompleta
        11: 2.60,  # Sup. univ. completa
        12: 4.20   # Maestría/Doctorado
    }
    base += base * educ_multipliers.get(c366, 0.65)

    # 2. Factor de Experiencia / Edad (c208)
    # Pico de ingresos en el mercado peruano ronda los 35-50 años.
    if c208 < 18:
        base = base * 0.75
    elif c208 > 65:
        base = base * 0.85
    else:
        # Incremento sutil por madurez laboral
        base += (c208 - 18) * 35.0

    # 3. Factor de Región (region)
    region_mods = {
        '1': 700.0,   # Lima Metropolitana
        '2': 250.0,   # Resto urbano
        '3': -200.0   # Rural
    }
    base += region_mods.get(region, 250.0)

    # 4. Tipo de Trabajo (c310)
    job_mods = {
        '1': 1200.0,  # Empleador o patrono
        '2': 150.0,   # Trabajador independiente
        '3': 450.0,   # Empleado u obrero
        '6': -250.0,  # Trabajador del hogar
        '7': -150.0   # Aprendiz/practicante
    }
    base += job_mods.get(c310, 450.0)

    # 5. Tamaño de Empresa (c317)
    company_mods = {
        '1': 0.0,      # Hasta 20 personas
        '2': 350.0,    # De 21 a 50 personas
        '3': 700.0,    # De 51 a 100 personas
        '4': 1100.0,   # De 101 a 500 personas
        '5': 1900.0    # Más de 500 personas
    }
    base += company_mods.get(c317, 0.0)

    # 6. Seguro de Salud (seguro1)
    insurance_mods = {
        '1': 300.0,   # EsSalud (formalidad típica)
        '2': 600.0,   # Seguro privado (ingresos altos)
        '3': 700.0,   # Ambos
        '4': 0.0,     # Otro
        '5': -100.0,  # SIS
        '6': -150.0   # No está afiliado
    }
    base += insurance_mods.get(seguro1, 0.0)

    # 7. Horas de Trabajo (whoraT) normalizado a la jornada estándar de 48 horas
    hours_ratio = min(max(whoraT / 48.0, 0.25), 1.75)
    base = base * hours_ratio

    # 8. Formalidad (c312)
    if c312 == '1':
        base += 500.0  # Persona Jurídica
    elif c312 == '2':
        base += 250.0  # Persona Natural RUC
    elif c312 == '3':
        base -= 250.0  # Informal

    # Salario estimado redondeado y acotado al rango realista
    salario_final = round(max(base, 1025.0), 2)

    # Nivel de formalidad descriptivo
    formalidad_map = {
        '1': 'Formal (Empresa Registrada)',
        '2': 'Formal (Persona Natural con RUC)',
        '3': 'Informal (Sin RUC)',
        '4': 'Informal (No especificado / No sabe)'
    }
    nivel_formalidad = formalidad_map.get(c312, 'Formal (Empresa Registrada)')

    # Percentil del mercado según el salario estimado
    if salario_final < 1400.0:
        percentil_mercado = 'Percentil 30 (Ingreso Básico)'
    elif salario_final < 2800.0:
        percentil_mercado = 'Percentil 55 (Ingreso Promedio)'
    elif salario_final < 5000.0:
        percentil_mercado = 'Top 25% superior'
    else:
        percentil_mercado = 'Top 10% de altos ingresos'

    # Confianza del score simulada (estable pero cambia ligeramente con los inputs)
    factor_hash = (c366 * 3 + c208 + int(c207) * 7 + int(region) * 11) % 15
    confianza_val = 84.0 + (factor_hash * 0.9)
    confianza_score = f"{round(confianza_val, 1)}%"

    return {
        'ingreso_estimado': salario_final,
        'confianza_score': confianza_score,
        'nivel_formalidad': nivel_formalidad,
        'percentil_mercado': percentil_mercado
    }

# =====================================================================
# 2. VISTAS DEL COMPONENTE FRONTEND SPA
# =====================================================================

def navbar():
    return Header(
        Div(
            # Banda institucional gubernamental sutil estilo gob.pe
            Div(
                Div(
                    I(cls="fa-solid fa-landmark"),
                    Span("Proyecto de Investigación Académica · Universidad Ricardo Palma"),
                    cls="gov-header-inner"
                ),
                cls="gov-header-band"
            ),
            # Navbar Principal
            Div(
                Div(
                    A(
                        Img(src="/static/imagenes/logo.png", alt="Logo MlingresoPeru", cls="navbar-logo"),
                        href="#inicio", cls="logo-link"
                    ),
                    Div(
                        Div(
                            Span("MI", cls="brand-accent"),
                            Span("ingreso", cls="brand-main"),
                            Span("Peru", cls="brand-country"),
                            cls="brand-logo-text"
                        ),
                        cls="brand-logo-group"
                    ),
                    Img(src="/static/imagenes/etiqueta.png", alt="Aval Académico", cls="navbar-badge-img"),
                    cls="brand-group"
                ),
                Nav(
                    A(I(cls="fa-solid fa-house"), "Inicio", href="#inicio", cls="menu-link"),
                    A(I(cls="fa-solid fa-gears"), "Cómo funciona", href="#como-funciona", cls="menu-link"),
                    A(I(cls="fa-solid fa-calculator"), "Predictor", href="#predictor", cls="menu-link"),
                    A(I(cls="fa-solid fa-envelope"), "Contacto", href="#contacto", cls="menu-link"),
                    cls="menu-nav-links"
                ),
                cls="navbar-main-content"
            ),
            cls="navbar-container"
        ),
        cls="navbar-fixed-element"
    )

def hero():
    return Div(
        Section(
            # 1. Slider de Fondo (Ancho y Alto Completo)
            Div(
                # Contenedor de slides
                Div(
                    # Slide 1
                    Div(
                        Img(src="/static/imagenes/slide1.jpg", alt="Slide 1", cls="slide-img"),
                        Div("Análisis EPEN 2025", cls="slide-caption"),
                        cls="slide active"
                    ),
                    # Slide 2
                    Div(
                        Img(src="/static/imagenes/slide2.jpg", alt="Slide 2", cls="slide-img"),
                        Div("Algoritmos de Gradient Boosting", cls="slide-caption"),
                        cls="slide"
                    ),
                    # Slide 3
                    Div(
                        Img(src="/static/imagenes/slide3.jpg", alt="Slide 3", cls="slide-img"),
                        Div("Investigación Académica URP", cls="slide-caption"),
                        cls="slide"
                    ),
                    # Slide 4
                    Div(
                        Img(src="/static/imagenes/slide4.jpg", alt="Slide 4", cls="slide-img"),
                        Div("Campus URP", cls="slide-caption"),
                        cls="slide"
                    ),
                    cls="slides-wrapper"
                ),
                # Controles de navegación
                Button(I(cls="fa-solid fa-chevron-left"), cls="slider-btn prev"),
                Button(I(cls="fa-solid fa-chevron-right"), cls="slider-btn next"),
                # Puntos indicadores
                Div(
                    Span(cls="dot active"),
                    Span(cls="dot"),
                    Span(cls="dot"),
                    Span(cls="dot"),
                    cls="slider-dots"
                ),
                cls="hero-slider"
            ),
            # 2. Capa de Contenido Superpuesto (Texto y Botones a la izquierda)
            Div(
                Div(
                    Span( "", cls="hero-overlay-eyebrow"),
                    H1(
                        "Estima tu ",
                        Span("ingreso mensual", cls="red-gradient-text"),
                        " en el mercado laboral peruano"
                    ),
                    P(
                        "Utiliza nuestro algoritmo predictor entrenado con los datos de la Encuesta "
                        "Permanente de Empleo Nacional (EPEN) del INEI para proyectar tus metas salariales.",
                        cls="hero-overlay-desc"
                    ),
                    Div(
                        A(I(cls="fa-solid fa-calculator"), "Calcular Salario", href="#predictor", cls="btn-cta-primary"),
                        A(I(cls="fa-solid fa-circle-question"), "Ver Metodología", href="#como-funciona", cls="btn-cta-ghost"),
                        cls="hero-buttons-wrapper"
                    ),
                    # Badges académicos e institucionales
                    Div(
                        Span(I(cls="fa-solid fa-circle-check"), "Datos de EPEN INEI", cls="hero-badge-item"),
                        Span(I(cls="fa-solid fa-university"), "Investigación URP", cls="hero-badge-item"),
                        cls="hero-badges-container"
                    ),
                    cls="hero-content-overlay"
                ),
                cls="section-container hero-content-wrapper"
            ),
            id="inicio", cls="hero-section-fullwidth"
        ),
        # 3. Fila de Métricas Estadísticas (Flota sobre la base del hero)
        Div(
            # Tarjeta 1: Precisión
            Div(
                I(cls="fa-solid fa-bullseye card-stat-icon"),
                Div(
                    Span("Precisión del Modelo", cls="card-stat-title"),
                    Span("87.4%", cls="card-stat-value"),
                    cls="card-stat-texts"
                ),
                cls="hero-stat-card card-accent-red"
            ),
            # Tarjeta 2: Tamaño Dataset
            Div(
                I(cls="fa-solid fa-database card-stat-icon"),
                Div(
                    Span("Registros EPEN", cls="card-stat-title"),
                    Span("120K+ Muestras", cls="card-stat-value"),
                    cls="card-stat-texts"
                ),
                cls="hero-stat-card"
            ),
            # Tarjeta 3: Algoritmo
            Div(
                I(cls="fa-solid fa-brain card-stat-icon"),
                Div(
                    Span("Algoritmo Predictor", cls="card-stat-title"),
                    Span("Gradient Boosting", cls="card-stat-value"),
                    cls="card-stat-texts"
                ),
                cls="hero-stat-card"
            ),
            cls="hero-bottom-stats-row"
        ),
        cls="hero-wrapper-container"
    )

def como_funciona():
    pasos = [
        ("fa-solid fa-clipboard-list", "1. Registrar tus Datos", "Ingresa variables demográficas y laborales como educación, región, edad y horas semanales esperadas."),
        ("fa-solid fa-chart-line", "2. Procesamiento de IA", "El modelo de predicción calcula tu perfil contra el histórico ponderado de la encuesta nacional EPEN del INEI."),
        ("fa-solid fa-chart-pie", "3. Análisis de Resultados", "Obtén la estimación salarial exacta en Soles, confianza del cálculo, nivel de formalidad y tu posición en el percentil del mercado.")
    ]
    return Section(
        Div(
            Div(
                Span(I(cls="fa-solid fa-gears"), " METODOLOGÍA", cls="section-eyebrow"),
                H2("¿Cómo se estima tu ingreso mensual?", cls="section-main-heading"),
                P("Nuestro sistema procesa tus inputs a través de un pipeline estructurado en 3 pasos clave:", cls="section-sub-heading"),
                
                Div(
                    *[
                        Div(
                            Div(
                                Div(I(cls=icono), cls="step-card-icon-container"),
                                cls="step-card-header"
                            ),
                            H3(titulo, cls="step-card-title"),
                            P(descripcion, cls="step-card-desc"),
                            cls="step-card-element"
                        )
                        for icono, titulo, descripcion in pasos
                    ],
                    cls="steps-horizontal-grid"
                ),
                cls="section-inner-wrapper"
            ),
            cls="section-container"
        ),
        id="como-funciona", cls="section-grey-background"
    )

def predictor():
    return Section(
        Div(
            Div(
                Span(I(cls="fa-solid fa-calculator"), " PROYECCIÓN SALARIAL", cls="section-eyebrow"),
                H2("Calculadora de Ingreso Estimado", cls="section-main-heading"),
                
                # Panel informativo
                Div(
                    I(cls="fa-solid fa-triangle-exclamation warning-icon"),
                    P("El modelo actual utiliza datos del preprocesamiento EPEN del INEI. Las estimaciones son simuladas con fines académicos y de desarrollo de la interfaz de usuario.", cls="warning-text"),
                    cls="warning-banner-container"
                ),
                
                # Grid Side-by-Side (Lado a Lado)
                Div(
                    # Columna de Formulario
                    Div(
                        Form(
                            Div(
                                # 1. Nivel Educativo
                                Div(
                                    Label(I(cls="fa-solid fa-graduation-cap label-icon"), " Nivel Educativo (c366)", For="c366"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Sin nivel", value="1"),
                                        Option("Educación Inicial", value="2"),
                                        Option("Primaria incompleta", value="3"),
                                        Option("Primaria completa", value="4"),
                                        Option("Secundaria incompleta", value="5"),
                                        Option("Secundaria completa", value="6"),
                                        Option("Básica especial", value="7"),
                                        Option("Sup. no univ. incompleta", value="8"),
                                        Option("Sup. no univ. completa", value="9"),
                                        Option("Sup. univ. incompleta", value="10"),
                                        Option("Sup. univ. completa", value="11"),
                                        Option("Maestría/Doctorado", value="12"),
                                        id="c366", name="c366", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                # 2. Edad
                                Div(
                                    Label(I(cls="fa-solid fa-cake-candles label-icon"), " ¿Cuántos años tienes? (c208)", For="c208"),
                                    Input(type="number", id="c208", name="c208", placeholder="Ej: 25", min="14", max="100", required=True),
                                    cls="form-group-field"
                                ),
                                # 3. Sexo
                                Div(
                                    Label(I(cls="fa-solid fa-venus-mars label-icon"), " Sexo (c207)", For="c207"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Hombre", value="1"),
                                        Option("Mujer", value="2"),
                                        id="c207", name="c207", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                # 4. Región
                                Div(
                                    Label(I(cls="fa-solid fa-earth-americas label-icon"), " ¿En qué región buscas trabajo? (region)", For="region"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Lima Metropolitana", value="1"),
                                        Option("Resto urbano", value="2"),
                                        Option("Rural", value="3"),
                                        id="region", name="region", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                # 5. Tipo de trabajo
                                Div(
                                    Label(I(cls="fa-solid fa-network-wired label-icon"), " Tipo de trabajo al que aspiras (c310)", For="c310"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Empleador o patrono", value="1"),
                                        Option("Trabajador independiente", value="2"),
                                        Option("Empleado u obrero", value="3"),
                                        Option("Trabajador del hogar", value="6"),
                                        Option("Aprendiz/practicante remunerado", value="7"),
                                        id="c310", name="c310", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                # 6. Tamaño de empresa
                                Div(
                                    Label(I(cls="fa-solid fa-users label-icon"), " Tamaño de empresa esperado (c317)", For="c317"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Hasta 20 personas", value="1"),
                                        Option("De 21 a 50 personas", value="2"),
                                        Option("De 51 a 100 personas", value="3"),
                                        Option("De 101 a 500 personas", value="4"),
                                        Option("Más de 500 personas", value="5"),
                                        id="c317", name="c317", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                # 7. ¿Buscas negocio formal?
                                Div(
                                    Label(I(cls="fa-solid fa-building-shield label-icon"), " ¿Buscas negocio/empleo formal? (c312)", For="c312"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Sí, formal (Persona jurídica)", value="1"),
                                        Option("Persona natural con RUC", value="2"),
                                        Option("Prefiero informal (Sin RUC)", value="3"),
                                        Option("No sabe", value="4"),
                                        id="c312", name="c312", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                # 8. Seguro de salud
                                Div(
                                    Label(I(cls="fa-solid fa-hand-holding-heart label-icon"), " Seguro de salud esperado (seguro1)", For="seguro1"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("EsSalud", value="1"),
                                        Option("Seguro privado", value="2"),
                                        Option("Ambos", value="3"),
                                        Option("Otro", value="4"),
                                        Option("SIS", value="5"),
                                        Option("No está afiliado", value="6"),
                                        id="seguro1", name="seguro1", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                # 9. Horas semanales
                                Div(
                                    Label(I(cls="fa-solid fa-hourglass-half label-icon"), " ¿Horas semanales planeadas? (whoraT)", For="whoraT"),
                                    Input(type="number", id="whoraT", name="whoraT", placeholder="Ej: 48", min="1", max="120", required=True),
                                    cls="form-group-field"
                                ),
                                # 10. Frecuencia de pago
                                Div(
                                    Label(I(cls="fa-solid fa-money-check-dollar label-icon"), " Frecuencia de pago esperada (c338)", For="c338"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Diario", value="1"),
                                        Option("Semanal", value="2"),
                                        Option("Quincenal", value="3"),
                                        Option("Mensual", value="4"),
                                        id="c338", name="c338", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                cls="inputs-grid-layout"
                            ),
                            Button(
                                I(cls="fa-solid fa-wand-magic-sparkles submit-btn-icon"),
                                Span("Calcular Ingreso Estimado"),
                                type="submit",
                                cls="btn-predictor-submit btn-pulse"
                            ),
                            hx_post="/calcular-salario",
                            hx_target="#resultado-ia-target",
                            hx_swap="innerHTML",
                            cls="predictor-form-block"
                        ),
                        cls="predictor-form-column"
                    ),
                    # Columna de Resultados (Lado Derecho)
                    Div(
                        Div(
                            # Contenedor del placeholder inicial
                            Div(
                                I(cls="fa-solid fa-chart-line placeholder-result-icon"),
                                H3("Esperando Parámetros", cls="placeholder-result-title"),
                                P("Completa todos los campos del perfil laboral en el formulario de la izquierda y haz clic en calcular para proyectar tu salario estimado.", cls="placeholder-result-desc"),
                                cls="placeholder-result-wrapper"
                            ),
                            id="resultado-ia-target",
                            cls="result-box-interactive-panel"
                        ),
                        cls="predictor-result-column"
                    ),
                    cls="predictor-grid-layout"
                ),
                cls="section-inner-wrapper"
            ),
            cls="section-container"
        ),
        id="predictor", cls="section-white-background"
    )

def contacto():
    return Footer(
        Div(
            Div(
                # Información del proyecto
                Div(
                    Div(
                        Span("MI", cls="footer-brand-accent"),
                        Span("ingreso", cls="footer-brand-main"),
                        Span("Peru", cls="footer-brand-country"),
                        cls="footer-brand-title"
                    ),
                    P(
                        "MiingresoPeru es un estimador interactivo de ingresos mensuales en soles"
                        " desarrollado como proyecto de investigación por estudiantes de la Universidad Ricardo Palma, "
                        "utilizando machine learning entrenado sobre el EPEN del INEI.",
                        cls="footer-brand-desc"
                    ),
                    cls="footer-col-about"
                ),
                # Enlaces rápidos de navegación interna
                Div(
                    H4("Navegación SPA", cls="footer-section-title"),
                    Div(
                        A("Inicio", href="#inicio", cls="footer-link-item"),
                        A("Cómo Funciona", href="#como-funciona", cls="footer-link-item"),
                        A("Predictor IA", href="#predictor", cls="footer-link-item"),
                        cls="footer-links-grid"
                    ),
                    cls="footer-col-links"
                ),
                # Stack tecnológico
                Div(
                    H4("Stack Tecnológico", cls="footer-section-title"),
                    Div(
                        Span(I(cls="fa-brands fa-python"), " Python 3", cls="tech-badge"),
                        Span(I(cls="fa-solid fa-code"), " FastHTML", cls="tech-badge"),
                        Span(I(cls="fa-solid fa-bolt"), " HTMX", cls="tech-badge"),
                        Span(I(cls="fa-solid fa-gears"), " Machine Learning", cls="tech-badge"),
                        Span(I(cls="fa-solid fa-database"), " EPEN (INEI)", cls="tech-badge"),
                        cls="footer-tech-badges-grid"
                    ),
                    cls="footer-col-tech"
                ),
                cls="footer-top-grid"
            ),
            # Barra de copyright y créditos
            Div(
                P("© 2026 MiingresoPeru. Desarrollado con fines académicos y de investigación científica.", cls="copyright-text"),
                P("Curso: Inteligencia Artificial — URP", cls="course-text"),
                cls="footer-bottom-bar"
            ),
            cls="section-container"
        ),
        id="contacto", cls="footer-section"
    )

# =====================================================================
# 3. RUTAS PRINCIPALES DEL SISTEMA
# =====================================================================

@rt('/')
def get():
    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            # SEO y Metatags
            Title("MiingresoPeru — Estimador Salarial con Inteligencia Artificial"),
            Meta(name="description", content="Proyecta tu ingreso mensual esperado en Soles utilizando modelos de Inteligencia Artificial entrenados con datos oficiales de la EPEN del INEI. Proyecto académico de la URP."),
            Meta(name="keywords", content="miingreso, peru, salarios inei, epen inei, inteligencia artificial peru, estimador salarial, urp"),
            Link(rel="icon", href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🇵🇪</text></svg>"),
            # Hojas de estilo y fuentes
            Link(rel="stylesheet", href="/static/fontawesome/css/all.min.css"),
            Link(rel="preconnect", href="https://fonts.googleapis.com"),
            Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
            Link(
                rel="stylesheet",
                href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap"
            ),
            Link(rel="stylesheet", href="/static/css/style.css"),
            # IMPORTANTE: Cargamos HTMX explícitamente para garantizar la interactividad SPA sin reloads
            Script(src="https://unpkg.com/htmx.org@1.9.12")
        ),
        Body(
            navbar(),
            hero(),
            como_funciona(),
            predictor(),
            contacto(),
            # Scripts personalizados para interacciones SPA y micro-animaciones
            Script("""
                // Scroll suave personalizado
                document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                    anchor.addEventListener('click', function (e) {
                        e.preventDefault();
                        const targetId = this.getAttribute('href');
                        const targetEl = document.querySelector(targetId);
                        if (targetEl) {
                            const offset = 80; // Compensación por navbar fijo
                            const targetPosition = targetEl.getBoundingClientRect().top + window.scrollY - offset;
                            window.scrollTo({
                                top: targetPosition,
                                behavior: 'smooth'
                            });
                        }
                    });
                });

                // Efecto navbar compacto al scrollear
                window.addEventListener('scroll', () => {
                    const navbar = document.querySelector('.navbar-fixed-element');
                    if (window.scrollY > 50) {
                        navbar.classList.add('scrolled');
                    } else {
                        navbar.classList.remove('scrolled');
                    }
                });

                // Intersection Observer para revelar elementos con scroll
                const revealElements = document.querySelectorAll('.hero-stat-card, .step-card-element, .predictor-grid-layout');
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('reveal-active');
                        }
                    });
                }, { threshold: 0.1 });

                revealElements.forEach(el => observer.observe(el));

                // Lógica del Carrusel / Banner Rotativo (Fade suave)
                let currentSlideIndex = 0;
                const slides = document.querySelectorAll('.slide');
                const dots = document.querySelectorAll('.dot');

                function showSlide(index) {
                    if (slides.length === 0) return;
                    if (index >= slides.length) {
                        currentSlideIndex = 0;
                    } else if (index < 0) {
                        currentSlideIndex = slides.length - 1;
                    } else {
                        currentSlideIndex = index;
                    }
                    
                    slides.forEach((slide, i) => {
                        slide.classList.toggle('active', i === currentSlideIndex);
                    });
                    
                    dots.forEach((dot, i) => {
                        dot.classList.toggle('active', i === currentSlideIndex);
                    });
                }

                document.querySelector('.slider-btn.prev')?.addEventListener('click', () => {
                    showSlide(currentSlideIndex - 1);
                });

                document.querySelector('.slider-btn.next')?.addEventListener('click', () => {
                    showSlide(currentSlideIndex + 1);
                });

                dots.forEach((dot, index) => {
                    dot.addEventListener('click', () => {
                        showSlide(index);
                    });
                });

                // Rotación automática cada 5 segundos
                setInterval(() => {
                    showSlide(currentSlideIndex + 1);
                }, 5000);
            """)
        )
    )

@rt('/calcular-salario')
async def post(request):
    """
    Ruta del endpoint de estimación salarial.
    Recibe los inputs del formulario predictor, los simula con la lógica IA del EPEN
    y retorna la tarjeta de resultados inyectada dinámicamente vía HTMX.
    """
    try:
        # Recuperar datos del payload del formulario
        form_data = await request.form()
        datos_recibidos = {k: v for k, v in form_data.items()}
        
        # Validación de campos requeridos
        required_fields = ['c366', 'c208', 'c207', 'region', 'c310', 'c317', 'c312', 'seguro1', 'whoraT', 'c338']
        for field in required_fields:
            if not datos_recibidos.get(field):
                return Div(
                    I(cls="fa-solid fa-triangle-exclamation err-icon"),
                    P("Por favor, selecciona una opción válida para todos los campos requeridos.", cls="err-message"),
                    cls="result-error-container"
                )

        # Ejecutar modelo mockup EPEN
        res = simular_modelo_ia_epen(datos_recibidos)

        # Retornar el panel con los resultados procesados con alto nivel visual
        return Div(
            # Tarjeta de resultado
            Div(
                # Encabezado
                Div(
                    Div(
                        I(cls="fa-solid fa-circle-check success-badge-icon"),
                        Div(
                            H3("Estimación Salarial Generada", cls="success-card-title"),
                            P("Basado en el preprocesamiento de la encuesta EPEN del INEI", cls="success-card-subtitle"),
                        ),
                        cls="success-card-title-group"
                    ),
                    cls="success-card-header"
                ),
                
                # Ingreso Mensual Gigante
                Div(
                    Span("INGRESO MENSUAL ESTIMADO (INGTOT)", cls="ingreso-sub-label"),
                    Div(
                        Span("S/", cls="ingreso-currency"),
                        Span(f"{res['ingreso_estimado']:,.2f}", cls="ingreso-value-text"),
                        cls="ingreso-display-group"
                    ),
                    cls="ingreso-display-container"
                ),
                
                # Métricas adicionales
                Div(
                    # Métrica 1: Confianza del cálculo
                    Div(
                        Div(
                            Span(I(cls="fa-solid fa-gauge-high"), " Confianza del Score", cls="metric-meta-label"),
                            Span(res['confianza_score'], cls="metric-meta-value"),
                            cls="metric-meta-header"
                        ),
                        Div(
                            Div(cls="progress-meter-bar-fill", style=f"width: {res['confianza_score']}"),
                            cls="progress-meter-bar-track"
                        ),
                        cls="metric-meta-card"
                    ),
                    # Métrica 2: Nivel de Formalidad
                    Div(
                        Span(I(cls="fa-solid fa-building-circle-check"), " Formalidad Laboral", cls="metric-meta-label"),
                        Span(res['nivel_formalidad'], cls="metric-meta-value-text"),
                        cls="metric-meta-card"
                    ),
                    # Métrica 3: Percentil de mercado
                    Div(
                        Span(I(cls="fa-solid fa-chart-simple"), " Percentil de Mercado", cls="metric-meta-label"),
                        Span(res['percentil_mercado'], cls="metric-meta-value-text"),
                        cls="metric-meta-card"
                    ),
                    cls="metrics-dashboard-grid"
                ),
                
                # Footer de la tarjeta con aclaración del proyecto
                Div(
                    I(cls="fa-solid fa-graduation-cap URP-badge-icon"),
                    P("Proyecto de Inteligencia Artificial - Universidad Ricardo Palma (Facultad de Ingeniería)", cls="academic-reference-text"),
                    cls="success-card-footer"
                ),
                cls="resultado-card-wrap animate-fade-in"
            )
        )
    except Exception as e:
        # En caso de error inesperado
        return Div(
            I(cls="fa-solid fa-circle-xmark err-icon"),
            P(f"Ha ocurrido un error inesperado al procesar tu solicitud: {str(e)}", cls="err-message"),
            cls="result-error-container"
        )

# Ejecución del servidor FastHTML
serve()