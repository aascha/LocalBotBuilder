<template>
  <div class="page-layout">
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

    <!-- Content card -->
    <div class="content-card">
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
</template>
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const sideBarActive = ref(false);
const router = useRouter();

function goToBuilder() {
  router.push("/create");
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
<style>
.content-card {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  padding: 20px 100px;
  margin: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
