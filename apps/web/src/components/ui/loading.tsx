// A BTSH specifc loading spinner
import React from "react";

const Loading = () => {
  return (
    <div className="flex items-center justify-center">
      <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-current border-t-transparent"></div>
    </div>
  );
};

export default Loading;