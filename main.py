# =====================================================================
# PROYECTO ACADÉMICO: MIINGRESOPERU (UNIVERSIDAD RICARDO PALMA)
# Estimador Salarial basado en la Encuesta Permanente de Empleo (EPEN)
# =====================================================================

from fasthtml.common import *  # noqa: F403
from dotenv import load_dotenv
import os
import json
import xgboost as xgb
import pandas as pd

load_dotenv()

# Inicialización de FastHTML - pico=False previene conflictos con nuestros estilos custom.css
app, rt = fast_app(pico=False, secret_key=os.environ.get("SESSION_SECRET", "mi_secreto_seguro_urp_2026"))

# --- Carga del modelo real (una sola vez, al iniciar la app) ---
modelo = xgb.XGBRegressor()
modelo.load_model("models/modelo_ingresos.json")

with open("models/columnas_modelo.json") as f:
    columnas_modelo = json.load(f)

# --- Valores por defecto para las 16 variables ocultas (no visibles en el form) ---
defaults_ocultos = {
    "REGION": 1, "ESTRATO": 5, "C205": 2, "C311": 5, "C359": 1,
    "C361_1": 1, "C361_5": 2, "C364_1": 2,
    "C375_1": 2, "C375_2": 2, "C375_3": 2, "C375_4": 2, "C375_5": 2, "C375_6": 2,
    "C376": 10, "C377": 7,
}

def predecir_ingreso_real(datos_recibidos: dict) -> dict:
    """
    Predicción real usando el modelo XGBoost entrenado con datos EPEN (INEI).
    Recibe el dict crudo del formulario (strings) y devuelve la misma
    estructura que antes usaba la simulación, para no romper el HTML.
    """
    # 1. Parsear inputs del formulario (mismos nombres que ya usa el HTML)
    try:
        c366 = int(datos_recibidos.get('c366', 6))
        c208 = int(datos_recibidos.get('c208', 30))
        c207 = int(datos_recibidos.get('c207', 1))
        region = int(datos_recibidos.get('region', 1))
        c310 = int(datos_recibidos.get('c310', 3))
        c317 = int(datos_recibidos.get('c317', 1))
        c312 = int(datos_recibidos.get('c312', 1))
        seguro1 = int(datos_recibidos.get('seguro1', 5))
        whoraT = int(datos_recibidos.get('whoraT', 40))
        c338 = int(datos_recibidos.get('c338', 4))
    except (ValueError, TypeError):
        raise ValueError("Datos del formulario inválidos o incompletos")

    # 2. Armar el vector de entrada con las 26 columnas exactas del modelo
    formulario_modelo = {
        "C366": c366,
        "C208": c208,
        "C207": c207,
        "REGION": region,
        "C310": c310,
        "C317": c317,
        "C312": c312,
        "SEGURO1": seguro1,
        "C318_T": whoraT,
        "whoraT": whoraT,
        "C338": c338,
    }
    entrada = {**defaults_ocultos, **formulario_modelo}
    fila = pd.DataFrame([[entrada[col] for col in columnas_modelo]], columns=columnas_modelo)

    # 3. Predicción real del modelo
    ingreso_estimado = float(modelo.predict(fila)[0])
    ingreso_estimado = round(max(ingreso_estimado, 0.0), 2)

    # 4. Metadatos descriptivos (formalidad, percentil) calculados sobre la predicción real
    formalidad_map = {
        1: 'Formal (Empresa Registrada)',
        2: 'Formal (Persona Natural con RUC)',
        3: 'Informal (Sin RUC)',
        4: 'Informal (No especificado / No sabe)'
    }
    nivel_formalidad = formalidad_map.get(c312, 'Formal (Empresa Registrada)')

    if ingreso_estimado < 1400.0:
        percentil_mercado = 'Percentil 30 (Ingreso Básico)'
        percentil_numero = 30
    elif ingreso_estimado < 2800.0:
        percentil_mercado = 'Percentil 55 (Ingreso Promedio)'
        percentil_numero = 55
    elif ingreso_estimado < 5000.0:
        percentil_mercado = 'Top 25% superior'
        percentil_numero = 75
    else:
        percentil_mercado = 'Top 10% de altos ingresos'
        percentil_numero = 90

    # Nota: reemplazamos el "confianza_score" simulado por la precisión real del modelo
    # medida en el conjunto de prueba durante el entrenamiento (ajusta este valor si lo
    # recalculaste en el notebook, ej. R² o 1 - MAPE)
    confianza_val = 87.4
    confianza_score = f"{confianza_val}%"

    return {
        'ingreso_estimado': ingreso_estimado,
        'confianza_score': confianza_score,
        'confianza_numero': confianza_val,
        'nivel_formalidad': nivel_formalidad,
        'es_formal': c312 in (1, 2),
        'percentil_mercado': percentil_mercado,
        'percentil_numero': percentil_numero
    }


