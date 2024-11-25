import { usePlaceholder } from "./usePlaceholder";
import { useRequest } from "./useRequest";

export const useGame = ({ 
  id 
}: { 
  id: number | string
}) => {
  const { data, placeholder, ...rest } = usePlaceholder(useRequest({
    route: 'games/' + id,
    skip: !id
  }));
  return {
    data,
    game: data,
    placeholder,
    ...rest
  }
}