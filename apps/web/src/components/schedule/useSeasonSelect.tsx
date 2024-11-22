import { useSeasons } from "@/hooks/requests/useSeasons";
import { useSelect } from "../ui/hooks/useSelect"


export const useSeasonSelect = ({
  initialSelectedValue,
  defaultActive=true
}: {
  initialSelectedValue?: string | number,
  defaultActive?: boolean
}) => {
  const { seasons, loading } = useSeasons({});

  let defaultSeason: number | string | undefined;
  if (!!initialSelectedValue) {
    defaultSeason = initialSelectedValue;
  } else if (!!defaultActive) {
    const activeSeason = seasons?.find(s => s.is_current);
    if (!!activeSeason) {
      defaultSeason = activeSeason.id
    } else {
      const futureSeason = seasons?.find(s => s.is_future);
      if (!!futureSeason) {
        defaultSeason = futureSeason.id
      }
    }
  }

  const { select, selectedValue } = useSelect({
    initialSelectedValue: defaultSeason,
    options: seasons?.map(s => ({label: s.year, value: s.id})) || [],
    isLoading: loading,
    placeholder: 'Select Season...'
  });

  const selectedSeason = seasons?.find(s => s.id === selectedValue);

  return {
    select,
    selectedSeason,
    selectedValue,
    seasons
  }
}