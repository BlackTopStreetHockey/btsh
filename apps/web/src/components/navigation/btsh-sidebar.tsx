import BTSHLogo from "./btsh-logo"
import BTSHNavLinkList from "./btsh-nav-link-list";


export default function BTSHSidebar() {
  return (
    <div className="bg-gray-800 text-white fixed top-0 left-0 w-32 h-screen p-2">
      <div className="flex flex-col gap-8">
        <BTSHLogo />    

        <BTSHNavLinkList />
      </div>
    </div>
  )
}
