<template>
  <div class="bot-overview-page">
    <!-- Header -->
    <header class="nav-bar">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
      </router-link>

      <div class="user-menu">
        <div class="avatar-icon name-icon" @click="openMenu">
          {{ user?.name || 'Lade...' }}
        </div>
        <ul v-if="menuOpen" class="menu-dropdown" @click.stop>
          <li class="menu-user">{{ user?.name || 'Lade...' }}</li>
          <li @click="logout">Logout</li>
        </ul>
      </div>
    </header>

    <!-- Bot Overview Box -->
    <div class="bot-overview-box">
      <h2>Meine Bots</h2>
      <div class="grid-container">
        <div
          v-for="(bot, index) in bots"
          :key="index"
          class="bot-card"
        >
          <div class="bot-image">
            <img :src="bot.image || '/default-bot.png'" alt="Bot Image" />
          </div>
          <div class="bot-info">
            <h3>{{ bot.bot_name }}</h3>
            <p>{{ bot.system_prompt }}</p>
            <button @click="downloadBot(bot.bot_name)">Herunterladen</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Bar -->
    <div class="bottom-bar">
      <ul>
        <li>
          <router-link to="/impressum" style="text-decoration: none; display: inline;">
            Impressum
          </router-link>
        </li>
        <li>
          <router-link to="/datenschutz" style="text-decoration: none; display: inline;">
            Datenschutz
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const bots = ref([])
const menuOpen = ref(false)
const user = ref(null)
const router = useRouter()

function openMenu() {
  menuOpen.value = !menuOpen.value
}

async function logout() {
  try {
    await axios.post('/api/logout', {}, { withCredentials: true })
    router.push('/login')
  } catch (err) {
    console.error('Logout failed:', err)
  }
}

async function downloadBot(botName) {
  try {
    const response = await axios.get(`/api/download/${encodeURIComponent(botName)}`, {
      responseType: 'blob',
      withCredentials: true
    })

    const blob = new Blob([response.data])
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${botName.replace(/\s+/g, "_")}_bot_package.zip`
    a.click()
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error("Fehler beim Herunterladen:", err)
    alert("Fehler beim Herunterladen der Datei.")
  }
}

onMounted(async () => {
  try {
    const session = await axios.get('/api/me', { withCredentials: true })
    if (!session.data.user) {
      router.push('/login')
      return
    }

    user.value = session.data.user

    const response = await axios.get('/api/history', { withCredentials: true })
    bots.value = response.data
  } catch (error) {
    console.error('Failed to fetch bots:', error)
    router.push('/login')
  }
})
</script>

<style scoped>
.avatar-icon {
  cursor: pointer;
  padding: 0.5rem 1rem;
  font-weight: bold;
  background-color: #f5f5f5;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.avatar-icon:hover {
  background-color: #e0e0e0;
}

.menu-dropdown {
  list-style: none;
  margin: 0;
  padding: 0;
  background: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  position: absolute;
  right: 1rem;
  top: 60px;
  z-index: 1000;
}

.menu-dropdown li {
  padding: 0.8rem 1.2rem;
  cursor: pointer;
}

.menu-dropdown li:hover {
  background-color: #f0f0f0;
}
</style>
