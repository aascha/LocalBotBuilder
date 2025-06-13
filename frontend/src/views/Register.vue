<template>
  <div class="login-page">
    <!-- Top navigation bar -->
    <header class="nav-bar">
      <router-link to="/">
        <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
      </router-link>
      <button class="nav-btn light" @click="goToLogin">Anmelden</button>
    </header>

    <!-- Registration Form Box -->
    <div class="login-box">
      <h2>Registriere dich</h2>
      <form @submit.prevent="handleRegister">
        <label for="name">Vollständiger Name</label>
        <input
          id="name"
          type="text"
          placeholder="Max Mustermann"
          v-model="name"
        />

        <label for="email">E-Mail-Adresse</label>
        <input
          id="email"
          type="email"
          placeholder="email@example.de"
          v-model="email"
        />

        <label for="password">Passwort</label>
        <input
          id="password"
          type="password"
          placeholder="**********"
          v-model="password"
        />

        <label for="confirmPassword">Passwort bestätigen</label>
        <input
          id="confirmPassword"
          type="password"
          placeholder="**********"
          v-model="confirmPassword"
        />

        <p v-if="error" class="error-msg">{{ error }}</p>

        <button type="submit" class="cta-button">Registrieren</button>
      </form>

      <p class="small-link">
        Du hast bereits ein Konto?
        <a href="#" @click.prevent="goToLogin">Anmelden</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')

const router = useRouter()

onMounted(async () => {
  try {
    const res = await axios.get('/api/me', { withCredentials: true })
    if (res.data.user) {
      router.push('/questionnaire1')
    }
  } catch (err) {
    console.error('Fehler beim Session-Check:', err)
  }
})

async function handleRegister() {
  error.value = ''

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwörter stimmen nicht überein.'
    return
  }

  try {
    const response = await axios.post('/api/register', {
      name: name.value,
      email: email.value,
      password: password.value
    })

    if (response.data.message) {
      // ✅ Set 'user' in localStorage and redirect to questionnaire
      localStorage.setItem('user', 'true')
      router.push('/questionnaire1')
    }
  } catch (err) {
    if (err.response && err.response.data?.error) {
      error.value = err.response.data.error
    } else {
      error.value = 'Ein unbekannter Fehler ist aufgetreten.'
    }
  }
}

function goToLogin() {
  router.push('/login')
}
</script>
