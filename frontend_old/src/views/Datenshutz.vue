<template>
  <div class="page-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <img src="../assets/sidebar-icon.svg" class="sidebar-icon" alt="Menu" />
      <router-link to="/" class="nav-button">Startseite</router-link>
      <router-link to="/create" class="nav-button">Bot erstellen</router-link>
      <router-link to="/botoverview" class="nav-button">Meine Bots</router-link>
    </aside>

    <!-- Main content -->
    <main class="content-card fade-in">
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
          E-Mail: info@tha.de
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
    </main>
  </div>
</template>

<style scoped>
.page-layout {
  display: flex;
  flex-wrap: wrap;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
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

h3 {
  font-size: 20px;
  margin-top: 30px;
  margin-bottom: 10px;
  color: #222;
}

p {
  font-size: 16px;
  line-height: 1.6;
  color: #444;
  margin-bottom: 20px;
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
