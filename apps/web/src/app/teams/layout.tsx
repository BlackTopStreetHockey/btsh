import React from "react";

const ScheduleLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="relative flex flex-col h-screen">
      <main className="w-full p-6 flex-grow">{children}</main>
    </div>
  );
};

export default ScheduleLayout;
