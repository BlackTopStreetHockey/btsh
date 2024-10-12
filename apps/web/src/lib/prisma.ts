// /lib/prisma.ts
import { PrismaClient } from '@prisma/client';

declare global {
  let prisma: PrismaClient | undefined;
}

let prisma: PrismaClient;

if (process.env.NODE_ENV === 'production') {
  prisma = new PrismaClient();
}

export default prisma;
