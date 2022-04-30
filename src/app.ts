import { Termynal } from "./termynal";

export function runDevApp() {
  new Termynal("#app", {
    lineData: [{ value: "💬 This is a development termynal" }],
  });
}
