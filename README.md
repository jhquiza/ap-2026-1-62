# Repositorio de la asignatura de Análisis Predictivo, periodo 2026-1, cohorte 62

Este es el repositorio oficial del curso de Análisis Predictivo de la Universidad de Medellín

---

# Guía de Trabajo con Git: Fork, Upstream y Entregas

Para el desarrollo de las actividades de la clase, utilizaremos un flujo de trabajo profesional. Siga estos pasos para configurar su entorno:

### 1. Crear su propia copia (Fork)

No trabajará directamente sobre el repositorio del profesor. Cada uno debe tener su copia personal en la nube.

1. Entre al enlace del repositorio de la clase: https://github.com/jhquiza/ap-2026-1-62.
2. En la esquina superior derecha, haga clic en el botón **Fork**.
3. Asegúrese de que el "Owner" sea su usuario de GitHub y haga clic en **Create fork**.

### 2. Clonar su Fork localmente

Ahora, descargue **su copia** (no la del profesor) a su computadora.

```bash
git clone https://github.com/SU_USUARIO/ap-2026-1-62.git
cd ap-2026-1-62
```

Configure el entorno con uv (Recomendado)

```bash
# Instalar uv si no lo tiene
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Sincronizar el entorno con el archivo pyproject.toml 
uv sync
```

### 3. Configurar el repositorio del Profesor como "Upstream"

Este paso es vital. Sirve para que, si el profesor añade nuevo material o corrige un ejercicio, usted pueda descargar esos cambios sin borrar su propio progreso.

En su terminal, dentro de la carpeta del proyecto, ejecute:

```bash
# Agregue el repo del profesor como una fuente remota llamada "upstream"
git remote add upstream https://github.com/jhquiza/ap-2026-1-62.git

# Verifique que ahora tiene dos remotos: origin (el suyo) y upstream (el de la clase)
git remote -v

```

### 4. ¿Cómo actualizar su trabajo con lo que suba el profesor?

Si el profesor avisa que hay material nuevo, no necesitan clonar todo de nuevo. Solo corra estos comandos:

```bash
# 1. Traer los cambios del profesor
git fetch upstream

# 2. Asegurarse de estar en su rama principal
git checkout main

# 3. Fusionar los cambios del profesor en su copia local
git merge upstream/main

```

### 5. Cómo entregar las tareas (Pull Request)

Cuando termine un ejercicio y quiera que el profesor lo revise:

1. Suba sus cambios a su propio GitHub (**origin**):

```bash
git add .
git commit -m "Solución a la actividad 1"
git push origin main

```

2. Entre a su repositorio en la web de GitHub.

3. Verá un mensaje que dice **"This branch is X commits ahead of... "**. Haga clic en **Contribute** y luego en **Open Pull Request**.

4. Escriba un título claro (ej: "Entrega Actividad 1 - Nombre del Estudiante") y envíenlo.

---
