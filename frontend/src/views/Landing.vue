<template>
  <div class="wrapper">
    <!-- Top navigation buttons -->
    <header class="nav-bar">
      <div></div> <!-- spacer -->
      <div class="nav-buttons">
        <template v-if="user">
          <div class="username-label" @click="toggleMenu">{{ user.name }}</div>
          <ul v-if="menuOpen" class="menu-dropdown">
            <li @click="logout">Logout</li>
          </ul>
        </template>
        <template v-else>
          <button class="nav-btn light" @click="goToLogin">Anmelden</button>
          <button class="nav-btn dark" @click="goToRegister">Registrieren</button>
        </template>
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
      <button class="cta-button" @click="goToQuestionnaire">
        Erstelle deinen Chatbot
      </button>
    </main>

    <footer class="footer">
      <router-link to="/impressum" class="footer-link">Impressum</router-link>
      <router-link to="/datenschutz" class="footer-link"
        >Datenschutz</router-link
      >
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
const menuOpen = ref(false);

function goToLogin() {
  router.push("/login");
}

function goToRegister() {
  router.push("/register");
}

async function goToBuilder() {
  try {
    const res = await axios.get("/api/me", { withCredentials: true });
    const completed = res.data?.user?.questionnaire_completed;

    if (completed) {
      router.push("/create");
    } else {
      router.push("/questionnaire"); // make sure this route exists
    }
  } catch (err) {
    console.error("Fehler beim Überprüfen des Fragebogens:", err);
    alert("Bitte erneut einloggen.");
    router.push("/login");
  }
}


async function goToQuestionnaire() {
  try {
    const res = await axios.get("/api/me", { withCredentials: true });

    if (res.data?.user) {
      const completed = res.data.user.questionnaire_completed;
      if (completed) {
        router.push("/create");  // ✅ Skip questionnaire if already done
      } else {
        router.push("/questionnaire1"); // 👈 Only for first-time
      }
    } else {
      router.push("/login"); // Not logged in
    }
  } catch (err) {
    console.error("Fehler beim Laden des Users:", err);
    router.push("/login");
  }
}



function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

async function logout() {
  menuOpen.value = false;
  try {
    await axios.post("/api/logout", {}, { withCredentials: true });
    user.value = null;
    router.push("/login");
  } catch (err) {
    console.error("Logout failed:", err);
  }
}

// check if user is logged in
onMounted(async () => {
  try {
    const res = await axios.get("/api/me", { withCredentials: true });
    if (res.data?.user) user.value = res.data.user;
  } catch (err) {
    console.warn("No user session.");
  }
});
</script>
