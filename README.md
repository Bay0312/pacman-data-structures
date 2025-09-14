# 🎮 Pacman — Data Structures

> **Implementación moderna del clásico Pac-Man** desarrollada en **Python + Pygame** para practicar estructuras de datos y algoritmos (pathfinding A*, máquinas de estado y AI de fantasmas). Incluye build WebAssembly y deploy automático.

[![Demo Web](https://img.shields.io/badge/🌐_Demo-Jugar_Ahora-4CAF50?style=for-the-badge)](https://bay0312.github.io/pacman-data-structures/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)](https://python.org)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green?style=flat&logo=python)](https://pygame.org)

---

## 🌟 Características Principales

<div align="center">
<table>
<tr>
<td align="center">🖥️<br><b>Local</b><br>Fluido y sin<br>dependencias extra</td>
<td align="center">🌐<br><b>Web</b><br>WASM + Pyodide<br>sin instalación</td>
<td align="center">💾<br><b>Guardado</b><br>Sistema de<br>persistencia JSON</td>
<td align="center">👻<br><b>IA Avanzada</b><br>A* pathfinding<br>múltiples modos</td>
</tr>
</table>
</div>

### ✨ Funcionalidades

- **🎵 Audio inteligente** con arranque seguro multiplataforma
- **⌨️ Controles responsive** con estados de juego (ready/pausa/victoria)
- **🎯 IA de fantasmas** con algoritmos A* y modos scatter/chase/frightened
- **📊 Estructuras de datos** optimizadas para rendimiento y aprendizaje

---

## 🎯 Demo en Vivo

### [🔗 **Jugar en el Navegador**](https://bay0312.github.io/pacman-data-structures/)

> **⚠️ Demo Experimental:** Algunas funciones (audio y notificaciones) pueden comportarse diferente debido a limitaciones de WebAssembly/Pyodide.

---

## 🎮 Controles

| Tecla | Acción | Contexto |
|-------|--------|----------|
| **↑ ↓ ← →** | Mover Pac-Man | Durante el juego |
| **ESC** | Pausar/Reanudar | Cualquier momento |
| **G** | Guardar partida | Solo en pausa (No hay aviso de que el guardado fue exitoso) |
| **C** | Cargar partida | Solo en pausa |
| **Q** | Salir del juego | Solo en pausa |
| **ENTER** | Reiniciar | Tras victoria/derrota |

---

## 🚀 Instalación y Ejecución

### 💻 Método Local (Recomendado)

**Requisitos:** Python 3.10+ y pip

```bash
# 1. Clonar repositorio
git clone https://github.com/bay0312/pacman-data-structures.git
cd pacman-data-structures/PacMan

# 2. (Opcional) Crear entorno virtual
python -m venv .venv

# Activar entorno:
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# 3. Instalar dependencias
pip install pygame

# 4. Ejecutar juego
python main.py
```

> 💡 **Tip:** El archivo `guardado.json` se genera automáticamente al usar la función de guardado en el juego.

### 🌐 Build para Web (Opcional)

```bash
# Instalar herramientas de build web
pip install pygbag==0.9.2

# Construir versión web
cd pacman-data-structures/PacMan
pygbag --build .

# Archivos generados en: PacMan/build/web/
```

---

## 📁 Arquitectura del Proyecto

<details>
<summary><b>🏗️ Ver estructura completa</b></summary>

```
pacman-data-structures/
├── PacMan/                    # 📦 Código principal
│   ├── main.py               # 🚀 Loop principal y estados
│   ├── mapa.py               # 🗺️ Grid, paredes, elementos
│   ├── pacman.py             # 🟡 Lógica del jugador
│   ├── blinky.py             # 👻 Fantasma rojo (A* directo)
│   ├── pinky.py              # 🩷 Fantasma rosa (A* predictivo)
│   ├── clyde.py              # 🟠 Fantasma naranja (mixto)
│   ├── inky.py               # 🩵 Fantasma cian (esquina/mixto)
│   ├── elementos.py          # 🔵 Puntos, píldoras, frutas
│   ├── config.py             # ⚙️ Configuración global
│   ├── img/                  # 🖼️ Sprites y gráficos
│   ├── Fantasmas/            # 👻 Animaciones fantasmas
│   ├── sonidos/              # 🎵 Efectos y música
│   └── guardado.json         # 💾 Estado guardado (auto)
├── .github/workflows/
│   └── deploy.yml            # 🤖 CI/CD automático
└── README.md
```

</details>

---

## 🧠 Estructuras de Datos y Algoritmos

<div align="center">
<table>
<tr>
<th>🔧 Componente</th>
<th>📊 Estructura</th>
<th>🎯 Propósito</th>
</tr>
<tr>
<td><b>Grid/Mapa</b></td>
<td>Matriz 2D</td>
<td>Colisiones, render, pathfinding</td>
</tr>
<tr>
<td><b>Pathfinding</b></td>
<td>A* + heapq</td>
<td>IA fantasmas con heurística Manhattan</td>
</tr>
<tr>
<td><b>Estados IA</b></td>
<td>State Machine</td>
<td>Scatter → Chase → Frightened</td>
</tr>
<tr>
<td><b>Estados Juego</b></td>
<td>Enum States</td>
<td>PREPARADO → JUGANDO → PAUSA → FIN</td>
</tr>
<tr>
<td><b>Persistencia</b></td>
<td>JSON serialization</td>
<td>Guardado/carga de partidas</td>
</tr>
</table>
</div>

### 🎮 Algoritmos Implementados

- **A\* Pathfinding:** Para navegación inteligente de fantasmas
- **State Machines:** Gestión de estados de juego y comportamiento de IA
- **Collision Detection:** Sistema optimizado de detección de colisiones
- **JSON Serialization:** Persistencia eficiente del estado del juego

---

## 🌐 Deploy Automático

El proyecto incluye **GitHub Actions** para deploy automático:

### 🔄 Workflow Automático
1. **Build** con pygbag en cada push
2. **Deploy** a GitHub Pages automáticamente 
3. **Actualización** de la demo en vivo

### ⚙️ Configuración
```yaml
# Rama de trigger: web-demo
# Configurar en: Settings → Pages → Source: GitHub Actions
```

---

## ⚠️ Limitaciones Conocidas (Demo Web)

<div align="center">
<table>
<tr>
<th>🚨 Problema</th>
<th>📝 Descripción</th>
<th>💡 Solución</th>
</tr>
<tr>
<td><b>🔇 Audio</b></td>
<td>Bloqueado sin interacción del usuario</td>
<td>Clic inicial en canvas</td>
</tr>
<tr>
<td><b>🎵 Calidad</b></td>
<td>Variaciones por sample rate web</td>
<td>Navegadores actualizados</td>
</tr>
<tr>
<td><b>💾 Guardado</b></td>
<td>Limitado a sesión del navegador</td>
<td>Versión local para persistencia</td>
</tr>
<tr>
<td><b>⏱️ Rendimiento</b></td>
<td>FPS reducido en segundo plano</td>
<td>Mantener pestaña activa</td>
</tr>
<tr>
<td><b>🪟 Notificaciones</b></td>
<td>Mensajes breves pueden no verse</td>
<td>Repetir acción si necesario</td>
</tr>
</table>
</div>

---

## 🛠️ Troubleshooting

<details>
<summary><b>🐛 Problemas Comunes</b></summary>

### Pantalla negra en web
- Añade `#debug` a la URL para ver logs
- Verifica existencia de assets en rutas correctas
- Revisa consola del navegador

### Audio no funciona
- Realiza clic o pulsa tecla para "desbloquear" audio
- Los navegadores modernos requieren gesto del usuario
- Verifica permisos de audio del sitio

### Guardado no visible
- Pausa con `ESC` y presiona `G`
- Modal de confirmación es breve (2-3 segundos)
- Repite la acción si no aparece

### CI/CD falla
- Confirma estructura de carpetas
- Verifica branch `web-demo` para trigger
- Revisa permisos de GitHub Pages

</details>

---

## 🔧 Desarrollo

### 🛠️ Stack Tecnológico
- **Python 3.10+** - Lenguaje principal
- **Pygame 2.0+** - Engine gráfico y de audio  
- **pygbag** - Compilación a WebAssembly
- **GitHub Actions** - CI/CD automatizado

### 📋 Requirements (Opcional)
```txt
pygame==2.*
# Solo para build web local
pygbag==0.9.2
```

---

### 🎨 Recursos
- **Gráficos:** Creación original 
- **Audio:** De sus respectivos autores

### ⚖️ Marca Registrada
*Pac-Man* es marca registrada de sus titulares. Este proyecto es con **fines educativos**.

</div>
