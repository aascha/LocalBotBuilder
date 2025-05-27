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
          <h3>4. Basierend auf deiner Auswahl, empfehlen wir:</h3>
        </div>
        <div class="answers-wrapper">
          <label class="answer-option">
            <input type="radio" id="option1" name="model-selection" value="1" />
            <span><b>Standard-Modell</b> <br />Läuft auf jedem System</span>
          </label>
          <label class="answer-option">
            <input type="radio" id="option2" name="model-selection" value="2" />
            <span
              ><b>Ausgeglichenes Modell</b> <br />Bessere Qualität, moderate
              Ressourcenausschöpfung</span
            >
          </label>
          <label class="answer-option">
            <input type="radio" id="option3" name="model-selection" value="3" />
            <span
              ><b>Performance-Modell</b> <br />Beste Qualität, höhere
              Ressourcenausschöpfung</span
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
