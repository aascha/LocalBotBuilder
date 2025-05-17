<template>
    <div class="page-layout">
      <!-- Sidebar same as Impressum -->
      <aside class="sidebar">
        <img src="../assets/sidebar-icon.svg" class="sidebar-icon" alt="Menu" />
        <button class="side-btn" @click="$router.push('/create')">Bot erstellen</button>
        <button class="side-btn" @click="$router.push('/chat')">Meine Bots</button>
      </aside>
  
      <!-- Content card -->
      <div class="content-card">
        <h2>Datenschutz</h2>
        <p>
          Hier steht Ihr Datenschutz‐Text. Beschreiben Sie, wie Nutzerdaten
          verarbeitet werden, welche Cookies eingesetzt werden, etc.
        </p>
      </div>
    </div>
  </template>
  
  

  
  