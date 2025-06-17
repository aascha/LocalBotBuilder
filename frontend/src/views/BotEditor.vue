<template>
  <div class="bot-overview-page">
    <!-- Header -->
    <header class="nav-bar">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
      </router-link>

      <div class="user-menu">
        <div class="username-label" @click="toggleMenu">
          {{ username || 'Benutzer' }}
        </div>
        <ul v-if="menuOpen" class="menu-dropdown">
          <li @click="logout">Logout</li>
        </ul>
      </div>
    </header>


    <!-- Bot Editor -->
    <div class="bot-overview-box">
      <div class="bot-editor-header-row">
        <h2 class="bot-editor-heading">
          {{ botName }}
          <font-awesome-icon icon="pencil" class="pencil-icon" />
        </h2>
        <button class="save-btn" @click="save">Änderungen speichern</button>
      </div>

      <div class="grey-line"></div>

      <!-- Eigenschaften -->
      <h3 class="bot-editor-subheading">
        Eigenschaften
        <font-awesome-icon icon="pencil" class="pencil-icon" />
      </h3>
      <div class="tag-row">
        <button
          v-for="(t, i) in tags"
          :key="i"
          :class="{ selected: t.selected }"
          class="tag-btn"
          @click="selectTone(i)"
        >
          {{ t.label }}
        </button>
      </div>

      <!-- Beschreibung -->
      <h3 class="bot-editor-subheading">
        Beschreibung
        <font-awesome-icon icon="pencil" class="pencil-icon" />
      </h3>
      <div class="desc-box-editor">
        <textarea
          v-model="desc"
          class="desc-input"
          placeholder="Dies ist eine Test-Beschreibung."
        ></textarea>
      </div>

      <!-- Vorschaubild (empty for now) -->
      <h3 class="bot-editor-subheading">
        Vorschaubild
        <font-awesome-icon icon="pencil" class="pencil-icon" />
      </h3>
      <div class="icon-preview"></div>

      <div class="grey-line"></div>

      <!-- Buttons -->
      <div class="editor-button-row">
        <button class="download-btn" @click="download">Herunterladen</button>
        <button class="share-btn" @click="share">Teilen</button>
      </div>
    </div>

    <!-- Footer -->
    <div class="bottom-bar">
      <ul>
        <li><router-link to="/impressum">Impressum</router-link></li>
        <li><router-link to="/datenschutz">Datenschutz</router-link></li>
      </ul>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const botId = ref(null)
const botName = ref("Test Bot")
const desc = ref("")
const tags = ref([])
const menuOpen = ref(false)
const username = ref("Benutzer")

const allTags = [
  "Einfache Antworten", "Lustig", "Motivierend", "Detailliert",
  "Versichernd", "Freundlich", "Professionell", "Nachvollziehbar", "Verständig"
]

// ✅ Load user info
async function getUser() {
  try {
    const res = await axios.get("/api/me", { withCredentials: true })
    username.value = res.data?.user?.name || "Benutzer"
  } catch (err) {
    console.error("Benutzer konnte nicht geladen werden:", err)
  }
}

// ✅ Load bot data
onMounted(async () => {
  await getUser()
  botId.value = route.query.id
  try {
    const res = await axios.get(`/api/bot/${botId.value}`, { withCredentials: true })
    const bot = res.data

    botName.value = bot.bot_name
    desc.value = bot.system_prompt || ""

    tags.value = allTags.map(label => ({
      label,
      selected: bot.tone === label
    }))
  } catch (err) {
    console.error("Fehler beim Laden:", err)
    router.push("/botoverview")
  }
})

// ✅ Save changes
async function save() {
  const selectedTone = tags.value.find(t => t.selected)?.label || "Einfache Antworten"

  const formData = new FormData()
  formData.append("bot_name", botName.value)
  formData.append("model_name", "qwen")
  formData.append("system_prompt", desc.value)
  formData.append("tone", selectedTone)
  formData.append("temperature", "0.7")
  formData.append("context_window", "2048")

  try {
    await axios.post(`/api/update/${botId.value}`, formData, { withCredentials: true })
    alert("✅ Änderungen gespeichert!")
  } catch (err) {
    console.error("Fehler beim Speichern:", err)
    alert("❌ Fehler beim Speichern.")
  }
}

// ✅ Download after save
async function download() {
  try {
    await save() // ensure updated

    const encoded = encodeURIComponent(botName.value)
    const downloadUrl = `/api/download/${encoded}`

    for (let i = 0; i < 5; i++) {
      const check = await fetch(downloadUrl, { method: 'HEAD' })
      if (check.ok) {
        const res = await fetch(downloadUrl)
        const blob = await res.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement("a")
        a.href = url
        a.download = `${encoded}_bot_package.zip`
        document.body.appendChild(a)
        a.click()
        a.remove()
        window.URL.revokeObjectURL(url)
        return
      }
      await new Promise(resolve => setTimeout(resolve, 1000)) // wait 1s
    }

    alert("❌ Der Download ist noch nicht bereit. Versuche es später erneut.")
  } catch (err) {
    console.error("Download fehlgeschlagen:", err)
    alert("❌ Fehler beim Herunterladen.")
  }
}

// Placeholder
function share() {
  alert("🔗 Teilen-Funktion kommt bald!")
}

// UI control
function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

async function logout() {
  try {
    await axios.post("/api/logout", {}, { withCredentials: true })
    router.push("/login")
  } catch (err) {
    console.error("Logout fehlgeschlagen:", err)
  }
}

function selectTone(index) {
  tags.value.forEach((t, i) => t.selected = i === index)
}
</script>
