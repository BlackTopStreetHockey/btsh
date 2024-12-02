import { teams } from "./teams";

const _find = (key: string, value: string) => {
  for (const team of teams) {
    for (const [k, v] of Object.entries(team)) {
      if (k === key && v === value) {
        return team;
      }
    }
  }
};

export const getTeam = (sn: string) => {
  return _find("shortName", sn);
};

const _findByDivision = (
  collection: Record<string, unknown>[],
  key: string,
  value: string,
): Record<string, unknown> | undefined => {
  for (const o of collection) {
    for (const [k, v] of Object.entries(o)) {
      if (k === key && v === value) {
        return o;
      }
      if (Array.isArray(v)) {
        const _o = _findByDivision(v, key, value);
        if (_o) {
          return { ..._o, division: o };
        }
      }
    }
  }
};

// Note: Less efficient than the above, but it's a one-off
export const getTeamByDivison = (sn: string) => {
  return _findByDivision(teams, "shortName", sn);
};
