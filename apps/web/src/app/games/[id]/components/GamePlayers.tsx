import { useGamePlayers } from "@/hooks/requests/useGamePlayers";
import { groupBy } from "lodash";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../../../../components/ui/table";
// import { useGameGoals } from "@/hooks/requests/useGameGoals";

export const GamePlayers = ({ game }: { game: Game }) => {
  const { players, placeholder: playersPlaceholder } = useGamePlayers({
    gameId: game.id,
  });
  // const { goals, placeholder } = useGameGoals({ gameId: game.id });

  if (playersPlaceholder) return playersPlaceholder;
  const teamToPlayers = groupBy(
    players.filter((player: GamePlayer) => !player.is_goalie),
    "team.id",
  );
  const teamToGoalies = groupBy(
    players.filter((player: GamePlayer) => player.is_goalie),
    "team.id",
  );

  return (
    <div className="flex flex-col items-center">
      <div className="flex flex-row gap-8 align-stretch">
        {[game.away_team, game.home_team].map((team) => (
          <div key={team.id} className="flex flex-col gap-1">
            <div className="font-bold text-sm">{team.name}</div>
            <div className="flex flex-col">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Players</TableHead>
                    <TableHead></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {teamToPlayers[team.id].map((player: GamePlayer) => (
                    <TableRow key={player.id}>
                      <TableCell>{player.user.full_name}</TableCell>
                      <TableCell></TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Goalie</TableHead>
                    <TableHead></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {teamToGoalies[team.id].map((player: GamePlayer) => (
                    <TableRow key={player.id}>
                      <TableCell>{player.user.full_name}</TableCell>
                      <TableCell></TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
