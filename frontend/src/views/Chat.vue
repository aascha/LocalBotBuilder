<template>
  <div class="chat-page">
    <!-- ================= Header ================= -->
    <header class="nav-bar">
      <router-link to="/" class="logo-link">
        <img src="../assets/chatbot_logo.svg" alt="Logo" class="top-logo-chatbot" />
      </router-link>
    </header>

    <!-- ================ Body (Sidebar + Chat) ================ -->
    <div class="chat-container">
      <!-- ===== Sidebar (Verlauf) ===== -->
      <aside class="chat-history">
        <div class="history-header">
          <h3>Verlauf</h3>
          <button class="new-session-btn" @click="createNewSession">
            + Neue Unterhaltung
          </button>
        </div>

        <ul>
          <li
            v-for="(session, idx) in sessions"
            :key="idx"
            :class="{ 'session-active': idx === activeSessionIndex }"
            @click="loadSession(idx)"
          >
            <!-- Display first user message or “Neue Unterhaltung” if empty -->
            <div class="session-title">
              {{ sessionTitle(session) }}
            </div>
            <!-- Show small snippet of last message -->
            <div class="session-snippet">
              {{ lastSnippet(session) }}
            </div>
          </li>
        </ul>
      </aside>

      <!-- ===== Chat Main Area ===== -->
      <section class="chat-main">
        <!-- If no active session, prompt to create one -->
        <div v-if="activeSessionIndex === null" class="no-session">
          <p>Wähle eine Unterhaltung oder erstelle eine neue.</p>
        </div>
        <!-- Otherwise show messages for active session -->
        <div v-else class="chat-content">
          <ul class="messages">
            <li v-for="(m, i) in currentMessages" :key="i" :class="m.sender">
              {{ m.text }}
            </li>
          </ul>

          <!-- Chat Input Row -->
          <div class="chat-input-wrapper">
            <!-- Upload (placeholder) -->
            <button class="chat-btn upload" @click="onUpload">
              <font-awesome-icon
                :icon="['fas', 'circle-arrow-up']"
                class="chat-btn"
              />
            </button>

            <input
              v-model="userInput"
              type="text"
              class="chat-input"
              placeholder="Stelle mir eine Frage…"
              @keyup.enter="sendQuestion"
            />

            <!-- Send button -->
            <button class="chat-btn send" @click="sendQuestion">
              <font-awesome-icon
                :icon="['fas', 'circle-arrow-right']"
                class="chat-btn"
              />
            </button>
            <div class="model-select" @change="updateModel">
              <span>Sprachmodell</span>
              <select v-model="model">
                <option value="qwen">Qwen 2.5 0.5B (Standard)</option>
                <option value="phi">Phi</option>
                <option value="deepseek-r1">DeepSeek-R1 7B</option>
              </select>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { useModelStore } from "../store";

// --- Router & Avatar menu ---
const router = useRouter();
const menuOpen = ref(false);
const store = useModelStore();
const model = ref("qwen"); // Default model
const modelOptions = [
  { value: "qwen", label: "Qwen 2.5 0.5B (Standard)" },
  { value: "phi", label: "Phi" },
  { value: "deepseek-r1", label: "DeepSeek-R1 7B" },
];
const selectedModel = ref(model.value);
function updateModel() {
  selectedModel.value = model.value;
  store.setModel(selectedModel.value);
  // TODO: Call AI API with the selected model
  console.log(`Model changed to: ${model.value}`);
}

// --- Sessions & Messages ---
// Each session = { messages: [{ sender: 'bot'|'user', text: '…' }, …] }
const sessions = ref([
  // Start with one empty session (you can remove if you prefer starting blank)
  {
    messages: [
      { sender: "bot", text: "Hi, ich bin dein Bot! Wie kann ich helfen?" },
    ],
  },
]);

// Index of the currently active session, or null if none
const activeSessionIndex = ref(0);

// Convenience: get messages of the active session
const currentMessages = computed(() => {
  if (activeSessionIndex.value === null) return [];
  return sessions.value[activeSessionIndex.value].messages;
});

// --- User input state ---
const userInput = ref("");

// Create a brand-new (empty) session and make it active
function createNewSession() {
  sessions.value.push({
    messages: [
      { sender: "bot", text: "Hi, ich bin dein Bot! Wie kann ich helfen?" },
    ],
  });
  activeSessionIndex.value = sessions.value.length - 1;
  userInput.value = "";
}

// Load a given session index into the main view
function loadSession(idx) {
  activeSessionIndex.value = idx;
  userInput.value = "";
}

