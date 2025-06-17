<template>
  <div class="create-page-builder">
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
      <aside id="sidebar" class="sidebar">
        <div>
          <img
            src="../assets/sidebar-icon.svg"
            class="sidebar-icon"
            alt="Menu"
            @click.stop="toggleSidebar"
          />
        </div>
        <button class="nav-button" :class="{ active: isActive('/create') }">
          Bot erstellen
        </button>
        <button class="nav-button" :class="{ active: isActive('/botoverview') }" @click="goToBots">
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

      <main class="create-container">
        <h2 class="create-title">
          Erstelle deinen<br />personalisierten Chatbot
        </h2>

        <input
          v-model="name"
          type="text"
          class="name-input"
          placeholder="Gib mir einen Namen!"
        />

        <div class="tag-row">
          <button
            v-for="(t, i) in tags"
            :key="i"
            :class="{ selected: t.selected }"
            class="tag-btn"
            @click="selectTone(i)"
          >
            {{ t.label }}
          </button>
        </div>

        <div class="desc-box">
          <textarea
            v-model="desc"
            class="desc-input"
            placeholder="Beschreibe deinen Bot…"
          ></textarea>

          <div class="desc-footer">
            <span>Sprachmodell</span>
            <select v-model="model">
              <option value="qwen">Qwen 2.5 0.5B (Standard)</option>
              <option value="mistral">Mistral:7B</option>
              <option value="llama">Llama3:8B</option>
            </select>
          </div>
        </div>

        <button class="generate-btn" @click="generate">Generieren</button>
      </main>
    </div>
  </div>
  <!-- Success Notification -->
    <div v-if="showSuccess" class="success-popup">
      <p>Bot erfolgreich erstellt!</p>
      <button @click="downloadGeneratedBot" class="download-button-popup">
        Bot herunterladen
      </button>
    </div>

</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";

const name = ref("");
const desc = ref("");
const model = ref("qwen");
const menuOpen = ref(false);
const sideBarActive = ref(false);
const username = ref("Benutzer");

const router = useRouter();
const route = useRoute();

const showSuccess = ref(false);
const lastBotName = ref("");


const tags = ref([
  { label: "Einfache Antworten", selected: true },
  { label: "Lustig" },
  { label: "Motivierend" },
  { label: "Detailliert" },
  { label: "Versichernd" },
  { label: "Freundlich" },
  { label: "Professionell" },
  { label: "Nachvollziehbar" },
  { label: "Verständig" },
]);

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
    console.error("Logout failed:", err);
    alert("Logout fehlgeschlagen.");
  }
}


function goToBots() {
  router.push("/botoverview");
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

function selectTone(index) {
  tags.value.forEach((tag, i) => {
    tag.selected = i === index;
  });
}

async function generate() {
  try {
    const selectedTone = tags.value.find((t) => t.selected)?.label || "Einfache Antworten";

    const formData = new FormData();
    formData.append("bot_name", name.value);
    formData.append("system_prompt", desc.value);
    formData.append("model_name", model.value);
    formData.append("temperature", "0.7");
    formData.append("context_window", "2048");
    formData.append("tone", selectedTone);

    // 🆕 Attach default icon
    const defaultIcon = await fetch(new URL("../assets/default-bot-icon.jpg", import.meta.url)).then(r => r.blob());
    formData.append("icon", new File([defaultIcon], "default-bot-icon.jpg", { type: "image/png" }));

    await axios.post("/api/create", formData, {
      withCredentials: true,
    });

    router.push("/botoverview");
  } catch (err) {
    console.error("Bot creation failed:", err);
  }
}


async function downloadGeneratedBot() {
  try {
    const encodedName = encodeURIComponent(lastBotName.value);
    const res = await fetch(`/api/download/${encodedName}`);
    if (!res.ok) return alert("Download fehlgeschlagen.");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${lastBotName.value.replace(/\s+/g, "_")}_bot_package.zip`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    showSuccess.value = false;
  } catch (err) {
    console.error("Fehler beim Herunterladen:", err);
    alert("Download fehlgeschlagen.");
  }
}


onMounted(async () => {
  try {
    const res = await axios.get("/api/me", { withCredentials: true });
    username.value = res.data?.user?.name || "Benutzer";
  } catch (err) {
    console.warn("Could not load username:", err);
  }
});
</script>

<style scoped>
.success-popup {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #ffffff;
  border-left: 6px solid #4caf50;
  color: #2e7d32;
  padding: 1rem 2rem;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 999;
  animation: fadeInUp 0.3s ease-out;
  min-width: 320px;
}

.download-button-popup {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.download-button-popup:hover {
  background-color: #388e3c;
}

@keyframes fadeInUp {
  from {
    transform: translateX(-50%) translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateX(-50%) translateY(0);
    opacity: 1;
  }
}
</style>
