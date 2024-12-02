"use client";

import { useParams } from "next/navigation";
import RegistrationStep1 from "./components/step-1";
import RegistrationStep2 from "./components/step-2";
import { RegistrationProvider } from "../context/registration-context";

export default function RegistrationSteps() {
  const params = useParams();

  const StepComponent =
    params.step === "1" ? RegistrationStep1 : RegistrationStep2;

  return (
    <RegistrationProvider>
      <div className="container mx-auto px-4 py-8 max-w-2xl space-y-8">
        <StepComponent />
      </div>
    </RegistrationProvider>
  );
}