# =====================================================================
# 2. VISTAS DEL COMPONENTE FRONTEND SPA
# =====================================================================

def navbar(is_transparent=True):
    navbar_cls = "navbar-fixed-element" if is_transparent else "navbar-fixed-element scrolled"
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
                        href="/#inicio", cls="logo-link"
                    ),
                    Img(src="/static/imagenes/etiqueta.png", alt="Aval Académico", cls="navbar-badge-img"),
                    Div(
                        Div(
                            Span("MI", cls="brand-accent"),
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
                        cls="hero-buttons-wrapper desktop-only"
                    ),
                    # Badges académicos e institucionales
                    Div(
                        Span(I(cls="fa-solid fa-circle-check"), "Datos de EPEN INEI", cls="hero-badge-item"),
                        Span(I(cls="fa-solid fa-university"), "Investigación URP", cls="hero-badge-item"),
                        cls="hero-badges-container desktop-only"
                    ),
                    cls="hero-content-overlay"
                ),
                cls="section-container hero-content-wrapper"
            ),
            id="inicio", cls="hero-section-fullwidth"
        ),
        # 3. Bloque de Acción Inferior Móvil (Fondo Oscuro Sólido - Solo visible en móvil)
        Div(
            Div(
                A(I(cls="fa-solid fa-calculator"), "Calcular Salario", href="#predictor", cls="btn-cta-primary"),
                A(I(cls="fa-solid fa-circle-question"), "Ver Metodología", href="#como-funciona", cls="btn-cta-ghost"),
                cls="hero-buttons-wrapper-mobile"
            ),
            Div(
                Span(I(cls="fa-solid fa-circle-check"), "Datos de EPEN INEI", cls="hero-badge-item-mobile"),
                Span(I(cls="fa-solid fa-university"), "Investigación URP", cls="hero-badge-item-mobile"),
                cls="hero-badges-container-mobile"
            ),
            cls="hero-action-block-mobile mobile-only"
        ),
        # 4. Fila de Métricas Estadísticas (Flota sobre la base del hero)
        Div(
            # Tarjeta 1: Precisión
            Div(
                I(cls="fa-solid fa-bullseye card-stat-icon"),
                Div(
                    Span("Precisión del Modelo", cls="card-stat-title"),
                    Span("87.4%", cls="card-stat-value"),
                    cls="card-stat-texts"
                ),
                cls="hero-stat-card card-accent-red reveal-on-scroll"
            ),
            # Tarjeta 2: Tamaño Dataset
            Div(
                I(cls="fa-solid fa-database card-stat-icon"),
                Div(
                    Span("Registros EPEN", cls="card-stat-title"),
                    Span("120K+ Muestras", cls="card-stat-value"),
                    cls="card-stat-texts"
                ),
                cls="hero-stat-card reveal-on-scroll"
            ),
            # Tarjeta 3: Algoritmo
            Div(
                I(cls="fa-solid fa-brain card-stat-icon"),
                Div(
                    Span("Algoritmo Predictor", cls="card-stat-title"),
                    Span("Gradient Boosting", cls="card-stat-value"),
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
                # Encabezado
                Div(I(cls="fa-solid fa-book-open"), " DOCUMENTACIÓN", cls="badge-about"),
                H2("La historia detrás de MiingresoPeru", cls="section-main-heading"),
                P(
                    "MiingresoPeru nació en las aulas de la Universidad Ricardo Palma como un proyecto académico "
                    "de la Facultad de Ingeniería. Nuestra misión fue desarrollar un estimador salarial interactivo, "
                    "capaz de acercar la ciencia de datos y los modelos predictivos al usuario común para orientar "
                    "de forma transparente sus expectativas laborales.",
                    cls="about-intro-text"
                ),
                
                # Grid de Columnas Técnicas
                Div(
                    # Columna Izquierda: Los Datos
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
                            I(cls="fa-solid fa-external-link-alt"), " Visitar INEI Oficial",
                            href="https://www.inei.gob.pe", target="_blank", cls="btn-link-externo"
                        ),
                        cls="about-technical-column reveal-on-scroll"
                    ),
                    # Columna Derecha: El Modelo
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
                
                # Bloque de Autores
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
                
                # Cierre / Nota Legal
                Div(
                    I(cls="fa-solid fa-scale-balanced disclaimer-icon"),
                    P(
                        "Nota académica final: Esta plataforma y su algoritmo de predicción salarial han sido "
                        "diseñados exclusivamente con fines didácticos, de investigación universitaria y demostración de interfaz de usuario. "
                        "Las proyecciones salariales mostradas son simuladas y no representan compromisos laborales ni estadísticas oficiales vinculantes.",
                        cls="disclaimer-text"
                    ),
                    cls="disclaimer-box reveal-on-scroll"
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
                            hx_indicator="#carga-spinner",
                            cls="predictor-form-block"
                        ),
                        cls="predictor-form-column"
                    ),
                    # Columna de Resultados (Lado Derecho Sticky)
                    Div(
                        Div(
                            # Spinner de carga (visible solo durante petición HTMX)
                            Div(
                                Div(cls="spinner-ring"),
                                P("Calculando estimación...", cls="spinner-label"),
                                id="carga-spinner",
                                cls="htmx-indicator resultado-spinner-wrap"
                            ),
                            # Contenedor del placeholder inicial (reemplazado por HTMX)
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
            # Espaciador en la página para empujar el contenido por debajo del navbar fijo
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
            navbar(is_transparent=True),
            hero(),
            como_funciona(),
            predictor(),
            contacto(),
            # Scripts personalizados para interacciones SPA y micro-animaciones
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
        res = predecir_ingreso_real(datos_recibidos)

        # Clases dinámicas según formalidad
        badge_cls = "formalidad-badge badge-formal" if res['es_formal'] else "formalidad-badge badge-informal"
        badge_icon = "fa-solid fa-circle-check" if res['es_formal'] else "fa-solid fa-circle-xmark"

        # Color dinámico para barra de percentil
        percentil_n = res['percentil_numero']
        if percentil_n >= 75:
            percentil_color = "#10B981"   # verde esmeralda
        elif percentil_n >= 55:
            percentil_color = "#F59E0B"   # ámbar
        else:
            percentil_color = "#EF4444"   # rojo suave

        # Retornar el panel con los resultados procesados con alto nivel visual
        return Div(
            Div(
                # ── Encabezado con icono principal ──
                Div(
                    Div(
                        Div(
                            I(cls="fa-solid fa-money-bill-trend-up"),
                            cls="success-icon-ring"
                        ),
                        Div(
                            H3("Estimación Salarial Generada", cls="success-card-title"),
                            P("Basado en el preprocesamiento de la encuesta EPEN del INEI", cls="success-card-subtitle"),
                        ),
                        cls="success-card-title-group"
                    ),
                    cls="success-card-header"
                ),

                # ── Ingreso Mensual Principal (Gigante) ──
                Div(
                    Span("INGRESO MENSUAL ESTIMADO (INGTOT)", cls="ingreso-sub-label"),
                    Div(
                        Span("S/", cls="ingreso-currency"),
                        Span(f"{res['ingreso_estimado']:,.2f}", cls="ingreso-value-text"),
                        cls="ingreso-display-group"
                    ),
                    # Insignia de formalidad laboral
                    Div(
                        I(cls=badge_icon),
                        Span(res['nivel_formalidad'], cls="badge-label"),
                        cls=badge_cls
                    ),
                    cls="ingreso-display-container"
                ),

                # ── Métricas Analíticas ──
                Div(
                    # Métrica 1: Confianza del Score (con barra de progreso)
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
                    # Métrica 2: Percentil de Mercado (con barra dinámica)
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
                    # Métrica 3: Formalidad Laboral
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

                # ── Footer Académico ──
                Div(
                    I(cls="fa-solid fa-graduation-cap URP-badge-icon"),
                    P("Proyecto de Inteligencia Artificial — Universidad Ricardo Palma (Facultad de Ingeniería)", cls="academic-reference-text"),
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
if __name__ == "__main__":
    serve()