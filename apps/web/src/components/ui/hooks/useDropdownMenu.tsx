import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "../dropdown-menu";

export type DropdownOptions = {
  label: string;
  value: string;
  seperateAfter?: boolean;
  isSelected?: boolean;
  isDisabled?: boolean;
  isLabel?: boolean;
  onClick: () => void;
};

export const useDropdownMenu = ({
  trigger,
  options,
}: {
  trigger: React.ReactNode | JSX.Element | string;
  options: DropdownOptions[];
}) => {
  const dropdownMenu = (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <div className="cursor-pointer inline-block flex-row gap-2">
          {trigger}
        </div>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        {options.map((option, index) => (
          <div key={index}>
            {option.isLabel ? (
              <DropdownMenuLabel>{option.label}</DropdownMenuLabel>
            ) : (
              <DropdownMenuItem
                onClick={!option.isDisabled ? option.onClick : undefined}
                className={`${option.isSelected ? "bg-secondary" : ""} ${
                  option.isDisabled ? "cursor-not-allowed" : ""
                }`}
              >
                {option.label}
              </DropdownMenuItem>
            )}
            {option.seperateAfter && <DropdownMenuSeparator />}
          </div>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
  return {
    dropdownMenu,
  };
};
