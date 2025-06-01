<template>
  <div class="page-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <!-- replace sidebar-icon.svg with your own -->
      <img src="../assets/sidebar-icon.svg" class="sidebar-icon" alt="Menu" />
      <router-link to="/create" class="nav-button">Bot erstellen</router-link>
      <router-link to="/botoverview" class="nav-button">Meine Bots</router-link>
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

<style scoped>
/* Layout container */
.page-layout {
  display: flex;
  flex-wrap: wrap;
  min-height: 100vh;
}

/* Sidebar styles */
.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #f4f4f4;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sidebar-icon {
  width: 40px;
  margin-bottom: 20px;
}

.nav-button {
  display: block;
  width: 100%;
  text-align: center;
  margin-bottom: 10px;
  padding: 10px;
  color: #fff;
  background-color: #007bff;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.nav-button:hover {
  background-color: #0056b3;
}

/* Main content styles */
.content-card {
  flex: 1;
  padding: 40px;
  background-color: #ffffff;
}

h2 {
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
}

p {
  font-size: 16px;
  line-height: 1.6;
  color: #444;
  margin-bottom: 20px;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

/* Responsive layout */
@media (max-width: 768px) {
  .page-layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    flex-direction: row;
    justify-content: space-around;
  }

  .nav-button {
    width: auto;
    margin: 5px;
  }

  .content-card {
    padding: 20px;
  }
}

</style>
