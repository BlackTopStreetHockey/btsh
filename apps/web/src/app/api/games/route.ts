// /pages/api/games/index.ts
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

  if (req.method === 'GET') {
    const games = await prisma.game.findMany({
      include: {
        homeTeam: true,
        awayTeam: true,
        referee: true,
      },
      orderBy: {
        startTime: 'asc',
      },
    });
    return res.json(games);
  }
}
