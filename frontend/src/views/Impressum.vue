<template>
    <div class="page-layout">
      <!-- Sidebar -->
      <aside class="sidebar">
        <!-- replace sidebar-icon.svg with your own -->
        <img src="../assets/sidebar-icon.svg" class="sidebar-icon" alt="Menu" />
        <button class="side-btn" @click="$router.push('/create')">Bot erstellen</button>
        <button class="side-btn" @click="$router.push('/chat')">Meine Bots</button>
      </aside>
  
      <!-- Content card -->
      <div class="content-card">
        <h2>Impressum</h2>
        <p><strong>Herausgeber</strong><br/>
           Technische Hochschule Augsburg<br/>
           An der Hochschule 1<br/>
           86161 Augsburg</p>
        <p>
          Telefon: +49 (0)821-5586-0<br/>
          Telefax: +49 (0)821-5586-3222<br/>
          E-Mail: <a href="mailto:info@tha.de">info@tha.de</a>
        </p>
      </div>
    </div>
  </template>
  
  
  
  
  
  