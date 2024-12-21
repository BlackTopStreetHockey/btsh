"use client";

import { FC, useState } from "react";
import Link from "next/link";
import Image from "next/image";

import { getTeam } from "@/data/getTeam";
import { standings } from "@/data/2024/standings-2024";
import { Button } from "@/components/ui/button";

const Divisions: FC = () => (
  <div className="flex flex-col text-center gap-2">
    <div className="text-red-800 bg-red-200 font-mono font-semibold px-2 rounded-full">
      ♠️ Division 1
    </div>
    <div className="text-pink-800 bg-pink-200 font-mono font-semibold px-2 rounded-full">
      ♣️ Division 2
    </div>
    <div className="text-purple-800 bg-purple-200 font-mono font-semibold px-2 rounded-full">
      ♦️ Division 3
    </div>
    <div className="text-blue-800 bg-blue-200 font-mono font-semibold px-2 rounded-full">
      ❤️ Division 4
    </div>
  </div>
);

const getColor = (division: number) => {
  switch (division) {
    case 1:
      return { color: "text-red-800 bg-red-200", symbol: "♠️" };
    case 2:
      return { color: "text-pink-800 bg-pink-200", symbol: "♣️" };
    case 3:
      return { color: "text-purple-800 bg-purple-200", symbol: "♦️" };
    case 4:
      return { color: "text-blue-800 bg-blue-200", symbol: "❤️" };
  }
};

export const sortRanker = (a: any, b: any, isLeagueSort: boolean) => {
  // sort by the entire league or within the division
  let diff = isLeagueSort ? 0 : a[1].div - b[1].div;

  // then, sort by points, or wins if points are even
  diff = diff || b[1].points - a[1].points || b[1].wins - a[1].wins;

  // then sort by these random one-offs which represent tie-breakers for head-to-head games
  // if (!diff) {
  //   if (a[0] == 'WTP' && b[0] == 'GANK') { return 1 }
  //   if (a[0] == 'FUZZ' && b[0] == 'CK') { return 1 }
  //   if (a[0] == 'FK'   && b[0] == 'LBS') { return -1 }
  // }

  // finally, use goals diff if nothing else
  return diff || b[1].diff - a[1].diff;
};

const Standings: FC = () => {
  const [sort, setSort] = useState("league");
  const isLeagueSort = sort === "league";

  return (
    <div className="text-black py-8">
      <div className="container mx-auto flex flex-col items-start md:flex-row my-12 md:my-24">
        <div className="flex flex-col w-full sticky md:top-36 lg:w-1/4 mt-2 md:mt-12 px-4">
          <div className="text-gray-500 uppercase tracking-loose font-mono text-black">
            2024
          </div>
          <h1 className="text-3xl md:text-4xl leading-normal md:leading-relaxed mb-2 text-black">
            Standings
          </h1>
          <p className="text-black mb-3">
            There are 4 Divisions. Division Winners Move up. Division Losers
            move down.
          </p>

          <Divisions />

          <div className="flex flex-col gap-2 my-2">
            <h2 className="text-black">Sort by:</h2>
            {isLeagueSort ? (
              <Button
                onClick={() => setSort("division")}
                className="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Divisions
              </Button>
            ) : (
              <Button
                onClick={() => setSort("league")}
                className="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                League
              </Button>
            )}
          </div>

          {/* <div className="flex flex-col gap-2 my-2">
              <Heading color="text">View:</Heading>
              <Link href="/playoffs" passHref>
                <Button variant="secondary" color="white">
                  Playoff Bracket
                </Button>
              </Link>
            </div> */}
        </div>

        <div className="ml-0 lg:w-3/4">
          <div className="container mx-auto w-full h-full">
            <div className="relative wrap overflow-hidden p-2 h-full">
              <div className="flex w-full flex-col">
                <table className="mx-auto max-w-4xl w-full whitespace-nowrap rounded-lg bg-white divide-y divide-gray-300 overflow-hidden">
                  <thead className="bg-gray-50">
                    <tr className="text-gray-600">
                      <th className="text-sm uppercase px-3 py-2 text-left">
                        <Link href="#" className="cursor-pointer">
                          Team
                        </Link>
                      </th>
                      <th className="text-sm uppercase px-3 py-2 text-center">
                        <Link href="#" className="cursor-pointer">
                          Points
                        </Link>
                      </th>
                      <th className="text-sm uppercase px-3 py-2 text-center">
                        <Link href="#" className="cursor-pointer">
                          Div
                        </Link>
                      </th>
                      <th className="text-sm uppercase px-3 py-2">📈📉</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {Object.entries(standings)
                      .filter((t: any) => t[0] !== "BTSH")
                      .sort((a: any, b: any) => sortRanker(a, b, isLeagueSort))
                      .map((t: any, idx: number) => {
                        const sn = t[0];
                        const data = t[1];
                        const team = getTeam(sn);

                        return (
                          <tr
                            key={t}
                            className={`team ${idx! % 5 && !isLeagueSort ? "bg-gray-50" : "bg-white"}`}
                          >
                            <td className="name">
                              <div className="flex items-center">
                                <div className="w-8 h-8 ml-2">
                                  <Image
                                    width="32"
                                    height="32"
                                    alt="User avatar"
                                    src={
                                      team.logoUrl
                                        ? team.logoUrl
                                        : "/btsh-head.svg"
                                    }
                                  />
                                </div>
                                <div className="flex flex-col ml-2">
                                  <Link
                                    href={`/teams/${team.shortName}`}
                                    passHref
                                  >
                                    <span className="cursor-pointer text-blue-600">
                                      <span
                                        className={`${!isLeagueSort && "hidden"}`}
                                      >
                                        {idx + 1}:{" "}
                                      </span>
                                      {team.name}
                                    </span>
                                  </Link>
                                  <p className="text-gray-400 text-xs font-mono text-left">
                                    ({data.record.wins}-{data.record.losses}-
                                    {data.record.otLosses})
                                  </p>
                                </div>
                              </div>
                            </td>
                            <td className="points">
                              <p className="text-gray-400 text-sm font-semibold font-mono text-center tracking-wide p-2">
                                {data.points}
                              </p>
                            </td>
                            <td className="division text-center text-gray-400">
                              <span
                                className={`font-mono font-semibold px-2 rounded-full ${getColor(data.div)?.color}`}
                              >
                                {getColor(data.div)?.symbol}
                              </span>
                            </td>
                            <td className="change text-center">
                              <div
                                className={`ml-2 px-2 py-1 rounded text-white text-sm font-mono ${
                                  data.diff >= 0
                                    ? data.diff
                                      ? "bg-[#66AA66]"
                                      : "bg-[#CCC]"
                                    : "bg-[#FF8888]"
                                }`}
                              >
                                {data.diff}
                              </div>
                            </td>
                          </tr>
                        );
                      })}
                  </tbody>
                  <tfoot>
                    <tr>
                      <td
                        colSpan={5}
                        className="p-3 font-mono  text-sm text-gray-400"
                      >
                        Send any corrections to{" "}
                        <a
                          href="mailto:justin@btsh.org?subject=and%20they%20will%20be%20posted%20on%20facebook"
                          className="text-blue-500 hover:text-blue-600"
                        >
                          justin@btsh.org
                        </a>
                      </td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Standings;
