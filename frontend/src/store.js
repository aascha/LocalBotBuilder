import { defineStore } from "pinia";

export const useQuestionnaireStore = defineStore("questionnaire", {
  state: () => ({
    firstAnswer: null,
    secondAnswer: null,
    thirdAnswer: null,
    fourthAnswer: null,
    fifthAnswer: null,
  }),
  actions: {
    setFirstAnswer(answer) {
      this.firstAnswer = answer;
    },
    setSecondAnswer(answer) {
      this.secondAnswer = answer;
    },
    setThirdAnswer(answer) {
      this.thirdAnswer = answer;
    },
    setFourthAnswer(answer) {
      this.fourthAnswer = answer;
    },
    setFifthAnswer(answer) {
      this.fifthAnswer = answer;
    },
    reset() {
      this.firstAnswer = null;
      this.secondAnswer = null;
      this.thirdAnswer = null;
      this.fourthAnswer = null;
      this.fifthAnswer = null;
    },
  },
});

export const useModelStore = defineStore("model", {
  state: () => ({
    model: "qwen2.5:3b",
  }),
  actions: {
    setModel(model) {
      this.model = model;
    },
  },
});
