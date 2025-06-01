<template>
    <div class="login-page">
      <!-- Top navigation bar -->
      <header class="nav-bar">
      <!-- Logo navigates to landing -->
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
  
          <!-- Error message (always shown for now) -->
          <p v-if="error" class="error-msg">
            {{ error }}
          </p>

  
          <!-- Submit button -->
          <button type="submit" class="cta-button">Registrieren</button>
        </form>
  
        <!-- Link to switch back to Login -->
        <p class="small-link">
          Du hast bereits ein Konto?
          <a href="#" @click.prevent="goToLogin">Anmelden</a>
        </p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  
  const name = ref('')
  const email = ref('')
  const password = ref('')
  const confirmPassword = ref('')
  const error = ref(false)
  
  const router = useRouter()
  
  // For now, always show error when submitting registration
import axios from 'axios'

async function handleRegister() {
  error.value = false

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
      router.push('/login') // Redirect on success
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.error) {
      error.value = err.response.data.error
    } else {
      error.value = 'Ein unbekannter Fehler ist aufgetreten.'
    }
  }
}

  
  // Navigate to the login page
  function goToLogin() {
    router.push('/login')
  }
  </script>
  