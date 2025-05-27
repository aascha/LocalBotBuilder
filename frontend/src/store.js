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
  },
});
