<template>
  <div class="bot-overview-page">
    <!-- header -->
    <header class="nav-bar">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
      </router-link>

      <div class="user-menu">
        <div class="username-label" @click="toggleMenu">
          {{ username }}
        </div>
        <ul v-if="menuOpen" class="menu-dropdown">
          <li @click="logout">Logout</li>
        </ul>
      </div>
    </header>

    <div class="side-main-wrapper">
      <!-- Sidebar -->
      <aside id="sidebar" class="sidebar">
        <div>
          <img
            src="../assets/sidebar-icon.svg"
            class="sidebar-icon"
            alt="Menu"
            @click.stop="toggleSidebar"
          />
        </div>
        <button
          class="nav-button"
          :class="{ active: isActive('/create') }"
          @click="goToBuilder"
        >
          Bot erstellen
        </button>
        <button
          class="nav-button"
          :class="{ active: isActive('/botoverview') }"
          @click="goToBots"
        >
          Meine Bots
        </button>
        <button
        class="nav-button"
        :class="{ active: isActive('/download') }"
        @click="goToDownloads"
      >
        Downloads
      </button>
      </aside>

      <main class="main-content">
        <!-- Bot Overview Box -->
        <div class="bot-overview-box">
          <h2>Meine Bots</h2>
          <div class="grey-line"></div>
          <div class="grid-container">
            <div
              v-for="(bot, index) in bots"
              :key="bot.id"
              :class="`bot-card bot-card-${(index % 6) + 1}`"
              @click="goToEditor(bot.id)"
            >
            <img
              class="bot-image"
              :src="bot.image_url"
              alt="Bot Icon"
            />
              <div class="bot-info">
                <h3>{{ bot.bot_name }}</h3>
                <p><strong>Modell:</strong> {{ bot.model_name }}</p>
                <p class="prompt-snippet">
                  {{ bot.system_prompt?.slice(0, 100) }}<span v-if="bot.system_prompt?.length > 100">...</span>
                </p>

              </div>
              <button class="download-bot-btn" @click.stop="downloadBot(bot.bot_name)">
                  Herunterladen
                </button>
            </div>
          </div>
        </div>
      </main>
    </div>

    <div class="bottom-bar">
      <ul>
        <li>
          <router-link to="/impressum" style="text-decoration: none; display: inline">Impressum</router-link>
        </li>
        <li>
          <router-link to="/datenschutz" style="text-decoration: none; display: inline">Datenschutz</router-link>
        </li>
      </ul>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";

const router = useRouter();
const route = useRoute();

const sideBarActive = ref(false);
const menuOpen = ref(false);
const bots = ref([]);
const username = ref("Lade...");

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}
function goToDownloads() {
  router.push("/download");
}


async function logout() {
  try {
    await axios.post("/api/logout", {}, { withCredentials: true });
    router.push("/login");
  } catch (err) {
    console.error("Logout fehlgeschlagen:", err);
    alert("Logout fehlgeschlagen.");
  }
}

function goToLanding() {
  router.push("/");
}

function goToBuilder() {
  router.push("/create");
}

function goToBots() {
  router.push("/botoverview");
}

function goToEditor(botId) {
  router.push(`/boteditor?id=${botId}`);
}

function toggleSidebar() {
  sideBarActive.value = !sideBarActive.value;
  const sidebar = document.getElementById("sidebar");
  if (sideBarActive.value) {
    sidebar.classList.add("active");
  } else {
    sidebar.classList.remove("active");
  }
}

function isActive(path) {
  return route.path === path;
}

async function downloadBot(name) {
  try {
    const encoded = encodeURIComponent(name);
    const url = `/api/download/${encoded}`;

    const check = await fetch(url, { method: 'HEAD' });
    if (!check.ok) {
      alert("❌ Datei ist nicht bereit. Stelle sicher, dass du Änderungen gespeichert hast.");
      return;
    }

    const res = await fetch(url);
    const blob = await res.blob();
    const fileUrl = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = fileUrl;
    a.download = `${encoded}_bot_package.zip`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(fileUrl);
  } catch (err) {
    console.error("Fehler beim Herunterladen:", err);
    alert("❌ Download fehlgeschlagen.");
  }
}



// Fetch bots + user info
onMounted(async () => {
  try {
    const [botRes, userRes] = await Promise.all([
      axios.get("/api/history", { withCredentials: true }),
      axios.get("/api/me", { withCredentials: true }),
    ]);

    bots.value = botRes.data;
    username.value = userRes.data?.user?.name || "Benutzer";
  } catch (err) {
    console.error("Fehler beim Laden der Seite:", err);
    router.push("/login");
  }
});
</script>

<style scoped>

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
}
</style>