import { Player } from '../../../global';
import { teams } from '../teams';

const generateRandomName = (): string => {
  const maleFirstNames = ['John', 'Mike', 'Alex', 'Chris', 'David'];
  const femaleFirstNames = ['Jane', 'Emily', 'Sarah', 'Emma', 'Olivia'];
  const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'];
  const gender = Math.random() < 0.5 ? 'M' : 'F';
  const firstNames = gender === 'M' ? maleFirstNames : femaleFirstNames;
  return `${firstNames[Math.floor(Math.random() * firstNames.length)]} ${lastNames[Math.floor(Math.random() * lastNames.length)]}`;
};

const generateRandomNumber = (): number => {
  return Math.floor(Math.random() * 99) + 1;
};

const generatePlayersForTeam = (teamName: string, count: number): Player[] => {
  return Array.from({ length: count }, (_, index) => ({
    id: `${teamName.toLowerCase().replace(/\s+/g, '-')}-player-${index + 1}`,
    name: generateRandomName(),
    number: generateRandomNumber(),
    team: teamName,
  }));
};

export const mockPlayers: Player[] = teams.flatMap(team => generatePlayersForTeam(team.name, 15));

// Example usage:
// console.log(mockPlayers);

