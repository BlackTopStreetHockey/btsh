// /pages/api/games/[id].ts
import { NextApiRequest, NextApiResponse } from 'next';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '../auth/[...nextauth]';
import prisma from '@/lib/prisma';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const session = await getServerSession(req, res, authOptions);
  
  if (!session) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const { id } = req.query;
  const gameId = parseInt(id as string);

  switch (req.method) {
    case 'GET':
      const game = await prisma.game.findUnique({
        where: { id: gameId },
        include: {
          homeTeam: true,
          awayTeam: true,
          referee: true,
        },
      });
      return res.json(game);

    case 'PUT':
      const { homeScore, awayScore, status } = req.body;
      const updatedGame = await prisma.game.update({
        where: { id: gameId },
        data: {
          homeScore,
          awayScore,
          status,
        },
      });
      return res.json(updatedGame);

    default:
      res.setHeader('Allow', ['GET', 'PUT']);
      return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
