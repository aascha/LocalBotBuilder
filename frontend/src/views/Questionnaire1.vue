<template>
  <div class="questionnaire"></div>
  <header class="header">
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0, user-scalable=no"
    />
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
          <h3>
            1. Wie würdest du deine Erfahrung mit KI/LLM Tools beschreiben?
          </h3>
        </div>
        <div class="answers-wrapper">
          <label class="answer-option">
            <input type="radio" id="option1" name="experience" value="1" />
            <span
              ><b>Amateur</b> <br />Ich habe noch nie mit KI/LLM Tools
              gearbeitet.</span
            >
          </label>
          <label class="answer-option">
            <input type="radio" id="option2" name="experience" value="2" />
            <span
              ><b>Experte</b> <br />Ich habe ein wenig Erfahrung mit KI/LLM
              Tools.</span
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