// Handle sending a question
function sendQuestion() {
  const q = userInput.value.trim();
  if (!q || activeSessionIndex.value === null) return;

  // Add user message
  sessions.value[activeSessionIndex.value].messages.push({
    sender: "user",
    text: q,
  });

  // Fake bot response (replace with real API call)
  const fakeAnswer = `Antwort auf "${q}"`;
  sessions.value[activeSessionIndex.value].messages.push({
    sender: "bot",
    text: `Bot: ${fakeAnswer}`,
  });

  userInput.value = "";
}

// Placeholder upload action
function onUpload() {
  alert("Upload-Funktion noch nicht implementiert.");
}

// --- Sidebar Helper Functions ---
// Show first user line as title, or “Neue Unterhaltung” if no user yet
function sessionTitle(session) {
  const firstUser = session.messages.find((m) => m.sender === "user");
  return firstUser ? `User: ${firstUser.text}` : "Neue Unterhaltung";
}

// Show snippet (last message) in smaller font
function lastSnippet(session) {
  const lastMsg = session.messages[session.messages.length - 1];
  if (!lastMsg) return "";
  return `${lastMsg.sender === "user" ? "User" : "Bot"}: ${lastMsg.text}`;
}
</script>

<script>
export default {
  components: {
    FontAwesomeIcon,
  },
};
</script>

<style scoped>
/* ==================== Entire Page ==================== */
.chat-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f9fafb;
}

/* ==================== Header ==================== */
.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.logo-link img.top-logo {
  height: 40px;
  object-fit: contain;
}

.avatar-icon {
  position: relative;
  cursor: pointer;
}

.user-icon {
  font-size: 1.6rem;
  color: #38bdf8;
}

.menu-dropdown {
  position: absolute;
  top: 2.5rem;
  right: 0;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  list-style: none;
  margin: 0;
  padding: 0.5rem 0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.menu-dropdown li {
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.menu-dropdown li:hover {
  background: #f1f5f9;
}
/* ==================== Body Layout ==================== */
.chat-container {
  display: flex;
  flex: 1;
  padding: 1rem 0.5rem;
}

/* ==================== Sidebar (Verlauf) ==================== */
.chat-history {
  width: 280px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 1rem;
  margin-right: 1rem;
  overflow-y: auto;
  max-height: 85vh;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.history-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #0369a1;
}

.new-session-btn {
  background: #38bdf8;
  border: none;
  color: white;
  padding: 0.3rem 0.6rem;
  font-size: 0.9rem;
  border-radius: 4px;
  cursor: pointer;
}

.new-session-btn:hover {
  background: #0ea5e9;
}

.chat-history ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.chat-history li {
  cursor: pointer;
  margin-bottom: 0.75rem;
  padding: 0.6rem;
  border-radius: 8px;
  background: #f5faff;
  transition: background 0.2s;
}

.chat-history li:hover,
.chat-history li.session-active {
  background: #e0f2fe;
}

.session-title {
  font-weight: bold;
  color: #0369a1;
  margin-bottom: 0.25rem;
}

.session-snippet {
  font-size: 0.9rem;
  color: #475569;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ==================== Chat Main ==================== */
.chat-main {
  flex: 1;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  position: relative; /* Needed for absolute positioning */
  min-height: 400px;
}

/* When no session is chosen */
.no-session {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  font-size: 1.2rem;
}

/* ==================== Messages ==================== */
.messages {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 60vh;
  overflow-y: auto;
}

.messages .user {
  align-self: flex-end;
  background: #cfeffd;
  color: #0c4a6e;
  padding: 0.6rem 1rem;
  border-radius: 16px 16px 0 16px;
  max-width: 70%;
  word-break: break-word;
}

.messages .bot {
  align-self: flex-start;
  background: #f1f5f9;
  color: #0f172a;
  padding: 0.6rem 1rem;
  border-radius: 16px 16px 16px 0;
  max-width: 70%;
  word-break: break-word;
}

.chat-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

/* ==================== Chat Input Row ==================== */
.chat-input-wrapper {
  position: absolute;
  bottom: 1.5rem; /* Match .chat-main's padding */
  left: 1.5rem;
  right: 1.5rem;
  display: flex;
  flex-direction: row;
  border: 2px solid #38bdf8;
  border-radius: 2rem;
  padding: 0.25rem;
  background-color: white;
  /* Prevent children from inheriting border-radius */
  overflow: hidden;
}

.chat-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1rem;
  padding: 0.75rem 1rem;
  background: transparent;
  border-radius: 0;
}

.model-select {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 0.5rem;
  position: relative;
  align-self: auto;
}

.chat-btn {
  border-radius: 50%; /* Makes buttons perfectly round */
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 0.5rem;
}

.chat-btn.upload {
  color: #ffffff;
  background-color: #38bdf8;
}

.chat-btn.send {
  color: #ffffff;
  background-color: #38bdf8;
}
</style>
