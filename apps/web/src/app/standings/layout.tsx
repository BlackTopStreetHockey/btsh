import React from "react";

const StandingsLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="relative flex flex-col min-h-screen bg-gray-100">
      <main className="w-full p-6 flex-grow">{children}</main>
    </div>
  );
};

export default StandingsLayout;
