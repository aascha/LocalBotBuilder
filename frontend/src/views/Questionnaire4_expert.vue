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
          <h3>4. Wähle eine Sprachmodell-Konfiguration</h3>
        </div>
        <div class="answers-wrapper">
          <label class="answer-option">
            <input
              type="radio"
              id="option1"
              name="model-selection"
              value="1"
              v-model="selectedOption"
              @change="updateSelectedOption(options[0])"
            />
            <span
              ><b>Qwen2.5-3B (Standard-Modell)</b> <br /><span
                class="option-description"
                >4-12GB RAM, Min. GPU: GTX 1650 (4GB)
              </span></span
            >
          </label>
          <label class="answer-option">
            <input
              type="radio"
              id="option2"
              name="model-selection"
              value="2"
              v-model="selectedOption"
              @change="updateSelectedOption(options[1])"
            />
            <span
              ><b>Mistral-7b</b> <br />
              <span class="option-description"
                >12-16GB RAM, Min. GPU: GTX 1660/RTX 2060</span
              >
            </span>
          </label>
          <label class="answer-option">
            <input
              type="radio"
              id="option3"
              name="model-selection"
              value="3"
              v-model="selectedOption"
              @change="updateSelectedOption(options[2])"
            />
            <span
              ><b>LLaMA3-8b</b> <br /><span class="option-description"
                >16-38GB RAM, Min. GPU: RTX 2060 (6GB)</span
              >
            </span>
          </label>

          <div class="quiz-button-container">
            <button class="continue-button" @click="goToNextQuestion">
              Fortfahren
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
const options = [
  { id: "option1", value: "1" },
  { id: "option2", value: "2" },
  { id: "option3", value: "3" },
  { id: "option4", value: "4" },
];

const selectedOptionValue = ref(null);
const selectedOptionId = ref(null);
const menuOpen = ref(false);

const updateSelectedOption = (option) => {
  selectedOptionValue.value = option.value;
  selectedOptionId.value = option.id;
  store.setFourthAnswer(option);
};

function goToLanding() {
  router.push("/");
}

function goToBuilder() {
  router.push("/builder");
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

function goToNextQuestion() {
  if (selectedOptionValue.value === null) {
    alert("Bitte wähle eine Option aus.");
    return;
  }
  router.push("/questionnaire5");
}
function goBack() {
  router.push("/questionnaire3");
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
