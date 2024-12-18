import { usePlaceholder, useRequest } from "..";

export const usePaginated = ({
  route,
  method = "GET",
  body = undefined,
  skip = false, // if true, won't fire request
  ...requestArgs
}) => {
  const response = usePlaceholder(
    useRequest({ route, method, body, skip, ...requestArgs }),
  );

  const pagination = "TODO this";
  return {
    ...response,
    pagination,
  };
};
