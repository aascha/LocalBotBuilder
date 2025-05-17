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
      <button class="nav-button" @click="goToBuilder">Bot erstellen</button>
      <button class="nav-button">Meine Bots</button>
    </aside>
    <!-- Main Content -->
    <main class="main-content">
      <div class="quiz-wrapper">
        <div class="question">
          <h3>3. Was sind deine Systemspezifikationen?</h3>
        </div>
        <div class="answers-wrapper">
          <label class="answer-option">
            <input type="radio" id="option1" name="system-specs" value="1" />
            <span><b>Einsteiger</b> <br />Dual-core CPU, 4-8GB RAM</span>
          </label>
          <label class="answer-option">
            <input type="radio" id="option2" name="system-specs" value="2" />
            <span><b>Mittel</b> <br />Quad-core CPU, 8-16GB RAM</span>
          </label>
          <label class="answer-option">
            <input type="radio" id="option3" name="system-specs" value="3" />
            <span
              ><b>Hohe Performanz</b> <br />6+ Core CPU, 16-32GB RAM, GPU</span
            >
          </label>
          <label class="answer-option">
            <input type="radio" id="option4" name="system-specs" value="4" />
            <span
              ><b>Nicht sicher</b> <br />Standard-Modell wird verwendet</span
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

const router = useRouter();
const sideBarActive = ref(false);

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
  router.push("/questionnaire4");
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
