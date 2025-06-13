<template>
  <div class="create-page-builder">
    <!-- header -->
    <header class="nav-bar">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
      </router-link>
      <div class="user-menu">
        <div class="user-name" @click="openMenu">
          {{ user?.name || 'Lade...' }}
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
        <router-link to="/create" class="nav-button">Bot erstellen</router-link>
        <router-link to="/botoverview" class="nav-button">Meine Bots</router-link>
      </aside>

      <!-- Main Bot Creation Section -->
      <main class="create-container">
        <h2 class="create-title">
          Erstelle deinen<br />personalisierten Chatbot
        </h2>

        <!-- name -->
        <input
          v-model="name"
          type="text"
          class="name-input"
          placeholder="Gib mir einen Namen!"
        />

        <!-- style tags -->
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

        <!-- description box with file upload icon -->
        <div class="desc-box">
          <div class="upload-btn" @click="triggerFileInput">
            <img src="../assets/upload.svg" alt="upload" class="upload-icon" />
            <input
              type="file"
              ref="fileInput"
              @change="handleFileChange"
              style="display: none"
            />
          </div>

          <textarea
            v-model="desc"
            class="desc-input"
            placeholder="Beschreibe deinen Bot…"
          ></textarea>

          <div class="desc-footer">
            <span>Sprachmodell</span>
            <select v-model="model">
              <option value="qwen">Qwen 2.5 0.5B (Standard)</option>
              <option value="phi">Phi</option>
              <option value="deepseek-r1">DeepSeek-R1 7B</option>
              <option value="mistral">Mistral 7B</option>
              <option value="openchat">OpenChat 3.5 / 7B</option>
              <option value="deepseek-v2">DeepSeek V2 16B</option>
            </select>
          </div>
        </div>

        <button class="generate-btn" @click="generate" :disabled="loading">
          Generieren
        </button>

        <div v-if="loading" class="progress-container">
          <div class="progress-bar" :style="{ width: progress + '%' }"></div>
          <p>Datei wird verarbeitet... {{ progress }}%</p>
        </div>

        <div v-if="loading" class="loading-indicator">
          Bot wird erstellt und Datei wird verarbeitet...
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const name = ref("");
const desc = ref("");
const model = ref("qwen");
const menuOpen = ref(false);
const sideBarActive = ref(false);
const loading = ref(false);
const progress = ref(0);
const user = ref(null);
const file = ref(null);
const fileInput = ref(null);
let progressInterval = null;

const tags = ref([
  { label: "Einfache Antworten", selected: true },
  { label: "Lustig", selected: false },
  { label: "Motivierend", selected: false },
  { label: "Detailliert", selected: false },
  { label: "Versichernd", selected: false },
  { label: "Freundlich", selected: false },
  { label: "Professionell", selected: false },
  { label: "Nachvollziehbar", selected: false },
  { label: "Verständig", selected: false },
]);

const router = useRouter();

function openMenu() {
  menuOpen.value = !menuOpen.value;
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

function selectTone(index) {
  tags.value.forEach((tag, i) => {
    tag.selected = i === index;
  });
}

function triggerFileInput() {
  fileInput.value?.click();
}

function handleFileChange(e) {
  file.value = e.target.files[0];
}

async function logout() {
  try {
    await axios.post("/api/logout", {}, { withCredentials: true });
    router.push("/login");
  } catch (err) {
    console.error("Logout fehlgeschlagen:", err);
  }
}

async function generate() {
  const selectedTone = tags.value.find(t => t.selected)?.label || "Professionell";

  const formData = new FormData();
  formData.append("bot_name", name.value);
  formData.append("model_name", model.value);
  formData.append("system_prompt", desc.value);
  formData.append("temperature", "0.7");
  formData.append("context_window", "2048");
  formData.append("tone", selectedTone);
  if (file.value) {
    formData.append("file", file.value);
  }

  loading.value = true;
  progress.value = 0;

  progressInterval = setInterval(() => {
    if (progress.value < 90) {
      progress.value += 5;
    }
  }, 200);

  try {
    const res = await fetch("/api/create", {
      method: "POST",
      body: formData,
    });

    if (res.ok) {
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${name.value.replace(/\s+/g, "_")}_bot_package.zip`;
      a.click();
      window.URL.revokeObjectURL(url);
      progress.value = 100;
    } else {
      const errorText = await res.text();
      alert("❌ Fehler: " + errorText);
    }
  } catch (err) {
    console.error("❌ Fehler beim Erstellen des Bots:", err);
    alert("❌ Unerwarteter Fehler beim Erstellen des Bots.");
  } finally {
    clearInterval(progressInterval);
    loading.value = false;
  }
}

onMounted(async () => {
  try {
    const session = await axios.get("/api/me", { withCredentials: true });
    if (!session.data.user) {
      router.push("/login");
      return;
    }
    user.value = session.data.user;
  } catch (error) {
    console.error("Fehler beim Laden der Seite:", error);
    router.push("/login");
  }
});
</script>
