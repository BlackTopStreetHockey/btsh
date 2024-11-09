import Loading from "@/components/ui/loading";
import ApiError from "@/components/ui/api-error";

export const usePlaceholder = ({ data, loading, error, ...requestState }, placeholderProps={}) => {
  /* "placeholder" can be a loading icon, an error message, or null if there is data */
  let placeholder;

  if (loading) {
    placeholder = <Loading {...placeholderProps} />;
  } else if (error) {
    placeholder = <ApiError error={error} />;
  }

  return {
    data,
    placeholder,
    ...requestState 
  }
}

