import clsx from "clsx";
import Link from "next/link";


export default function TeamName({ 
  team,
  link,
  className='text-sm',
  imWidth=32
}: { 
  team: Team,
  link?: boolean,
  className?: string,
  imWidth?: number
}) {
  const content = (
    <div className={clsx("flex flex-row gap-2", className)}>
      <img src={team.logo} alt={team.name} width={imWidth} className='rounded' />
      <div>{team.name}</div>
    </div>
  );
  if (link) {
    return (
      <Link href={`/teams/${team.short_name}`}>
        {content}
      </Link>
    )
  }
  return content;
}