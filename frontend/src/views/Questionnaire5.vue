<template>
  <div class="questionnaire"></div>
  <header class="nav-bar">
    <div @click="goToLanding" class="logo">
      <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
    </div>

    <div class="avatar-icon" @click="openMenu">
      <font-awesome-icon :icon="['fas', 'circle-user']" class="user-icon" />
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
      <button class="nav-button" @click="goToBuilder">Bot erstellen</button>
      <button class="nav-button" @click="goToBots">Meine Bots</button>
    </aside>
    <!-- Main Content -->
    <main class="main-content">
      <div class="quiz-wrapper">
        <div class="question">
          <h3>5. Zusätzliche Optionen</h3>
        </div>
        <div class="answers-wrapper">
          <label class="answer-option">
            <input
              type="radio"
              id="option1"
              name="priority"
              value="1"
              v-model="selectedOption"
              @change="updateSelectedOption(options[0])"
            />
            <span>Chatbot verweist auf verwendete Dokumente</span>
          </label>
          <label class="answer-option">
            <input
              type="radio"
              id="option2"
              name="priority"
              value="2"
              v-model="selectedOption"
              @change="updateSelectedOption(options[1])"
            />
            <span>Desktop-Verknüpfung für Chatbot erstellen</span>
          </label>
          <div class="quiz-button-container">
            <button class="goToBuilder-button" @click="goToBuilder">
              Zum Bot Builder
            </button>
            
            <button class="back-button" @click="goBack">Zurück</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useQuestionnaireStore } from "../store";

const router = useRouter();
const sideBarActive = ref(false);
const store = useQuestionnaireStore();
const selectedOption = ref(null);
const menuOpen = ref(false);
const options = [
  {
    id: 1,
    value: "1",
  },
  {
    id: 2,
    value: "2",
  },
];

function updateSelectedOption(option) {
  selectedOption.value = option.value;
  store.setFourthAnswer(option);
}

function goToLanding() {
  router.push("/");
}

import axios from "axios"; // ⬅️ Make sure this is included

async function goToBuilder() {
  try {
    const res = await axios.post("/api/complete_questionnaire", {}, { withCredentials: true });

    if (res.status === 200) {
      router.push("/create");
    } else {
      throw new Error("Unexpected response");
    }
  } catch (err) {
    console.error("Fehler beim Abschließen des Fragebogens:", err.response?.data || err);
    alert("❌ Etwas ist schiefgelaufen. Versuche es erneut.");
  }
}



function goToBots() {
  router.push("/botoverview");
}

function openMenu() {
  menuOpen.value = !menuOpen.value;
}
function logout() {
  router.push("/login");
}

function goBack() {
  if (store.firstAnswer.value === "Experte") {
    router.push("/questionnaire4_expert");
  } else {
    router.push("/questionnaire4");
  }
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
