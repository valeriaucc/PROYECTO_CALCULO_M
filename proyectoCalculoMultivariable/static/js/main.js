// Utilidades globales para la aplicación

/* global bootstrap, Plotly */

// Importaciones necesarias
const bootstrap = window.bootstrap
const Plotly = window.Plotly

// Formatear números
function formatNumber(num, decimals = 4) {
  if (typeof num !== "number") return num
  return num.toFixed(decimals)
}

// Validar función matemática
function validarFuncion(funcion) {
  if (!funcion || funcion.trim() === "") {
    return { valido: false, mensaje: "La función no puede estar vacía" }
  }

  // Caracteres permitidos
  const regex = /^[0-9a-zA-Z+\-*/().,\s^*sqrtlogexpsincostan]+$/
  if (!regex.test(funcion)) {
    return { valido: false, mensaje: "La función contiene caracteres no permitidos" }
  }

  return { valido: true }
}

// Mostrar notificación
function mostrarNotificacion(mensaje, tipo = "info") {
  const colores = {
    success: "#198754",
    error: "#dc3545",
    warning: "#ffc107",
    info: "#0dcaf0",
  }

  const notif = document.createElement("div")
  notif.className = "alert alert-" + tipo + " position-fixed top-0 start-50 translate-middle-x mt-3"
  notif.style.zIndex = "9999"
  notif.style.minWidth = "300px"
  notif.innerHTML = `
        <i class="fas fa-${tipo === "success" ? "check-circle" : tipo === "error" ? "exclamation-circle" : "info-circle"}"></i>
        ${mensaje}
    `

  document.body.appendChild(notif)

  setTimeout(() => {
    notif.style.opacity = "0"
    notif.style.transition = "opacity 0.5s"
    setTimeout(() => notif.remove(), 500)
  }, 3000)
}

// Copiar al portapapeles
function copiarAlPortapapeles(texto) {
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(texto)
      .then(() => {
        mostrarNotificacion("Copiado al portapapeles", "success")
      })
      .catch(() => {
        mostrarNotificacion("Error al copiar", "error")
      })
  } else {
    // Fallback para navegadores antiguos
    const textarea = document.createElement("textarea")
    textarea.value = texto
    textarea.style.position = "fixed"
    textarea.style.opacity = "0"
    document.body.appendChild(textarea)
    textarea.select()
    try {
      document.execCommand("copy")
      mostrarNotificacion("Copiado al portapapeles", "success")
    } catch (err) {
      mostrarNotificacion("Error al copiar", "error")
    }
    document.body.removeChild(textarea)
  }
}

// Descargar archivo
function descargarArchivo(contenido, nombreArchivo, tipoMime = "text/plain") {
  const blob = new Blob([contenido], { type: tipoMime })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = nombreArchivo
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

// Sanitizar entrada matemática
function sanitizarEntrada(texto) {
  if (!texto) return ""

  // Reemplazos comunes
  texto = texto.replace(/\^/g, "**")
  texto = texto.replace(/√/g, "sqrt")
  texto = texto.replace(/π/g, "pi")
  texto = texto.replace(/∞/g, "oo")
  texto = texto.replace(/×/g, "*")
  texto = texto.replace(/÷/g, "/")

  return texto.trim()
}

// Parsear punto desde string
function parsearPunto(x, y) {
  try {
    return [Number.parseFloat(x), Number.parseFloat(y)]
  } catch (e) {
    return null
  }
}

// Validar límites de integración
function validarLimites(limites) {
  if (!Array.isArray(limites)) return false

  for (const limite of limites) {
    if (!Array.isArray(limite) || limite.length !== 2) return false
  }

  return true
}

// Formatear ecuación para MathJax
function formatearEcuacion(ecuacion) {
  // Reemplazar ** por ^
  ecuacion = ecuacion.replace(/\*\*/g, "^")
  // Agregar espacios alrededor de operadores
  ecuacion = ecuacion.replace(/([+\-*/])/g, " $1 ")
  return ecuacion
}

// Manejar errores de API
function manejarErrorAPI(error) {
  console.error("Error de API:", error)

  if (error.message) {
    mostrarNotificacion(error.message, "error")
  } else {
    mostrarNotificacion("Error al comunicarse con el servidor", "error")
  }
}

// Inicializar tooltips de Bootstrap
document.addEventListener("DOMContentLoaded", () => {
  // Inicializar tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))

  // Agregar animación de fade-in a las cards
  const cards = document.querySelectorAll(".card")
  cards.forEach((card, index) => {
    setTimeout(() => {
      card.classList.add("fade-in")
    }, index * 100)
  })

  // Sanitizar inputs automáticamente
  const inputsMatematicos = document.querySelectorAll('input[type="text"]')
  inputsMatematicos.forEach((input) => {
    if (input.id && (input.id.includes("funcion") || input.id.includes("restriccion"))) {
      input.addEventListener("blur", function () {
        this.value = sanitizarEntrada(this.value)
      })
    }
  })
})

// Configuración global de Plotly
if (typeof Plotly !== "undefined") {
  Plotly.setPlotConfig({
    locale: "es",
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ["sendDataToCloud"],
    responsive: true,
  })
}

// Prevenir envío de formularios con Enter (excepto en textareas)
document.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && e.target.tagName !== "TEXTAREA") {
    const form = e.target.closest("form")
    if (form) {
      e.preventDefault()
      const submitBtn = form.querySelector('button[type="submit"]')
      if (submitBtn) submitBtn.click()
    }
  }
})

// Exportar funciones globales
window.AppUtils = {
  formatNumber,
  validarFuncion,
  mostrarNotificacion,
  copiarAlPortapapeles,
  descargarArchivo,
  sanitizarEntrada,
  parsearPunto,
  validarLimites,
  formatearEcuacion,
  manejarErrorAPI,
}
