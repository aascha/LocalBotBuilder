<template>
  <div class="datenschutz-page">
    <!-- Header -->
    <header class="nav-bar">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo_full.svg" alt="Logo" class="top-logo" />
      </router-link>

      <div class="user-menu">
        <div class="user-name" @click="openMenu">
          {{ user?.name || 'Lade...' }}
        </div>
        <ul v-if="menuOpen" class="menu-dropdown">
          <li @click="logout">Logout</li>
        </ul>
      </div>
    </header>

    <!-- Sidebar + Content layout -->
    <div class="side-main-wrapper">
      <aside id="sidebar" class="sidebar">
        <div>
          <img
            src="../assets/sidebar-icon.svg"
            class="sidebar-icon"
            alt="Menu"
            @click.stop="toggleSidebar"
          />
        </div>
        <router-link to="/create" class="nav-button">Bot erstellen</router-link>
        <router-link to="/botoverview" class="nav-button">Meine Bots</router-link>
      </aside>

      <!-- Main content area -->
      <div class="legal-box fade-in">
        <h2>Datenschutzerklärung</h2>

        <section>
          <h3>1. Verantwortliche Stelle</h3>
          <p>
            Diese Website ist ein Projekt der Hochschule Augsburg im Rahmen einer Lehrveranstaltung.<br />
            Verantwortlich für den Inhalt:
          </p>
          <p>
            Technische Hochschule Augsburg<br />
            An der Hochschule 1<br />
            86161 Augsburg<br />
            E-Mail: <a href="mailto:info@tha.de">info@tha.de</a>
          </p>
        </section>

        <section>
          <h3>2. Allgemeines zur Datenverarbeitung</h3>
          <p>
            Wir verarbeiten personenbezogene Daten nur im technisch notwendigen Umfang. Eine Weitergabe an Dritte erfolgt nicht.
          </p>
        </section>

        <section>
          <h3>3. Kontaktaufnahme</h3>
          <p>
            Bei der Kontaktaufnahme über ein Formular oder per E-Mail werden Ihre Angaben zur Bearbeitung der Anfrage gespeichert.
          </p>
        </section>

        <section>
          <h3>4. Verwendung von Cookies</h3>
          <p>
            Diese Website verwendet technisch notwendige Cookies. Es werden keine Tracking-Cookies eingesetzt.
          </p>
        </section>

        <section>
          <h3>5. Webanalyse</h3>
          <p>
            Diese Website nutzt <strong>keine</strong> Webanalyse-Tools wie Google Analytics.
          </p>
        </section>

        <section>
          <h3>6. Ihre Rechte</h3>
          <p>
            Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch.
          </p>
          <p>
            Bei datenschutzrechtlichen Beschwerden wenden Sie sich bitte an den Datenschutzbeauftragten der Hochschule.
          </p>
        </section>

        <section>
          <h3>7. Datenschutzbeauftragter der Hochschule Augsburg</h3>
          <p>
            Website: <a href="https://www.hs-augsburg.de/Datenschutz.html" target="_blank">https://www.tha.de/Service/Datenschutz.html</a>
          </p>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const user = ref(null);
const menuOpen = ref(false);
const sideBarActive = ref(false);
const router = useRouter();

function openMenu() {
  menuOpen.value = !menuOpen.value;
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

async function logout() {
  try {
    await axios.post("/api/logout", {}, { withCredentials: true });
    localStorage.removeItem("user");
    localStorage.removeItem("questionnaireDone");
    router.push("/login");
  } catch (err) {
    console.error("Logout fehlgeschlagen:", err);
  }
}

onMounted(async () => {
  try {
    const session = await axios.get("/api/me", { withCredentials: true });
    if (session.data.user) {
      user.value = session.data.user;
    }
    // Do nothing if no user — stay on page
  } catch (err) {
    console.error("Fehler beim Laden:", err);
    // Don't redirect, just log the error
  }
});
</script>


<style scoped>

.side-main-wrapper {
  display: flex;
  flex: 1;
  height: 100%;
  overflow: hidden;
}
.datenschutz-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.legal-box {
  flex: 1;
  overflow-y: auto;
  padding: 3rem;
  background-color: #ffffff;
  color: #333;
  line-height: 1.7;
  font-size: 16px;
  max-width: 900px;
  margin: 0 auto;
}

.legal-box h2 {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #222;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

.legal-box h3 {
  font-size: 20px;
  margin-top: 30px;
  margin-bottom: 10px;
  color: #222;
}

.legal-box p {
  margin-bottom: 1.5rem;
}

.legal-box strong {
  font-weight: 600;
  color: #000;
}

.legal-box a {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.legal-box a:hover {
  text-decoration: underline;
}

section {
  margin-bottom: 30px;
}

.fade-in {
  animation: fadeIn ease 1s;
  animation-fill-mode: forwards;
  opacity: 0;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
