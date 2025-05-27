<template>
  <div class="bot-overview-page">
    <!-- Header -->
    <header class="nav-bar">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
      </router-link>
      <div class="user-menu">
        <div class="avatar-icon" @click="openMenu">
          <img src="../assets/avatar.svg" alt="Avatar" class="user-icon" />
        </div>
        <ul v-if="menuOpen" class="menu-dropdown">
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
import axios from 'axios'

const bots = ref([])
const menuOpen = ref(false)

function openMenu() {
  menuOpen.value = !menuOpen.value
}

function logout() {
  // your logout logic
  console.log('Logging out...')
}

onMounted(async () => {
  try {
    const response = await axios.get('/api/history')
    bots.value = response.data
  } catch (error) {
    console.error('Failed to fetch bots:', error)
  }
})
</script>
