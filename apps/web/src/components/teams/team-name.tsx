import clsx from "clsx";
import Link from "next/link";

export default function TeamName({
  team,
  link,
  size = 24,
  className = "text-sm",
}: {
  team: Team;
  link?: boolean;
  size?: number;
  className?: string;
}) {
  const content = (
    <div className="flex flex-row gap-2">
      <img src={team.logo} alt={team.name} width={size} className="rounded" />
      <div className={className}>{team.name}</div>
    </div>
  );
  if (link) {
    return <Link href={`/teams/${team.short_name}`}>{content}</Link>;
  }
  return content;
}
