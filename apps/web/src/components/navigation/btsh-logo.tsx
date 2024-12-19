import Image from "next/image";
import Link from "next/link";


export default function BTSHLogo({ row }: { row?: boolean }) {
  return (
    <Link href='/'>
      <div className={`flex ${row ? 'flex-row' : 'flex-col'} gap-2 items-center`}>
        <Image src="/btsh-head.svg" alt="BTSH" width={36} height={36} />
        <h2 className="text-lg font-bold">BTSH</h2>
      </div>
    </Link>
  )
}