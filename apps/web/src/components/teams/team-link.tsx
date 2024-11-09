import Link from "next/link";


export default function TeamLink({ team }: { team: Team }) {
  return (
    <Link href={`/teams/${team.id}`}>
      <div className="flex flex-row gap-2">
        <img src={team.logo} alt={team.name} width={24} height={24} className='rounded' />
        <div className="text-sm">{team.name}</div>
      </div>
    </Link>
  )
}