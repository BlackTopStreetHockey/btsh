import clsx from "clsx";
import Link from "next/link";
import { usePathname } from "next/navigation";


export default function BTSHNavLink({
  label,
  href,
}: {
  label: string,
  href: string
}) {
  const pathname = usePathname();

  return (
    <div className='w-full px-3 py-2 rounded-md bg-gray-900 text-gray-300 hover:text-white'>
      <Link href={href} className={clsx("block w-full", {
        "font-bold": pathname.startsWith(href)
      })}>
        {label}
      </Link>
    </div>
  )
}