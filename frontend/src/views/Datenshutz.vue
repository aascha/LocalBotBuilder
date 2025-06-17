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
      <h2>Datenschutz</h2>
      <p>
        <br />
        <b>Verantwortlicher und Geltungsbereich</b> <br />
        <br />Der Verantwortliche im Sinne der EU-Datenschutzgrundverordnung (im
        Folgenden: DSGVO) und <br />
        anderer nationaler Datenschutzgesetze der Mitgliedsstaaten sowie
        sonstiger <br />
        datenschutzrechtlicher Bestimmungen ist: <br />
        <br />
        <b>Technische Hochschule Augsburg</b>, <br />
        Körperschaft des öffentlichen Recht gemäß Art. 11 Abs. 1 S. 1 BayHSchG,
        <br />
        vertreten durch ihren Präsidenten Prof. Dr. Gordon T. Rohrmair <br />
        <br />

        An der Hochschule 1 <br />
        86161 Augsburg <br />
        <br />
        Telefon: +49 (0)821-5586-0 <br />
        Telefax: +49 (0)821-5586-3222 <br />
        <br />
        info@tha.de <br />
        <br />
        Diese Datenschutzerklärung gilt für die Webseiten: <br />
        <a href="https://www.tha.de">https://www.tha.de</a>
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
