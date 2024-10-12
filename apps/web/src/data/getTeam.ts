import teams from './teams';

const _findByDivision = (collection: any, key: string, value: string): any => {
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

const _find = (key: string, value: string): any => {
  for (const team of teams) {
    for (const [k, v] of Object.entries(team)) {
      if (k === key && v === value) {
        return team;
      }
    }
  }
};

export const excludes = [
  '3rd Lowest Ranked',
  '2nd Lowest Ranked',
  'Lowest Ranked',
  'Winner of 14/19',
  'Winner of 15/18',
  'Winner of 16/17',
  '19th Place',
  '18th Place',
  '17th Place',
  '16th Place',
  '15th Place',
  '14th Place',
  '13th Place',
  '12th Place',
  '11th Place',
  '10th Place',
  '9th Place',
  '8th Place',
  '7th Place',
  '6th Place',
  '5th Place',
  '4th Place',
  '3rd Place',
  '2nd Place',
  '1st Place',
  '8HR',
  '7HR',
  '6HR',
  '5HR',
  '4HR',
  '3HR',
  '2HR',
  '1HR',
];

export const getTeam = (sn: string) => {
  if (excludes.findIndex((e) => e == sn) !== -1) {
    return {
      name: sn,
    };
  }
  return _find('shortName', sn);
};

// Note: Less efficient than the above, but it's a one-off
export const getTeamByDivison = (sn: string) => {
  if (excludes.findIndex((e) => e == sn) !== -1) {
    return {
      name: sn,
    };
  }
  return _findByDivision(teams, 'shortName', sn);
};
