"use client";

import { createContext, useContext, useState, ReactNode, useEffect } from "react";

interface RegistrationData {
  firstName: string;
  lastName: string;
  fullName: string;
  email: string;
  gender: string;
  position: string;
  team: string;
  location: string;
  helpingInterests: string[];
  otherSkills: string;
  partyTheme: string;
  waiverSignature: string;
  waiverEmail: string;
  waiverAccepted: boolean;
}

interface RegistrationContextType {
  formData: RegistrationData;
  updateFormData: (data: Partial<RegistrationData>) => void;
}

const RegistrationContext = createContext<RegistrationContextType | undefined>(
  undefined
);

const initialFormData: RegistrationData = {
  firstName: "",
  lastName: "",
  fullName: "",
  email: "",
  gender: "",
  position: "",
  team: "",
  location: "",
  helpingInterests: [],
  otherSkills: "",
  partyTheme: "",
  waiverSignature: "",
  waiverEmail: "",
  waiverAccepted: false,
};

export function RegistrationProvider({ children }: { children: ReactNode }) {
  const [formData, setFormData] = useState<RegistrationData>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('registrationData');
      if (saved) {
        return JSON.parse(saved);
      }
    }
    return initialFormData;
  });

  useEffect(() => {
    if (formData.firstName || formData.lastName) {
      const fullName = `${formData.firstName} ${formData.lastName}`.trim();
      setFormData(prev => ({ ...prev, fullName }));
    }
  }, [formData.firstName, formData.lastName]);

  useEffect(() => {
    localStorage.setItem('registrationData', JSON.stringify(formData));
  }, [formData]);

  const updateFormData = (newData: Partial<RegistrationData>) => {
    setFormData((prev) => {
      const updated = { ...prev, ...newData };
      return updated;
    });
  };

  return (
    <RegistrationContext.Provider value={{ formData, updateFormData }}>
      {children}
    </RegistrationContext.Provider>
  );
}

export function useRegistration() {
  const context = useContext(RegistrationContext);
  if (context === undefined) {
    throw new Error("useRegistration must be used within a RegistrationProvider");
  }
  return context;
} 