import { teams } from "../teams";

const generateRandomName = (): string => {
  const maleFirstNames = ["John", "Mike", "Alex", "Chris", "David"];
  const femaleFirstNames = ["Jane", "Emily", "Sarah", "Emma", "Olivia"];
  const lastNames = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
  ];
  const gender = Math.random() < 0.5 ? "M" : "F";
  const firstNames = gender === "M" ? maleFirstNames : femaleFirstNames;
  return `${firstNames[Math.floor(Math.random() * firstNames.length)]} ${
    lastNames[Math.floor(Math.random() * lastNames.length)]
  }`;
};

const generateRandomNumber = (): number => {
  return Math.floor(Math.random() * 99) + 1;
};

const generatePlayersForTeam = (teamName: string, count: number): UserSeasonRegistration[] => {
  return Array.from({ length: count }, (_, index) => ({
    id: `${teamName.toLowerCase().replace(/\s+/g, "-")}-player-${index + 1}`,
    name: generateRandomName(),
    number: generateRandomNumber(),
    team: teamName,
    position: Math.random() < 0.5 ? "F" : "D",
    goals: generateRandomNumber(),
    gender: Math.random() < 0.5 ? "M" : "F",
    gp: generateRandomNumber(),
  }));
};

export const mockPlayers: UserSeasonRegistration[] = teams.flatMap((team) =>
  generatePlayersForTeam(team.name, 7),
);
