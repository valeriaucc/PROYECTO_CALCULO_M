
let currentCountry = "Colombia"
let updateInterval = null
let manualTimeOffset = 0 
let isManualMode = false 

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", () => {
  console.log("CLOCK SIGYE iniciado")
  initializeApp()
})

/**
 * Inicializa la aplicación
 */
function initializeApp() {
  // Configurar el selector de país
  const countrySelect = document.getElementById("countrySelect")
  countrySelect.addEventListener("change", handleCountryChange)

  document.getElementById("increaseHour").addEventListener("click", () => adjustTime(3600))
  document.getElementById("decreaseHour").addEventListener("click", () => adjustTime(-3600))
  document.getElementById("increaseMinute").addEventListener("click", () => adjustTime(60))
  document.getElementById("decreaseMinute").addEventListener("click", () => adjustTime(-60))
  document.getElementById("resetTime").addEventListener("click", resetTime)

  // Cargar la hora inicial
  updateTime()

  // Actualizar cada segundo
  updateInterval = setInterval(updateTime, 1000)

  // Cargar relojes mundiales
  loadWorldClocks()

  console.log(" Aplicación inicializada correctamente")
}

/**
 * Maneja el cambio de país seleccionado
 */
function handleCountryChange(event) {
  currentCountry = event.target.value
  console.log(` País cambiado a: ${currentCountry}`)
  resetTime() // Reset manual offset when changing country
  updateTime()
}

/**
 * Ajusta la hora manualmente
 * @param {number} seconds - Segundos a ajustar (positivo o negativo)
 */
function adjustTime(seconds) {
  isManualMode = true
  manualTimeOffset += seconds
  updateTime()
}

/**
 * Reinicia el reloj a la hora actual real
 */
function resetTime() {
  isManualMode = false
  manualTimeOffset = 0
  updateTime()
}

/**
 * Actualiza la hora del reloj principal
 */
