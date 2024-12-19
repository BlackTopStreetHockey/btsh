"use client";

import BTSHSidebar from "./btsh-sidebar";
import BTSHTopbar from "./btsh-topbar";



export default function BTSHNavbar() {
  return (
    <div>
      <div className='hidden md:block'>
        <BTSHSidebar />
      </div>
      <div className='block md:hidden'>
        <BTSHTopbar />
      </div>

    </div>
  );
};