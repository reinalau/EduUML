"""Prompts for different UML diagram types."""

DIAGRAM_PROMPTS = {
    "use_case": """Actúa como un ingeniero de software, experto en Ingenieria de Requerimientos. Analiza el código fuente adjunto y genera un diagrama UML de Casos de Uso. 
                REQUISITOS:
                a-Genera código {format_diagram} funcional para el diagrama.
                b-Identifica los actores y casos de uso principales implementados en el codigo (no inventar casos de uso que aun no existen en el codgo fuente).
                c-Proporciona una explicación educativa clara de lo que muestra el diagrama, los patrones encontrados y las relaciones principales.
                d-Responde exclusivamente en formato JSON con la siguiente estructura: 
                {
                "metadata": "Explicación detallada en español para estudiantes",
                "codigoUML": "código {format_diagram} aquí"
                }""",

    "sequence": """Actúa como un ingeniero de software, experto en Ingenieria de Requerimientos. Analiza el código fuente adjunto y genera un diagrama UML de Secuencia. 
                REQUISITOS:
                a-Genera código {format_diagram} funcional para el diagrama.
                b-Identificar: los actores (quienes inician) y los objetos (componentes del sistema) involucrados, sus líneas de vida (la existencia a lo largo del tiempo), los mensajes (interacciones) que se envían entre ellos en orden cronológico descendente, y las barras de activación para mostrar cuándo están activos, además de usar fragmentos para bucles o condiciones (no INVENTAR ACTIVIDADES que NO existen en el codgo fuente). 
                c-Proporciona una explicación educativa clara de lo que muestra el diagrama, los patrones encontrados y las relaciones principales.
                d-Responde exclusivamente en formato JSON con la siguiente estructura: 
                {
                "metadata": "Explicación detallada en español para estudiantes",
                "codigoUML": "código {format_diagram} aquí"
                }""",

    "activity": """Actúa como un ingeniero de software, experto en Ingenieria de Requerimientos. Analiza el código fuente adjunto y genera un diagrama UML de Actividad. 
                REQUISITOS:
                a-Genera código {format_diagram} funcional para el diagrama.
                b-Identificar las Acciones (pasos/tareas), el Nodo Inicial y Final, los Flujos de Control (flechas), los Nodos de Decisión (rombos) y de Unión/Bifurcación (barras para concurrencia), y las Particiones de Actividad (Carriles) si hay varios actores, para describir el flujo de trabajo o control de un sistema.
                c-Proporciona una explicación educativa clara de lo que muestra el diagrama, los patrones encontrados y las relaciones principales.
                d-Responde exclusivamente en formato JSON con la siguiente estructura: 
                {
                "metadata": "Explicación detallada en español para estudiantes",
                "codigoUML": "código {format_diagram} aquí"
                }""",

    "class": """Actúa como un arquitecto de software senior y profesor de ingeniería. Analiza el código fuente adjunto y genera un diagrama UML de Clases. 
                REQUISITOS:
                a-Genera código {format_diagram} funcional para el diagrama. 
                b-Proporciona una explicación educativa clara de lo que muestra el diagrama, los patrones encontrados y las relaciones principales.
                c-Responde exclusivamente en formato JSON con la siguiente estructura: 
                {
                "metadata": "Explicación detallada en español para estudiantes",
                "codigoUML": "código {format_diagram} aquí"
                }""",

    "component": """Actúa como un ingeniero de software, experto en Ingenieria de Requerimientos. Analiza el código fuente adjunto y genera un diagrama UML de Componentes. 
                REQUISITOS:
                a-Genera código {format_diagram} funcional para el diagrama.
                b-Identifica los módulos físicos o lógicos de tu sistema (como una UI, una pasarela de pago), representándolos con el ícono de componente (rectángulo con estereotipo <>), luego conecta estos componentes usando interfaces (círculos para las que provee, semicírculos para las que necesita) y define las relaciones (dependencia con línea discontinua, asociación con línea sólida), y finalmente agrupa componentes en paquetes para mostrar la estructura general.
                c-Ten en cuenta la inFraestructura como codigo (IAC: como .yaml, yml o .tf. Si encuentras IAC duplicada en diferentes lenguajes toma las de terraform).
                d-Proporciona una explicación educativa clara de lo que muestra el diagrama, los patrones encontrados y las relaciones principales.
                e-Responde exclusivamente en formato JSON con la siguiente estructura: 
                {
                "metadata": "Explicación detallada en español para estudiantes",
                "codigoUML": "código {format_diagram} aquí"
                }""",

    "deployment": """Actúa como un ingeniero de software, experto en Ingenieria de Requerimientos. Analiza el código fuente adjunto y genera un diagrama UML de Despliegue. 
                REQUISITOS:
                a-Genera código {format_diagram} funcional para el diagrama.
                b-Identifica los nodos físicos (hardware como servidores, dispositivos) y los artefactos (software como archivos ejecutables), luego dibuja las conexiones (rutas de comunicación) entre ellos y asigna los artefactos a sus nodos, usando formas estándar de UML como cubos para nodos y cajas para artefactos para visualizar la arquitectura física del sistema y sus componentes de software.
                c-Ten en cuenta el codigo de inFraestructura como codigo (IAC: como .yaml, yml o .tf. Si encuentras IAC duplicada en diferentes lenguajes toma las de terraform).
                d-Responde exclusivamente en formato JSON con la siguiente estructura: 
                {
                "metadata": "Explicación detallada en español para estudiantes",
                "codigoUML": "código {format_diagram} aquí"
                }""",

    "state": """Actúa como un ingeniero de software, experto en Ingenieria de Requerimientos. Analiza el código fuente adjunto y genera un diagrama UML de Estados. 
                REQUISITOS:
                a-Genera código {format_diagram} funcional para el diagrama.
                b-Identifica los estados por los que pasa un objeto, represéntalos con rectángulos redondeados, usa un círculo negro sólido para el inicio y un círculo negro con otro dentro para el final, y conecta los estados con flechas (transiciones) que indiquen el cambio y el evento que lo causa (ej. evento [condición] / acción), utilizando rombos para decisiones (bifurcaciones).
                c-Responde exclusivamente en formato JSON con la siguiente estructura: 
                {
                "metadata": "Explicación detallada en español para estudiantes",
                "codigoUML": "código {format_diagram} aquí"
                }"""
}