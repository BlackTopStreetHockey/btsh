import { HamburgerMenuIcon } from "@radix-ui/react-icons";
import BTSHLogo from "./btsh-logo";
import { useState } from "react";
import clsx from "clsx";
import BTSHNavLinkList from "./btsh-nav-link-list";



export default function BTSHTopbar({}) {
  const [open, setOpen] = useState(false);
  return (
    // justify contet space between
    <div>
      <div className="h-16 w-screen bg-gray-800 text-white fixed top-0 left-0 p-2 shadow-b-md">
        <div className='flex flex-row items-center justify-between'>
          <BTSHLogo row/>
          <button 
            className="inline-flex items-center justify-center p-2 w-10 h-10 text-sm rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200"
            onClick={() => setOpen(!open)}
          >
            <HamburgerMenuIcon />
          </button>
        </div>
      </div>
      {/* opening sidebar */}
      <div className={`${open ? 'block' : 'hidden'} w-full fixed top-16 left-0 z-50 shadow-t`}>
        <div className='h-100 bg-gray-800 pb-4 rounded-b shadow-b'>
          <div className='p-4'>
            <BTSHNavLinkList />
          </div>
        </div>
      </div>
    </div>
  )
}