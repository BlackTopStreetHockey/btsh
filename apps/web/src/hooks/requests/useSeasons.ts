import { usePlaceholder } from "./usePlaceholder";
import { useRequest } from "./useRequest";

export const useSeasons = ({}) => {
  const { data, placeholder, loading, error, ...rest } = usePlaceholder(useRequest({
    route: 'seasons',
  }));
  return {
    data,
    seasons: data?.results,
    placeholder,
    loading,
    error,
    ...rest
  }
}