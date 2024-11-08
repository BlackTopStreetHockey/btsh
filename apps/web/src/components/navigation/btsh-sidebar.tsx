import Image from "next/image";
import Link from "next/link";

export default function BTSHSidebar() {
  return (
    <div className="bg-gray-800 text-white w-64 h-screen fixed top-0 left-0">
      <div className="p-4">
        <Link href='/'>
          <Image src="/btsh-head.svg" alt="BTSH" width={24} height={24} />
          <h2 className="text-lg font-bold mb-4">BTSH</h2>
        </Link>

        <ul>
          <li className="mb-4">
            <Link href="/schedule" className="text-gray-300 hover:text-white">
              Schedule
            </Link>
          </li>
          <li className="mb-4">
            <Link href="/standings" className="text-gray-300 hover:text-white">
              Standings
            </Link>
          </li>
          <li className="mb-4">
            <a href="/stats" className="text-gray-300 hover:text-white">
              Stats
            </a>
          </li>
        </ul>

      </div>
    </div>
  );
};