async function updateTime() {
  try {
    const response = await fetch(`/time?country=${currentCountry}`)

    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`)
    }

    const data = await response.json()

    if (isManualMode && manualTimeOffset !== 0) {
      const adjustedData = applyTimeOffset(data, manualTimeOffset)
      updateClockDisplay(adjustedData)
      updateAnalogClock(adjustedData)
      updateLocationInfo(data) // Keep original location
      updatePeriodIndicator(adjustedData)
      updateMotivationalPhrase(adjustedData)
      updateTheme(adjustedData.is_day)
    } else {
      updateClockDisplay(data)
      updateAnalogClock(data)
      updateLocationInfo(data)
      updatePeriodIndicator(data)
      updateMotivationalPhrase(data)
      updateTheme(data.is_day)
    }
  } catch (error) {
    console.error(" Error al actualizar la hora:", error)
    showErrorMessage("No se pudo actualizar la hora. Reintentando...")
  }
}

/**
 * Aplica un offset de tiempo a los datos
 * @param {Object} data - Datos originales del tiempo
 * @param {number} offsetSeconds - Offset en segundos
 * @returns {Object} Datos ajustados
 */
function applyTimeOffset(data, offsetSeconds) {
  const adjustedData = { ...data }

  let totalSeconds = data.hour * 3600 + data.minute * 60 + data.second + offsetSeconds

  // Normalizar a rango 0-86399 (24 horas)
  while (totalSeconds < 0) totalSeconds += 86400
  while (totalSeconds >= 86400) totalSeconds -= 86400

  adjustedData.hour = Math.floor(totalSeconds / 3600)
  adjustedData.minute = Math.floor((totalSeconds % 3600) / 60)
  adjustedData.second = totalSeconds % 60

  // Recalcular AM/PM
  const hour12 = adjustedData.hour % 12 || 12
  adjustedData.am_pm = adjustedData.hour >= 12 ? "P.M." : "A.M."

  // Recalcular día/noche
  adjustedData.is_day = adjustedData.hour >= 6 && adjustedData.hour < 18

  return adjustedData
}

/**
 * Actualiza el reloj analógico
 * @param {Object} data - Datos del tiempo
 */
function updateAnalogClock(data) {
  const hourHand = document.getElementById("hourHand")
  const minuteHand = document.getElementById("minuteHand")
  const secondHand = document.getElementById("secondHand")

  // Calcular ángulos (0° = 12 en punto, sentido horario)
  const secondAngle = data.second * 6 // 6° por segundo
  const minuteAngle = data.minute * 6 + data.second * 0.1 // 6° por minuto + movimiento suave
  const hourAngle = (data.hour % 12) * 30 + data.minute * 0.5 // 30° por hora + movimiento suave

  // Aplicar rotaciones
  hourHand.style.transform = `rotate(${hourAngle}deg)`
  minuteHand.style.transform = `rotate(${minuteAngle}deg)`
  secondHand.style.transform = `rotate(${secondAngle}deg)`
}

/**
 * Actualiza el display del reloj digital
 */
function updateClockDisplay(data) {
  const hoursElement = document.getElementById("hours")
  const minutesElement = document.getElementById("minutes")
  const secondsElement = document.getElementById("seconds")
  const dateElement = document.getElementById("dateDisplay")
  const amPmElement = document.getElementById("amPm")

  // Convertir a formato 12 horas
  const hour12 = data.hour % 12 || 12

  // Formatear con ceros a la izquierda
  hoursElement.textContent = String(hour12).padStart(2, "0")
  minutesElement.textContent = String(data.minute).padStart(2, "0")
  secondsElement.textContent = String(data.second).padStart(2, "0")

  amPmElement.textContent = data.am_pm

  // Actualizar fecha
  dateElement.textContent = data.formatted_date
}

/**
 * Actualiza la información de ubicación
 */
function updateLocationInfo(data) {
  document.getElementById("countryFlag").textContent = data.flag
  document.getElementById("countryName").textContent = data.country
  document.getElementById("cityName").textContent = data.city
  document.getElementById("gmtInfo").textContent = data.gmt
}

/**
 * Actualiza el indicador de período (día/noche)
 */
function updatePeriodIndicator(data) {
  const periodIcon = document.getElementById("periodIcon")
  const periodText = document.getElementById("periodText")

  if (data.is_day) {
    
    periodText.textContent = "DÍA"
  } else {
    
    periodText.textContent = "NOCHE"
  }
}

/**
 * Actualiza la frase motivacional
 */
function updateMotivationalPhrase(data) {
  const phraseElement = document.getElementById("motivationalPhrase")

  // Solo actualizar si la frase cambió (para evitar animaciones innecesarias)
  if (phraseElement.textContent !== data.phrase) {
    phraseElement.style.animation = "none"
    setTimeout(() => {
      phraseElement.textContent = data.phrase
      phraseElement.style.animation = "fadeIn 1s ease-out"
    }, 50)
  }
}

/**
 * Actualiza el tema visual (día/noche)
 */
function updateTheme(isDay) {
  const body = document.body

  if (isDay) {
    body.classList.remove("night-mode")
    body.classList.add("day-mode")
  } else {
    body.classList.remove("day-mode")
    body.classList.add("night-mode")
  }
}

/**
 * Carga los relojes mundiales
 */
async function loadWorldClocks() {
  try {
    const response = await fetch("/timezones")
    const timezones = await response.json()

    const worldClocksGrid = document.getElementById("worldClocksGrid")
    worldClocksGrid.innerHTML = ""

    // Crear tarjetas para cada zona horaria (excepto la actual)
    for (const [country, info] of Object.entries(timezones)) {
      if (country !== currentCountry) {
        const card = createWorldClockCard(country, info)
        worldClocksGrid.appendChild(card)
      }
    }

    // Actualizar relojes mundiales cada segundo
    setInterval(updateWorldClocks, 1000)
  } catch (error) {
    console.error(" Error al cargar relojes mundiales:", error)
  }
}

/**
 * Crea una tarjeta de reloj mundial
 */
function createWorldClockCard(country, info) {
  const card = document.createElement("div")
  card.className = "world-clock-card"
  card.dataset.country = country

  card.innerHTML = `
        <div class="world-clock-header">
            <span class="world-clock-flag">${info.flag}</span>
            <div>
                <div class="world-clock-name">${country}</div>
                <div style="font-size: 0.85rem; opacity: 0.7;">${info.city}</div>
            </div>
        </div>
        <div class="world-clock-time" data-time="${country}">--:--:--</div>
    `

  // Hacer clic en la tarjeta para cambiar a ese país
  card.addEventListener("click", () => {
    document.getElementById("countrySelect").value = country
    currentCountry = country
    updateTime()
    loadWorldClocks() 
  })

  return card
}

/**
 * Actualiza todos los relojes mundiales
 */
async function updateWorldClocks() {
  const timeElements = document.querySelectorAll("[data-time]")

  for (const element of timeElements) {
    const country = element.dataset.time

    try {
      const response = await fetch(`/time/${country}`)
      const data = await response.json()
      element.textContent = data.formatted_time
    } catch (error) {
      console.error(` Error al actualizar ${country}:`, error)
    }
  }
}

/**
 * Muestra un mensaje de error
 */
function showErrorMessage(message) {
  // Crear elemento de notificación si no existe
  let notification = document.getElementById("errorNotification")

  if (!notification) {
    notification = document.createElement("div")
    notification.id = "errorNotification"
    notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(239, 68, 68, 0.95);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            animation: fadeInDown 0.5s ease-out;
        `
    document.body.appendChild(notification)
  }

  notification.textContent = message
  notification.style.display = "block"

  // Ocultar después de 3 segundos
  setTimeout(() => {
    notification.style.display = "none"
  }, 3000)
}

/**
 * Limpia los intervalos al cerrar la página
 */
window.addEventListener("beforeunload", () => {
  if (updateInterval) {
    clearInterval(updateInterval)
  }
})

// Manejo de errores globales
window.addEventListener("error", (event) => {
  console.error(" Error global:", event.error)
})

console.log(" App.js cargado correctamente")
