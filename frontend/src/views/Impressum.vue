<template>
  <div class="impressum-page">
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
      <div class="impressum-box">
        <h2>Impressum</h2>
        <p>
          <strong>Herausgeber</strong><br />
          Technische Hochschule Augsburg<br />
          An der Hochschule 1<br />
          86161 Augsburg
        </p>
        <p>
          Telefon: +49 (0)821-5586-0<br />
          Telefax: +49 (0)821-5586-3222<br />
          E-Mail: <a href="mailto:info@tha.de">info@tha.de</a>
        </p>
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
    // No redirect if not logged in!
  } catch (err) {
    console.error("Fehler beim Laden:", err);
    // Also no redirect here
  }
});
</script>


<style scoped>
.impressum-box {
  flex: 1;
  overflow-y: auto;
  padding: 3rem;
  background-color: #ffffff;
  color: #333;
  line-height: 1.7;
  font-size: 16px;
  max-width: 800px;
  margin: 0 auto;
}

.impressum-box h2 {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #222;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

.impressum-box p {
  margin-bottom: 1.5rem;
}

.impressum-box strong {
  font-weight: 600;
  color: #000;
}

.impressum-box a {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.impressum-box a:hover {
  text-decoration: underline;
}

</style>