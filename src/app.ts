import { Termynal } from "./termynal";

export function runDevApp() {
  new Termynal("#app", {
    lineData: [
      {
        value: "💬 This is a development termynal",
        class: "termynal-comment",
        delay: 0,
      },
      { prompt: "$", type: "input", value: "hello world" },
      { type: "progress", delay: 200 },
      { value: "we did it" },
    ],
  });
}
