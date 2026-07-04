from fasthtml.common import *
from dotenv import load_dotenv
import os
from predictor import predecir_ingreso_real

load_dotenv()
app, rt = fast_app(pico=False, secret_key=os.environ.get("SESSION_SECRET", "mi_secreto_seguro_urp_2026"))

def navbar(is_transparent=True):
    navbar_cls = "navbar-fixed-element" if is_transparent else "navbar-fixed-element scrolled"
    return Header(
        Div(
            Div(
                Div(
                    I(cls="fa-solid fa-landmark"),
                    Span("Proyecto de Investigación Académica · Universidad Ricardo Palma"),
                    cls="gov-header-inner"
                ),
                cls="gov-header-band"
            ),
            Div(
                Div(
                    A(
                        Img(src="/static/imagenes/logo.png", alt="Logo MlingresoPeru", cls="navbar-logo"),
                        href="/#inicio", cls="logo-link"
                    ),
                    Img(src="/static/imagenes/etiqueta.png", alt="Aval Académico", cls="navbar-badge-img"),
                    Div(
                        Div(
                            Span("Mi", cls="brand-accent"),
                            Span("ingreso", cls="brand-main"),
                            Span("Peru", cls="brand-country"),
                            cls="brand-logo-text"
                        ),
                        cls="brand-logo-group"
                    ),
                    cls="brand-group"
                ),
                Button(I(cls="fa-solid fa-bars"), cls="menu-hamburguesa", onclick="toggleMenuMobile()"),
                Nav(
                    A(I(cls="fa-solid fa-house"), "Inicio", href="/#inicio", cls="menu-link"),
                    A(I(cls="fa-solid fa-gears"), "Cómo funciona", href="/#como-funciona", cls="menu-link"),
                    A(I(cls="fa-solid fa-book-open"), "Sobre el Proyecto", href="/sobre-proyecto", cls="menu-link"),
                    A(I(cls="fa-solid fa-calculator"), "Predictor", href="/#predictor", cls="menu-link"),
                    A(I(cls="fa-solid fa-envelope"), "Contacto", href="/#contacto", cls="menu-link"),
                    cls="menu-nav-links"
                ),
                Div(
                    A(I(cls="fa-solid fa-house"), "Inicio", href="/#inicio", cls="menu-mobile-link", onclick="toggleMenuMobile()"),
                    A(I(cls="fa-solid fa-gears"), "Cómo funciona", href="/#como-funciona", cls="menu-mobile-link", onclick="toggleMenuMobile()"),
                    A(I(cls="fa-solid fa-book-open"), "Sobre el Proyecto", href="/sobre-proyecto", cls="menu-mobile-link", onclick="toggleMenuMobile()"),
                    A(I(cls="fa-solid fa-calculator"), "Predictor", href="/#predictor", cls="menu-mobile-link", onclick="toggleMenuMobile()"),
                    A(I(cls="fa-solid fa-envelope"), "Contacto", href="/#contacto", cls="menu-mobile-link", onclick="toggleMenuMobile()"),
                    id="menu-mobile-collapse",
                    cls="menu-mobile-collapse"
                ),
                cls="navbar-main-content"
            ),
            cls="navbar-container"
        ),
        cls=navbar_cls
    )

