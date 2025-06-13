<template>
  <div class="chat-page">
    <!-- header -->
    <header class="nav-bar">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
      </router-link>
      <div class="avatar-icon" @click="toggleMenu">👤</div>
      <ul v-if="menuOpen" class="menu-dropdown">
        <li @click="logout">Logout</li>
      </ul>
    </header>

    <div class="chat-container">
      <!-- sidebar toggle buttons -->
      <div class="sidebar-toggle">
        <button @click="showHistory = true"></button>
        <button @click="showHistory = false"></button>
      </div>

      <!-- optional left sidebar -->
      <aside v-if="showHistory" class="chat-history">
        <h3>Verlauf</h3>
        <ul>
          <li v-for="(msg, i) in history" :key="i">{{ msg }}</li>
        </ul>
      </aside>

      <!-- main chat area -->
      <section class="chat-main">
        <h2>Hi, ich bin dein [{{ botName }}]-Bot!</h2>
        <hr />
        <h3>Wie kann ich dir behilflich sein?</h3>

        <div class="chat-input-box">
          <button class="upload-btn">⤴</button>
          <input
            v-model="userQuestion"
            type="text"
            placeholder="Stelle mir eine Frage..."
          />
          <button class="send-btn" @click="sendQuestion">▶</button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const botName = "Muster";

const showHistory = ref(true);
const history = ref(["Hallo!", "Ich bin Ihr Bot-Verlaufseintrag."]);
const userQuestion = ref("");

// Menu logic
const menuOpen = ref(false);
function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}
function logout() {
  router.push("/login");
}

// When user clicks send, you can push the question into history then…
function sendQuestion() {
  if (!userQuestion.value.trim()) return;
  history.value.push(`User: ${userQuestion.value}`);
  // Here you’d call your AI and push the response:
  history.value.push(`Bot: Antwort auf "${userQuestion.value}"`);
  userQuestion.value = "";
}
</script>

<style>
.chat-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f9fafb;
}
.chat-container {
  display: flex;
  flex: 1;
  padding: 1rem 2rem;
}
.sidebar-toggle {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-right: 1rem;
}
.sidebar-toggle button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}
.chat-history {
  width: 200px;
  background: #fff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 1rem;
  margin-right: 1rem;
}
.chat-history h3 {
  margin-top: 0;
  color: #0369a1;
}
.chat-history ul {
  list-style: none;
  padding: 0;
}
.chat-history li {
  background: #f1f5f9;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
}
.chat-main {
  flex: 1;
  background: #fff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
}
.chat-main h2 {
  margin: 0;
  padding-top: 150px;
  color: #0369a1;
  font-size: 48px;
}
.chat-main h3 {
  margin-top: 0.5rem;
  color: #0369a1;
  font-size: 48px;
}
.chat-input-box {
  display: flex;
  align-items: center;
  border: 2px solid #38bdf8;
  border-radius: 40px;
  margin-top: 1.5rem;
  padding: 0.5rem 1rem;
}
.chat-input-box input {
  flex: 1;
  border: none;
  outline: none;
  padding: 0 1rem;
}
.upload-btn,
.send-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
}
.send-btn {
  background: #0369a1;
  color: white;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
