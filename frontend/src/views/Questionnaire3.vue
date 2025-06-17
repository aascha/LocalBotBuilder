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
          <h3>3. Was sind deine Systemspezifikationen?</h3>
        </div>
        <div class="answers-wrapper">
          <label class="answer-option">
            <input
              type="radio"
              id="option1"
              name="system-specs"
              value="1"
              v-model="selectedOption"
              @change="updateSelectedOption(options[0])"
            />
            <span
              ><b>Einsteiger</b> <br /><span class="option-description"
                >Dual-core CPU, 4-8GB RAM</span
              ></span
            >
          </label>
          <label class="answer-option">
            <input
              type="radio"
              id="option2"
              name="system-specs"
              value="2"
              v-model="selectedOption"
              @change="updateSelectedOption(options[1])"
            />
            <span
              ><b>Mittel</b> <br /><span class="option-description"
                >Quad-core CPU, 8-16GB RAM</span
              ></span
            >
          </label>
          <label class="answer-option">
            <input
              type="radio"
              id="option3"
              name="system-specs"
              value="3"
              v-model="selectedOption"
              @change="updateSelectedOption(options[2])"
            />
            <span
              ><b>Hohe Performanz</b> <br />
              <span class="option-description"
                >6+ Core CPU, 16-32GB RAM, GPU</span
              ></span
            >
          </label>
          <label class="answer-option">
            <input
              type="radio"
              id="option4"
              name="system-specs"
              value="4"
              v-model="selectedOption"
              @change="updateSelectedOption(options[3])"
            />
            <span
              ><b>Nicht sicher</b> <br /><span class="option-description"
                >Standard-Modell wird verwendet</span
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

const router = useRouter();
const sideBarActive = ref(false);
const store = useQuestionnaireStore();
const selectedOptionValue = ref(null);
const selectedOptionId = ref(null);
const setDefaultModel = ref(true);
const menuOpen = ref(false);

const options = [
  { id: "option1", value: "Einsteiger" },
  { id: "option2", value: "Mittel" },
  { id: "option3", value: "Hohe Performanz" },
  { id: "option4", value: "Nicht sicher" },
];

const updateSelectedOption = (option) => {
  selectedOptionValue.value = option.value;
  selectedOptionId.value = option.id;
  store.setThirdAnswer(option);
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
  if (selectedOptionValue.value != null) {
    if (store.firstAnswer.value === "Experte") {
      // Check the value of the first answer and navigate accordingly
      router.push("/questionnaire4_expert");
    } else {
      router.push("/questionnaire4");
    }
  } else {
    alert("Bitte wähle eine Option aus.");
  }
}

function goBack() {
  router.push("/questionnaire2");
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
