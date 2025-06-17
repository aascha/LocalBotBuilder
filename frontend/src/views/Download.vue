<template>
  <div class="create-page-builder">
    <!-- header -->
    <header class="nav-bar">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
      </router-link>

      <div class="user-menu">
        <div class="user-name" @click="toggleMenu">
          {{ user?.name || "Logout" }}
        </div>
        <ul v-if="menuOpen" class="menu-dropdown">
          <li @click="logout">Logout</li>
        </ul>
      </div>
    </header>

    <!-- Sidebar -->
    <div class="side-main-wrapper">
      <aside id="sidebar" class="sidebar">
        <div>
          <img
            src="../assets/sidebar-icon.svg"
            class="sidebar-icon"
            alt="Menu"
            @click.stop="toggleSidebar"
          />
        </div>
        <router-link
          to="/create"
          class="nav-button"
          :class="{ active: route.path === '/create' }"
          >Bot erstellen</router-link
        >

        <router-link
          to="/botoverview"
          class="nav-button"
          :class="{ active: route.path === '/botoverview' }"
          >Meine Bots</router-link
        >

        <router-link
          to="/download"
          class="nav-button"
          :class="{ active: route.path === '/download' }"
          >Downloads</router-link
        >
      </aside>

      <!-- main form -->
      <main class="setup-container">
        <h2 class="create-title">Setup-Guide</h2>

        <div class="setup-guide">
          <h3>Docker Installieren</h3>
          <span>
            Lade Docker herunter und installiere es auf deinem System. Ohne
            Docker funktioniert die App nicht.
            <a
              href="https://www.docker.com/"
              target="_blank"
              rel="noopener"
              style="color: #0076a2; text-decoration: underline"
              >Offizielle Docker-Website</a
            >.
            <br />
            <br />
          </span>
          <h3>Chatbot-App herunterlanden</h3>
          <span>
            Lade dir über den Button am Ende der Seite unsere App herunter.
            Entpacke das Zip-File in einen belibigen ordner und öffne
            "Start.exe" um Sie zu Installieren.
            <br />
            <br />
          </span>
          <h3>Konfiguriere deinen persönlichen Bot</h3>
          <span>
            Benutze unseren Bot Konfigurator, um die richtige für dein System zu
            finden und ihr eine Persönlichkeit zu verpassen.
            <router-link
              to="/questionnaire1"
              class="config-link"
              style="color: #0076a2; text-decoration: underline"
              >Bot-Konfigurator</router-link
            >
            <br />
            <br />
          </span>
          <h3>Platziere den Bot im Container und Starte die App</h3>
          <span>
            Öffne den Ordner deiner heruntergeladenen App und gehe in dieses
            Verzeichnis: <br />
            <code>chat → generated_bots</code><br />
            Lege dort dein <strong>Bot-Modell-File</strong> ab und starte die
            App neu. Viel Erfolg!
            <br />
            <br />
          </span>
          <button class="generate-btn" @click="download">Download</button>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.user-name {
  font-weight: bold;
  color: #0076a2;
  cursor: pointer;
  padding: 10px 20px;
  border: 1px solid #83deff;
  border-radius: 20px;
  background-color: #e0f7ff;
  transition: background-color 0.3s;
}

.user-name:hover {
  background-color: #bdf0ff;
}

.setup-container {
  margin: 3rem 5rem;
}
</style>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useRoute } from "vue-router";
const route = useRoute();

const menuOpen = ref(false);
const sideBarActive = ref(false);
const user = ref(null);

const router = useRouter();

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

async function logout() {
  try {
    await axios.post("/api/logout", {}, { withCredentials: true });
  } catch (e) {
    console.error("Logout error:", e);
  }
  router.push("/login");
}

function download() {
  alert("Download feature not implemented yet.");
}

function toggleSidebar() {
  sideBarActive.value = !sideBarActive.value;
  const sidebar = document.getElementById("sidebar");
  if (sidebar) {
    sidebar.classList.toggle("active", sideBarActive.value);
  }
}

onMounted(async () => {
  try {
    const session = await axios.get("/api/me", { withCredentials: true });
    user.value = session.data.user;
  } catch (e) {
    console.error("Failed to fetch user:", e);
    router.push("/login");
  }
});
</script>
