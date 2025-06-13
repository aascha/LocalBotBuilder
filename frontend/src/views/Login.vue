<template>
  <div class="login-page">
    <!-- Top navigation bar -->
    <header class="nav-bar">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
      </router-link>
      <button class="nav-btn dark" @click="goToRegister">Registrieren</button>
    </header>

    <!-- Login Form Box -->
    <div class="login-box">
      <h2>Willkommen zurück</h2>
      <form @submit.prevent="handleLogin">
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

        <p v-if="error" class="error-msg">{{ error }}</p>

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
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const email = ref("");
const password = ref("");
const error = ref("");

onMounted(async () => {
  try {
    const res = await axios.get("/api/me", { withCredentials: true });
    if (res.data.user) {
      router.push("/create");
    }
  } catch (err) {
    console.error("Fehler beim Session-Check:", err);
  }
});

async function handleLogin() {
  error.value = "";

  try {
    const response = await axios.post(
      "/api/login",
      {
        email: email.value,
        password: password.value,
      },
      {
        withCredentials: true,
      }
    );

    if (response.data.message) {
      // ✅ Set 'user' in localStorage after successful login
      localStorage.setItem('user', 'true');
      router.push("/create");
    }
  } catch (err) {
    error.value = "Login fehlgeschlagen. Bitte überprüfe deine Daten.";
  }
}

function goToRegister() {
  router.push("/register");
}
</script>
