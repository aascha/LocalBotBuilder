<template>
  <div class="login-page">
    <!-- Top navigation bar -->
    <header class="nav-bar">
      <img
        src="../assets/logo_full.svg"
        alt="Logo"
        class="top-logo"
        @click="goToLanding"
      />
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
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const email = ref("");
const password = ref("");
const error = ref(false);

import axios from "axios";

async function handleLogin() {
  error.value = false;

  try {
    const res = await axios.post(
      "/api/login",
      {
        email: email.value,
        password: password.value,
      },
      {
        withCredentials: true, // 🔑 Needed for Flask session cookies
      }
    );

    if (res.status === 200) {
      router.push("/create"); // ✅ Redirect to a logged-in page
    } else {
      error.value = true;
    }
  } catch (err) {
    console.error("Login error:", err);
    error.value = true;
  }
}


function goToRegister() {
  router.push("/register");
}

function goToLanding() {
  router.push("/");
}
</script>
