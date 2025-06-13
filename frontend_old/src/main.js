import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./style.css";
import "typeface-inter";
import { FontAwesomeIcon } from "./icons";

const app = createApp(App);

app.component("font-awesome-icon", FontAwesomeIcon);
app.use(router);
app.mount("#app");
