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
      <button class="nav-button">Meine Bots</button>
    </aside>
    <!-- Main Content -->
    <main class="main-content">
      <div class="quiz-wrapper">
        <div class="question">
          <h3>4. Basierend auf deiner Auswahl, empfehlen wir:</h3>
        </div>
        <div class="answers-wrapper">
          <label
            class="answer-option"
            :class="{
              'suggested-model': store.thirdAnswer.value === 'Nicht sicher',
            }"
          >
            <input
              type="radio"
              id="option1"
              name="model-selection"
              value="1"
              v-model="selectedOption"
              @change="updateSelectedOption(options[0])"
            />
            <span
              ><b>Standard-Modell</b> <br /><span class="option-description"
                >Läuft auf jedem System</span
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
              ><b>Ausgeglichenes Modell</b> <br /><span
                class="option-description"
                >Bessere Qualität, moderate Ressourcenausschöpfung</span
              ></span
            >
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
              ><b>Performance-Modell</b> <br />
              <span class="option-description"
                >Beste Qualität, höhere Ressourcenausschöpfung</span
              ></span
            >
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
import { watch } from "vue";

const options = [
  { id: "option1", value: "1" },
  { id: "option2", value: "2" },
  { id: "option3", value: "3" },
];

const selectedOption = ref(null);
const store = useQuestionnaireStore();
const menuOpen = ref(false);

const updateSelectedOption = (option) => {
  selectedOption.value = option.value;
  store.setFourthAnswer(option);
};
const router = useRouter();
const sideBarActive = ref(false);

function goToLanding() {
  router.push("/");
}

function goToBuilder() {
  router.push("/builder");
}
function openMenu() {
  menuOpen.value = !menuOpen.value;
}
function logout() {
  router.push("/login");
}

function goToNextQuestion() {
  if (selectedOption.value === null) {
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

function selectModel() {
  if (store.thirdAnswer.value === "Nicht sicher") {
    selectedOption.value = options[0].value;
  }
}
watch(() => store.thirdAnswer.value, selectModel); // Calls selectModel whenever thirdAnswer changes
</script>
