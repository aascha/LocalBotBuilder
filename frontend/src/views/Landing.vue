<template>
  <div class="wrapper">
    <!-- Top navigation bar -->
    <header class="nav-bar">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
      </router-link>
      <div class="user-menu" v-if="user">
        <div class="user-name" @click="openMenu">
          {{ user.name }}
        </div>
        <ul v-if="menuOpen" class="menu-dropdown">
          <li @click="logout">Logout</li>
        </ul>
      </div>
      <div class="nav-buttons" v-else>
        <button class="nav-btn light" @click="goToLogin">Anmelden</button>
        <button class="nav-btn dark" @click="goToRegister">Registrieren</button>
      </div>
    </header>


    <!-- Main content -->
    <main class="container">
      <!-- Logo + Title -->
      <div class="logo-box">
        <h1 class="logo-title">Local Bot Builder</h1>
        <img :src="logo" alt="Logo" class="logo-icon" />
      </div>

      <!-- Big Main Heading -->
      <h2 class="main-title">
        Erstelle deinen lokalen<br />
        Assistenten.
      </h2>

      <!-- Subtitle -->
      <p class="subtitle">
        Baue einen eigenen lokalen Chatbot, der dir bei deinen Fragen hilft und
        dir immer zur Seite steht.
      </p>

      <!-- Call to Action -->
      <button class="cta-button" @click="goToRegister">
        Erstelle deinen Chatbot
      </button>
    </main>

    <footer class="footer">
      <router-link to="/impressum" class="footer-link">Impressum</router-link>
      <router-link to="/datenschutz" class="footer-link">Datenschutz</router-link>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import logo from "../logo.jpg";

const router = useRouter();
const user = ref(null);
const menuOpen = ref(false); // <--- Add this

function openMenu() {         // <--- And this
  menuOpen.value = !menuOpen.value;
}


onMounted(async () => {
  try {
    const res = await axios.get("/api/me", { withCredentials: true });
    user.value = res.data.user;
  } catch (error) {
    console.error("Fehler beim Abrufen des Benutzers:", error);
  }
});

function goToLogin() {
  router.push("/login");
}

function goToRegister() {
  router.push("/register");
}

async function goToQuestionnaire() {
  try {
    const res = await axios.get("/api/me", { withCredentials: true });
    if (res.data.user) {
      router.push("/create"); 
    } else {
      router.push("/questionnaire1"); 
    }
  } catch (err) {
    router.push("/questionnaire1");
  }
}

async function logout() {
  try {
    await axios.post("/api/logout", {}, { withCredentials: true });
    user.value = null;
    router.push("/login");
  } catch (err) {
    console.error("Logout fehlgeschlagen:", err);
  }
}
</script>