def hero():
    return Div(
        Section(
            Div(
                Div(
                    Div(
                        Img(src="/static/imagenes/slide1.jpg", alt="Slide 1", cls="slide-img"),
                        Div("Análisis EPEN 2025", cls="slide-caption"),
                        cls="slide active"
                    ),
                    Div(
                        Img(src="/static/imagenes/slide2.jpg", alt="Slide 2", cls="slide-img"),
                        Div("Algoritmos de Gradient Boosting", cls="slide-caption"),
                        cls="slide"
                    ),
                    Div(
                        Img(src="/static/imagenes/slide3.jpg", alt="Slide 3", cls="slide-img"),
                        Div("Investigación Académica URP", cls="slide-caption"),
                        cls="slide"
                    ),
                    Div(
                        Img(src="/static/imagenes/slide4.jpg", alt="Slide 4", cls="slide-img"),
                        Div("Campus URP", cls="slide-caption"),
                        cls="slide"
                    ),
                    cls="slides-wrapper"
                ),
                Button(I(cls="fa-solid fa-chevron-left"), cls="slider-btn prev"),
                Button(I(cls="fa-solid fa-chevron-right"), cls="slider-btn next"),
                Div(
                    Span(cls="dot active"),
                    Span(cls="dot"),
                    Span(cls="dot"),
                    Span(cls="dot"),
                    cls="slider-dots"
                ),
                cls="hero-slider"
            ),
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
                        cls="hero-buttons-wrapper desktop-only"
                    ),
                    cls="hero-content-overlay"
                ),
                cls="section-container hero-content-wrapper"
            ),
            id="inicio", cls="hero-section-fullwidth"
        ),
        Div(
            Div(
                I(cls="fa-solid fa-bullseye card-stat-icon"),
                Div(
                    Span("Precisión del Modelo", cls="card-stat-title"),
                    Span("87.4%", cls="card-stat-value"),
                    cls="card-stat-texts"
                ),
                cls="hero-stat-card card-accent-red reveal-on-scroll"
            ),
            Div(
                I(cls="fa-solid fa-database card-stat-icon"),
                Div(
                    Span("Registros EPEN", cls="card-stat-title"),
                    Span("Datasets INEI", cls="card-stat-value"),
                    cls="card-stat-texts"
                ),
                cls="hero-stat-card reveal-on-scroll"
            ),
            Div(
                I(cls="fa-solid fa-brain card-stat-icon"),
                Div(
                    Span("Algoritmo Predictor", cls="card-stat-title"),
                    Span("XGBoost", cls="card-stat-value"),
                    cls="card-stat-texts"
                ),
                cls="hero-stat-card reveal-on-scroll"
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
                            cls="step-card-element reveal-on-scroll"
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

def sobre_proyecto():
    integrantes = [
        "Chacón Uscamaita, Rodrigo Alessandro",
        "Carrasco Pariona, Jerzy Ramón",
        "Espinoza Mathey, Manuel Adriano Valentín",
        "Vega Dulanto, César Matías Enrique",
        "Jiménez Rodríguez, Carlos Alonzo"
    ]
    return Section(
        Div(
            Div(
                Div(I(cls="fa-solid fa-book-open"), " DOCUMENTACIÓN", cls="badge-about"),
                H2("La historia detrás de MiingresoPeru", cls="section-main-heading"),
                P(
                    "MiingresoPeru nació en las aulas de la Universidad Ricardo Palma como un proyecto académico "
                    "de la Facultad de Ingeniería. Nuestra misión fue desarrollar un estimador salarial interactivo, "
                    "capaz de acercar la ciencia de datos y los modelos predictivos al usuario común para orientar "
                    "de forma transparente sus expectativas laborales.",
                    cls="about-intro-text"
                ),
                
                Div(
                    Div(
                        Div(I(cls="fa-solid fa-database technical-col-icon color-red"), cls="about-icon-container"),
                        H3("1. Los Datos y el Origen", cls="about-col-title"),
                        P("La base de conocimiento de nuestro modelo se fundamenta en la Encuesta Permanente de Empleo Nacional (EPEN) provista por el INEI. Aplicamos un riguroso proceso de:", cls="about-col-desc"),
                        Ul(
                            Li("Limpieza de registros duplicados e inconsistencias."),
                            Li("Preprocesamiento y codificación de variables categóricas."),
                            Li("Filtrado de ingresos atípicos para evitar sesgos."),
                            cls="about-bullets"
                        ),
                        A(
                            I(cls="fa-solid fa-external-link-alt"), " Visitar Fuente de Datasets",
                            href="https://www.datosabiertos.gob.pe/search/field_topic/economía-y-finanzas-29?query=Encuesta+Permanente+de+Empleo+Nacional+%28EPEN%29+2025&sort_by=changed&sort_order=DESC", target="_blank", cls="btn-link-externo"
                        ),
                        cls="about-technical-column reveal-on-scroll"
                    ),
                    Div(
                        Div(I(cls="fa-brands fa-github technical-col-icon"), cls="about-icon-container"),
                        H3("2. Modelamiento y Desarrollo", cls="about-col-title"),
                        P("Entrenamos un modelo supervisado usando el algoritmo XGBoost (eXtreme Gradient Boosting) en entornos de Google Colab. El flujo técnico incluyó:", cls="about-col-desc"),
                        Ul(
                            Li("Ajuste de hiperparámetros y validación cruzada."),
                            Li("Optimización del error cuadrático medio (RMSE)."),
                            Li("Exportación del modelo serializado y despliegue rápido."),
                            cls="about-bullets"
                        ),
                        A(
                            I(cls="fa-solid fa-external-link-alt"), " Ver Repositorio GitHub",
                            href="https://github.com/TailerRC/MiingresoPeru", target="_blank", cls="btn-link-externo"
                        ),
                        cls="about-technical-column reveal-on-scroll"
                    ),
                    cls="about-columns-grid"
                ),
                
                Div(
                    Div(
                        I(cls="fa-solid fa-users-gear authors-icon"),
                        H3("Quiénes lo hicimos posible (Desarrollo y Autoría)"),
                        cls="about-authors-header"
                    ),
                    P("Este proyecto es el resultado del trabajo en equipo y dedicación de los siguientes integrantes:", cls="about-authors-desc"),
                    Ul(
                        *[Li(I(cls="fa-solid fa-circle-check bullet-author-icon"), integrante) for integrante in integrantes],
                        cls="about-authors-list"
                    ),
                    cls="about-authors-block reveal-on-scroll"
                ),
                
                cls="section-inner-wrapper"
            ),
            cls="section-container"
        ),
        id="sobre-proyecto", cls="sobre-proyecto"
    )

def predictor():
    return Section(
        Div(
            Div(
                Span(I(cls="fa-solid fa-calculator"), " PROYECCIÓN SALARIAL", cls="section-eyebrow"),
                H2("Calculadora de Ingreso Estimado", cls="section-main-heading"),
                Div(
                    I(cls="fa-solid fa-triangle-exclamation warning-icon"),
                    P("Este predictor utiliza un modelo de Machine Learning (XGBoost) entrenado con datos reales del preprocesamiento EPEN del INEI. Las estimaciones son proyecciones estadísticas con fines académicos y no representan una garantía de ingreso real.", cls="warning-text"),
                    cls="warning-banner-container"
                ),
                
                Div(
                    Div(
                        Form(
                            Div(
                                Div(
                                    Label(I(cls="fa-solid fa-graduation-cap label-icon"), " Nivel Educativo", For="c366"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Secundaria incompleta", value="5"),
                                        Option("Secundaria completa", value="6"),
                                        Option("Sup. no universitaria incompleta", value="8"),
                                        Option("Sup. no universitaria completa", value="9"),
                                        Option("Sup. universitaria incompleta", value="10"),
                                        Option("Sup. universitaria completa", value="11"),
                                        Option("Maestría/Doctorado", value="12"),
                                        id="c366", name="c366", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                Div(
                                    Label(I(cls="fa-solid fa-cake-candles label-icon"), " ¿Cuántos años tienes?", For="c208"),
                                    Input(type="number", id="c208", name="c208", placeholder="Ej: 25", min="18", max="100", required=True),
                                    cls="form-group-field"
                                ),
                                Div(
                                    Label(I(cls="fa-solid fa-venus-mars label-icon"), " Sexo", For="c207"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Hombre", value="1"),
                                        Option("Mujer", value="2"),
                                        id="c207", name="c207", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                Div(
                                    Label(I(cls="fa-solid fa-earth-americas label-icon"), " ¿En qué región buscas trabajo?", For="region"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Lima Metropolitana", value="1"),
                                        Option("Resto urbano", value="2"),
                                        Option("Rural", value="3"),
                                        id="region", name="region", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                Div(
                                    Label(I(cls="fa-solid fa-network-wired label-icon"), " Tipo de trabajo al que aspiras", For="c310"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Empleador o patrono", value="1"),
                                        Option("Trabajador independiente", value="2"),
                                        Option("Empleado u obrero", value="3"),
                                        id="c310", name="c310", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                Div(
                                    Label(I(cls="fa-solid fa-users label-icon"), " Tamaño de empresa esperado", For="c317"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Hasta 20 personas", value="1"),
                                        Option("Más de 500 personas", value="5"),
                                        id="c317", name="c317", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                Div(
                                    Label(I(cls="fa-solid fa-building-shield label-icon"), " ¿Buscas negocio/empleo formal?", For="c312"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Sí, formal (Persona jurídica)", value="1"),
                                        Option("Persona natural con RUC", value="2"),
                                        Option("Prefiero informal (Sin RUC)", value="3"),
                                        id="c312", name="c312", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                Div(
                                    Label(I(cls="fa-solid fa-hand-holding-heart label-icon"), " Seguro de salud esperado", For="seguro1"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("EsSalud", value="1"),
                                        Option("Ambos", value="3"),
                                        Option("SIS", value="5"),
                                        id="seguro1", name="seguro1", required=True
                                    ),
                                    cls="form-group-field"
                                ),
                                Div(
                                    Label(I(cls="fa-solid fa-hourglass-half label-icon"), " ¿Horas semanales planeadas?", For="whoraT"),
                                    Input(type="number", id="whoraT", name="whoraT", placeholder="Ej: 48", min="1", max="48", required=True),
                                    cls="form-group-field"
                                ),
                                Div(
                                    Label(I(cls="fa-solid fa-money-check-dollar label-icon"), " Frecuencia de pago esperada", For="c338"),
                                    Select(
                                        Option("Selecciona...", value="", disabled=True, selected=True),
                                        Option("Semanal", value="2"),
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
                            hx_indicator="#carga-spinner",
                            cls="predictor-form-block"
                        ),
                        cls="predictor-form-column"
                    ),
                    Div(
                        Div(
                            Div(
                                Div(cls="spinner-ring"),
                                P("Calculando estimación...", cls="spinner-label"),
                                id="carga-spinner",
                                cls="htmx-indicator resultado-spinner-wrap"
                            ),
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
                    cls="predictor-grid-layout reveal-on-scroll"
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
                Div(
                    Div(
                        Span("Mi", cls="footer-brand-accent"),
                        Span("ingreso", cls="footer-brand-main"),
                        Span("Peru", cls="footer-brand-country"),
                        cls="footer-brand-title"
                    ),
                    P(
                        "MiingresoPeru es un estimador interactivo de ingresos mensuales en soles, "
                        "desarrollado por estudiantes de la Universidad Ricardo Palma con fines académicos "
                        "y de investigación. Los resultados son referenciales y no constituyen una oferta "
                        "laboral ni un dato oficial.",
                        cls="footer-brand-desc"
                    ),
                    cls="footer-col-about"
                ),
                Div(
                    H4("Fuente de Datos", cls="footer-section-title"),
                    P(
                        "Las estimaciones se basan en datos de la Encuesta Permanente de Empleo "
                        "Nacional (EPEN) del INEI.",
                        cls="footer-brand-desc"
                    ),
                    A(
                        I(cls="fa-solid fa-external-link-alt"), " Visitar Fuente de Datasets",
                        href="https://www.datosabiertos.gob.pe/search/field_topic/economía-y-finanzas-29?query=Encuesta+Permanente+de+Empleo+Nacional+%28EPEN%29+2025&sort_by=changed&sort_order=DESC", target="_blank", cls="footer-link-item"
                    ),
                    cls="footer-col-tech"
                ),
                cls="footer-top-grid"
            ),
            Div(
                P("© 2026 MiingresoPeru — Universidad Ricardo Palma. Proyecto académico sin fines comerciales.", cls="copyright-text"),
                cls="footer-bottom-bar"
            ),
            cls="section-container"
        ),
        id="contacto", cls="footer-section"
    )

@rt('/sobre-proyecto')
def get_sobre_proyecto():
    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Title("Sobre el Proyecto — MiingresoPeru"),
            Meta(name="description", content="Documentación académica, origen de datos del INEI y modelo predictivo XGBoost del proyecto MiingresoPeru de la Universidad Ricardo Palma."),
            Link(rel="icon", href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🇵🇪</text></svg>"),
            Link(rel="stylesheet", href="/static/fontawesome/css/all.min.css"),
            Link(rel="preconnect", href="https://fonts.googleapis.com"),
            Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
            Link(
                rel="stylesheet",
                href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap"
            ),
            Link(rel="stylesheet", href="/static/css/style.css"),
            Script(src="https://unpkg.com/htmx.org@1.9.12")
        ),
        Body(
            navbar(is_transparent=False),
            Div(cls="navbar-spacer"),
            sobre_proyecto(),
            contacto(),
            Script("""
                function toggleMenuMobile() {
                    const menu = document.getElementById('menu-mobile-collapse');
                    if (menu) {
                        menu.classList.toggle('active');
                    }
                }

                // Efecto navbar compacto al scrollear
                window.addEventListener('scroll', () => {
                    const navbar = document.querySelector('.navbar-fixed-element');
                    if (window.scrollY > 50) {
                        navbar.classList.add('scrolled');
                    }
                });

                // Intersection Observer para revelar elementos con scroll (se reactivan al volver)
                const revealElements = document.querySelectorAll('.reveal-on-scroll');
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('reveal-active');
                        } else {
                            entry.target.classList.remove('reveal-active');
                        }
                    });
                }, { threshold: 0.1 });

                revealElements.forEach(el => observer.observe(el));
            """)
        )
    )

@rt('/')
def get():
    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Title("MiingresoPeru — Estimador Salarial con Inteligencia Artificial"),
            Meta(name="description", content="Proyecta tu ingreso mensual esperado en Soles utilizando modelos de Inteligencia Artificial entrenados con datos oficiales de la EPEN del INEI. Proyecto académico de la URP."),
            Meta(name="keywords", content="miingreso, peru, salarios inei, epen inei, inteligencia artificial peru, estimador salarial, urp"),
            Link(rel="icon", href="static/imagenes/logo.png"),
            Link(rel="stylesheet", href="/static/fontawesome/css/all.min.css"),
            Link(rel="preconnect", href="https://fonts.googleapis.com"),
            Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
            Link(
                rel="stylesheet",
                href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap"
            ),
            Link(rel="stylesheet", href="/static/css/style.css"),
            Script(src="https://unpkg.com/htmx.org@1.9.12")
        ),
        Body(
            navbar(is_transparent=True),
            hero(),
            como_funciona(),
            predictor(),
            contacto(),
            Script("""
                function toggleMenuMobile() {
                    const menu = document.getElementById('menu-mobile-collapse');
                    if (menu) {
                        menu.classList.toggle('active');
                    }
                }

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

                // Intersection Observer para revelar elementos con scroll (se reactivan al volver)
                const revealElements = document.querySelectorAll('.hero-stat-card, .step-card-element, .predictor-grid-layout, .reveal-on-scroll');
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('reveal-active');
                        } else {
                            entry.target.classList.remove('reveal-active');
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
    Recibe los inputs del formulario predictor, ejecuta el modelo XGBoost
    entrenado con datos del EPEN (INEI) y retorna la tarjeta de resultados
    inyectada dinámicamente vía HTMX.
    """
    try:
        form_data = await request.form()
        datos_recibidos = {k: v for k, v in form_data.items()}
        required_fields = ['c366', 'c208', 'c207', 'region', 'c310', 'c317', 'c312', 'seguro1', 'whoraT', 'c338']
        for field in required_fields:
            if not datos_recibidos.get(field):
                return Div(
                    I(cls="fa-solid fa-triangle-exclamation err-icon"),
                    P("Por favor, selecciona una opción válida para todos los campos requeridos.", cls="err-message"),
                    cls="result-error-container"
                )
        edad = int(datos_recibidos.get('c208', 0))
        if edad < 18:
            return Div(
                I(cls="fa-solid fa-triangle-exclamation err-icon"),
                P("La edad mínima para trabajar legalmente en Perú es 18 años.", cls="err-message"),
                cls="result-error-container"
            )
        horas = int(datos_recibidos.get('whoraT', 0))
        if horas < 1 or horas > 48:
            return Div(
                I(cls="fa-solid fa-triangle-exclamation err-icon"),
                P("Las horas semanales deben estar entre 1 y 48 (límite legal en Perú).", cls="err-message"),
                cls="result-error-container"
            )
        res = predecir_ingreso_real(datos_recibidos)
        badge_cls = "formalidad-badge badge-formal" if res['es_formal'] else "formalidad-badge badge-informal"
        badge_icon = "fa-solid fa-circle-check" if res['es_formal'] else "fa-solid fa-circle-xmark"

        percentil_n = res['percentil_numero']
        if percentil_n >= 75:
            percentil_color = "#10B981"   # verde esmeralda
        elif percentil_n >= 55:
            percentil_color = "#F59E0B"   # ámbar
        else:
            percentil_color = "#EF4444"   # rojo suave

        return Div(
            Div(
                Div(
                    Div(
                        Div(
                            I(cls="fa-solid fa-money-bill-trend-up"),
                            cls="success-icon-ring"
                        ),
                        Div(
                            H3("Estimación Salarial Generada", cls="success-card-title"),
                            P("Predicción generada por modelo XGBoost entrenado con datos EPEN del INEI", cls="success-card-subtitle"),
                        ),
                        cls="success-card-title-group"
                    ),
                    cls="success-card-header"
                ),

                Div(
                    Span("INGRESO MENSUAL ESTIMADO", cls="ingreso-sub-label"),
                    Div(
                        Span("S/", cls="ingreso-currency"),
                        Span(f"{res['ingreso_estimado']:,.2f}", cls="ingreso-value-text"),
                        cls="ingreso-display-group"
                    ),
                    Div(
                        I(cls=badge_icon),
                        Span(res['nivel_formalidad'], cls="badge-label"),
                        cls=badge_cls
                    ),
                    cls="ingreso-display-container"
                ),

                Div(
                    Div(
                        Div(
                            Div(
                                I(cls="fa-solid fa-shield-heart metric-icon"),
                                cls="metric-icon-wrapper"
                            ),
                            Div(
                                Span("Confianza del Modelo", cls="metric-meta-label"),
                                Div(
                                    Span(res['confianza_score'], cls="metric-meta-value"),
                                    cls="metric-meta-header"
                                ),
                                Div(
                                    Div(
                                        cls="progress-meter-bar-fill",
                                        style=f"width: {res['confianza_score']}; background: linear-gradient(90deg, #10B981, #059669);"
                                    ),
                                    cls="progress-meter-bar-track"
                                ),
                                cls="metric-text-group"
                            ),
                            cls="metric-meta-card-inner"
                        ),
                        cls="metric-meta-card"
                    ),
                    Div(
                        Div(
                            Div(
                                I(cls="fa-solid fa-award metric-icon"),
                                cls="metric-icon-wrapper"
                            ),
                            Div(
                                Span("Percentil de Mercado", cls="metric-meta-label"),
                                Div(
                                    Span(res['percentil_mercado'], cls="metric-meta-value"),
                                    cls="metric-meta-header"
                                ),
                                Div(
                                    Div(
                                        cls="progress-meter-bar-fill percentil-bar",
                                        style=f"width: {percentil_n}%; background: linear-gradient(90deg, {percentil_color}, {percentil_color}cc);"
                                    ),
                                    cls="progress-meter-bar-track"
                                ),
                                cls="metric-text-group"
                            ),
                            cls="metric-meta-card-inner"
                        ),
                        cls="metric-meta-card"
                    ),
                    Div(
                        Div(
                            Div(
                                I(cls="fa-solid fa-building-shield metric-icon"),
                                cls="metric-icon-wrapper metric-icon-gold"
                            ),
                            Div(
                                Span("Régimen Laboral", cls="metric-meta-label"),
                                Div(
                                    Span(res['nivel_formalidad'], cls="metric-meta-value-text"),
                                    cls="metric-meta-header"
                                ),
                                cls="metric-text-group"
                            ),
                            cls="metric-meta-card-inner"
                        ),
                        cls="metric-meta-card"
                    ),
                    cls="metrics-dashboard-grid"
                ),
                Div(
                    I(cls="fa-solid fa-graduation-cap URP-badge-icon"),
                    P("Proyecto de Inteligencia Artificial — Universidad Ricardo Palma (Facultad de Ingeniería)", cls="academic-reference-text"),
                    cls="success-card-footer"
                ),
                cls="resultado-card-wrap animate-fade-in"
            )
        )

    except Exception as e:
        return Div(
            I(cls="fa-solid fa-circle-xmark err-icon"),
            P(f"Ha ocurrido un error inesperado al procesar tu solicitud: {str(e)}", cls="err-message"),
            cls="result-error-container"
        )

# Ejecución del servidor FastHTML
if __name__ == "__main__":
    serve()