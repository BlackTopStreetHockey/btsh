import BTSHNavLink from "./btsh-nav-link";
import { useNavigationLinks } from "./useNavigationLinks";


export default function BTSHNavLinkList() {
  const links = useNavigationLinks();

  return (
    <div className='flex flex-col gap-4'>
      {links.map((link) => (
        <div key={link.id}>
          <BTSHNavLink key={link.id} {...link} />
        </div>
      ))}
    </div>
  )
}