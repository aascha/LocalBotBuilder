import { createRouter, createWebHistory } from "vue-router";
import Landing from "../views/Landing.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import CreateBot from "../views/CreateBot.vue";
import Chat from "../views/Chat.vue";
import Impressum from "../views/Impressum.vue";
import Datenschutz from "../views/Datenshutz.vue";
import Questionnaire1 from "../views/Questionnaire1.vue";
import Questionnaire2 from "../views/Questionnaire2.vue";
import Questionnaire3 from "../views/Questionnaire3.vue";
import Questionnaire4 from "../views/Questionnaire4.vue";
import Questionnaire5 from "../views/Questionnaire5.vue";
import Questionnaire4_expert from "../views/Questionnaire4_expert.vue";
import BotOverview from "../views/BotOverview.vue";
import BotEditor from "../views/BotEditor.vue";
import download from "../views/download.vue";

const routes = [
  { path: "/", component: Landing },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/create", component: CreateBot },
  { path: "/chat", component: Chat },
  { path: "/impressum", component: Impressum },
  { path: "/datenschutz", component: Datenschutz },
  { path: "/questionnaire1", component: Questionnaire1 },
  { path: "/questionnaire2", component: Questionnaire2 },
  { path: "/questionnaire3", component: Questionnaire3 },
  { path: "/questionnaire4", component: Questionnaire4 },
  { path: "/questionnaire5", component: Questionnaire5 },
  { path: "/questionnaire4_expert", component: Questionnaire4_expert },
  { path: "/botoverview", component: BotOverview },
  { path: "/boteditor", component: BotEditor },
  { path: "/download", component: download },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
