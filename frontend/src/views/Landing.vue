<template>
  <div class="wrapper">
    <!-- Top navigation buttons -->
    <header class="nav-bar">
      <div></div>
      <!-- spacer -->
      <div class="nav-buttons">
        <button class="nav-btn light" @click="goToLogin">Anmelden</button>
        <button class="nav-btn dark" @click="goToRegister">Registrieren</button>
      </div>
    </header>

    <!-- Main content -->
    <main class="container">
      <!-- Logo + Title -->
      <div class="logo-box">
        <h1 class="logo-title">Local Bot Builder</h1>
        <img :src="logo" alt="Logo" class="logo-icon" />
      </div>

      <!-- Big Main Heading -->
      <h2 class="main-title">
        Erstelle deinen lokalen<br />
        Assistenten.
      </h2>

      <!-- Subtitle -->
      <p class="subtitle">
        Baue einen eigenen lokalen Chatbot, der dir bei deinen Fragen hilft und
        dir immer zur Seite steht.
      </p>

      <!-- Call to Action -->
      <button class="cta-button" @click="goToQuestionnaire">
        Erstelle deinen Chatbot
      </button>
    </main>

    <footer class="footer">
      <router-link to="/impressum" class="footer-link">Impressum</router-link>
      <router-link to="/datenschutz" class="footer-link"
        >Datenschutz</router-link
      >
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import logo from "../logo.jpg";

const router = useRouter();

function goToLogin() {
  router.push("/login");
}

function goToRegister() {
  router.push("/register");
}

function goToCreate() {
  router.push("/create");
}

function goToQuestionnaire() {
  router.push("/questionnaire1");
}
</script>
