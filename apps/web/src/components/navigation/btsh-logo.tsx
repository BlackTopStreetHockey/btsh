import Image from "next/image";
import Link from "next/link";


export default function BTSHLogo({}) {
  return (
    <Link href='/'>
      <div className='flex flex-col items-center'>
        <Image src="/btsh-head.svg" alt="BTSH" width={24} height={24} />
        <h2 className="text-lg font-bold">BTSH</h2>
      </div>
    </Link>
  )
}