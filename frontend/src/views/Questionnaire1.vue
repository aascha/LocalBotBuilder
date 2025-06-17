<template>
  <div class="wrapper">
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
            <h3>
              1. Wie würdest du deine Erfahrung mit KI/LLM Tools beschreiben?
            </h3>
          </div>
          <div class="answers-wrapper">
            <label class="answer-option">
              <input
                type="radio"
                id="option1"
                name="experience"
                value="1"
                v-model="selectedOption"
                @change="updateSelectedOption(options[0])"
              />
              <span
                ><b>Amateur</b> <br />
                <span class="option-description"
                  >Ich habe bisher kaum mit KI/LLM Tools gearbeitet.</span
                ></span
              >
            </label>
            <label class="answer-option">
              <input
                type="radio"
                id="option2"
                name="experience"
                value="2"
                v-model="selectedOption"
                @change="updateSelectedOption(options[1])"
              />
              <span
                ><b>Experte</b> <br />
                <span class="option-description"
                  >Ich habe viel Erfahrung mit KI/LLM Tools.</span
                ></span
              >
            </label>
          </div>
          <!-- Continue Button -->
          <div class="quiz-button-container">
            <button class="continue-button" @click="goToNextQuestion">
              Fortfahren
            </button>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useQuestionnaireStore } from "../store";

const options = [
  { id: "option1", value: "Amateur" },
  { id: "option2", value: "Experte" },
];

const selectedOptionValue = ref(null);
const selectedOptionId = ref(null);
const store = useQuestionnaireStore();
const menuOpen = ref(false);

const updateSelectedOption = (option) => {
  selectedOptionValue.value = option.value;
  selectedOptionId.value = option.id;
  store.setFirstAnswer(option);
};

const router = useRouter();
const sideBarActive = ref(false);

function goToLanding() {
  router.push("/");
}

function goToBuilder() {
  router.push("/create");
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
  if (selectedOptionValue.value != null) {
    router.push("/questionnaire2");
  } else alert("Bitte wähle eine Option aus.");
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
