

export const useNavigationLinks = () => {
  const links = [
    {
      id: 'schedule',
      label: 'Schedule',
      href: '/league-schedule'
    },
    {
      id: 'standings',
      label: 'Standings',
      href: '/standings'
    },
    {
      id: 'teams',
      label: 'Teams',
      href: '/teams'
    },
    {
      id: 'stats',
      label: 'Stats',
      href: '/stats'
    }
  ]
  return links;
}