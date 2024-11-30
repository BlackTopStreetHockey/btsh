import Link from "next/link";

export default function TeamName({
  team,
  link,
}: {
  team: Team;
  link?: boolean;
}) {
  const content = (
    <div className="flex flex-row gap-2">
      <img
        src={team.logo}
        alt={team.name}
        width={24}
        height={24}
        className="rounded"
      />
      <div className="text-sm">{team.name}</div>
    </div>
  );
  if (link) {
    return <Link href={`/teams/${team.short_name}`}>{content}</Link>;
  }
  return content;
}
