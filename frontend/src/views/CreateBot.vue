<template>
  <div class="create-page-builder">
    <!-- header -->
    <header class="nav-bar">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
      </router-link>
      <div class="user-menu">
        <div class="avatar-icon" @click="openMenu">
          <font-awesome-icon
            icon="circle-user"
            class="user-icon"
            @click="Logout"
          />
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
          <font-awesome-icon
            icon="list"
            class="list-icon"
            @click.stop="toggleSidebar"
          />
        </div>
        <button class="nav-button">Bot erstellen</button>
        <button class="nav-button">Meine Bots</button>
      </aside>

      <!-- main form -->
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

        <!-- description box -->
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
            <span>Erfahrungslevel</span>
            <select v-model="model">
              <option value="gpt-4o">GPT-4o</option>
              <option value="claude">Claude-Sonnet-3.7</option>
              <option value="gemini">Gemini-Pro</option>
              <option value="grok">Grok</option>
              <option value="deepseek">DeepSeek V3</option>
              <option value="llama">Meta Llama 3.3</option>
            </select>
          </div>
        </div>

        <!-- generate button -->
        <button class="generate-btn" @click="generate" :disabled="loading">
          Generieren
        </button>

        <!-- loading indicator -->
        <div v-if="loading" class="loading-indicator">
          ⏳ Bot wird erstellt und Datei wird verarbeitet...
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const name = ref("");
const desc = ref("");
const model = ref("gpt-4o");
const menuOpen = ref(false);
const sideBarActive = ref(false);
const loading = ref(false);

const tags = ref([
  { label: "Einfache Antworten", selected: true },
  { label: "Lustig", selected: false },
  { label: "Motivierend", selected: false },
  { label: "Detailliert", selected: false },
  { label: "Versichernd", selected: false },
  { label: "...", selected: false },
  { label: "Freundlich", selected: false },
  { label: "Professionell", selected: false },
  { label: "Nachvollziehbar", selected: false },
  { label: "Verständig", selected: false },
]);

function selectTone(index) {
  tags.value.forEach((tag, i) => {
    tag.selected = i === index;
  });
}

const router = useRouter();
function openMenu() {
  menuOpen.value = !menuOpen.value;
}
function logout() {
  router.push("/login");
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

  try {
    const res = await fetch("/api/create", {
      method: "POST",
      body: formData,
    });

    const text = await res.text();
    alert(text);
    console.log("✅ Flask response:", text);

    router.push("/chat");
  } catch (err) {
    console.error("❌ Error creating bot:", err);
    alert("❌ Fehler beim Erstellen des Bots.");
  } finally {
    loading.value = false;
  }
}

const file = ref(null);
const fileInput = ref(null);

function triggerFileInput() {
  fileInput.value?.click();
}

function handleFileChange(e) {
  file.value = e.target.files[0];
  console.log("📁 Selected file:", file.value?.name);
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
</script>
