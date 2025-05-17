<template>
  <div class="login-page">
    <!-- Top navigation bar -->
    <header class="nav-bar">
      <img src="../logo_full.png" alt="Logo" class="top-logo" />
      <button class="nav-btn dark" @click="goToRegister">Registrieren</button>
    </header>

    <!-- Login Form Box -->
    <div class="login-box">
      <h2>Willkommen zurück</h2>
      <form @submit.prevent="handleLogin">
        <label for="email">E-Mail-Adresse</label>
        <input id="email" type="email" placeholder="email@example.de" v-model="email" />

        <label for="password">Passwort</label>
        <input id="password" type="password" placeholder="**********" v-model="password" />

        <p v-if="error" class="error-msg">
          E-Mail oder Passwort wurden inkorrekt eingegeben.
        </p>

        <button type="submit" class="cta-button">Anmelden</button>
      </form>
      <p class="small-link">
        Du hast noch kein Konto? 
        <a href="#" @click.prevent="goToRegister">Registrieren</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref(false)

function handleLogin() {
  error.value = true // For demonstration, always show error
}

function goToRegister() {
  router.push('/register')
}
</script>


  