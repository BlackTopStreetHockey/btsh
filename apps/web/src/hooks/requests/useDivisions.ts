import { usePlaceholder } from "./usePlaceholder";
import { useRequest } from "./useRequest";

export const useDivisions = ({}) => {
  const { data, placeholder, loading, error, ...rest } = usePlaceholder(
    useRequest({
      route: "divisions",
    }),
  );
  return {
    data,
    divisions: data?.results,
    placeholder,
    loading,
    error,
    ...rest,
  };
};
