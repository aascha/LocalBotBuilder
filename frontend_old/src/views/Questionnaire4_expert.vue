<template>
  <div class="questionnaire"></div>
  <header class="header">
    <div @click="goToLanding" class="logo">
      <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
    </div>

    <font-awesome-icon icon="circle-user" class="user-icon" @click="Logout" />
  </header>
  <div class="side-main-wrapper">
    <!-- Sidebar -->
    <aside id="sidebar" class="sidebar">
      <div>
        <font-awesome-icon
          icon="list"
          class="list-icon"
          @click.stop="toggleSidebar"
        />
      </div>
      <router-link to="/create" class="nav-button">Bot erstellen</router-link>
      <router-link to="/botoverview" class="nav-button">Meine Bots</router-link>
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
              ><b>Qwen 2.5 1.5B (Standard-Modell)</b> <br /><span
                class="option-description"
                >6-8GB RAM</span
              ></span
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
              ><b>Phi</b> <br />
              <span class="option-description">6-8GB RAM</span>
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
              ><b>DeepSeek-R1 7B</b> <br /><span class="option-description"
                >13-16GB RAM</span
              >
            </span>
          </label>
          <label class="answer-option">
            <input
              type="radio"
              id="option3"
              name="model-selection"
              value="4"
              v-model="selectedOption"
              @change="updateSelectedOption(options[3])"
            />
            <span><b>Benutzerdefiniert</b> </span>
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

function Logout() {
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
