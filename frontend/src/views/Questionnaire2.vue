<template>
  <div class="questionnaire"></div>
  <header class="nav-bar">
    <div @click="goToLanding" class="logo">
      <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
    </div>

    <div class="avatar-icon" @click="openMenu">
      <font-awesome-icon icon="circle-user" class="user-icon" />
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
          <h3>2. Was soll dein Chatbot können?</h3>
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
            <span
              ><b>Schnelligkeit</b> <br /><span class="option-description"
                >Schnellere Antworten</span
              ></span
            >
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
            <span
              ><b>Qualität</b> <br /><span class="option-description"
                >Detailliertere / genauere Antworten</span
              ></span
            >
          </label>
          <label class="answer-option">
            <input
              type="radio"
              id="option3"
              name="priority"
              value="3"
              v-model="selectedOption"
              @change="updateSelectedOption(options[2])"
            />
            <span
              ><b>Ausgeglichen</b> <br /><span class="option-description"
                >Gute Mischung aus Schnelligkeit / Qualität</span
              ></span
            >
          </label>
          <label class="answer-option">
            <input
              type="radio"
              id="option4"
              name="priority"
              value="4"
              v-model="selectedOption"
              @change="updateSelectedOption(options[3])"
            />
            <span
              ><b>Minimale Ressourcenausschöpfung</b> <br /><span
                class="option-description"
                >Für ältere Systeme</span
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

const options = [
  { id: "option1", value: "Schnelligkeit" },
  { id: "option2", value: "Qualität" },
  { id: "option3", value: "Ausgeglichen" },
  { id: "option4", value: "Minimale Ressourcenausschöpfung" },
];

const selectedOptionValue = ref(null);
const selectedOptionId = ref(null);
const store = useQuestionnaireStore();
const menuOpen = ref(false);

const updateSelectedOption = (option) => {
  selectedOptionValue.value = option.value;
  selectedOptionId.value = option.id;
  store.setSecondAnswer(option);
};

const router = useRouter();
const sideBarActive = ref(false);

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
  if (selectedOptionValue.value != null) {
    router.push("/questionnaire3");
  } else alert("Bitte wähle eine Option aus.");
}

function goBack() {
  router.push("/questionnaire1");
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
