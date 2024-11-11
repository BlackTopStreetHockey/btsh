import { useEffect, useState } from "react";
import { Button } from "../button"
import { DropdownOptions, useDropdownMenu } from "./useDropdownMenu"
import { ChevronDown } from "lucide-react";


export const useSelect = ({
  options,
  initialSelectedValue,
  placeholder='Select...',
  isLoading=false,
  updateOnInitialChange=true
}: {
  options?: DropdownOptions[],
  initialSelectedValue?: string | number,
  placeholder?: string,
  isLoading?: boolean,
  updateOnInitialChange?: boolean
}) => {
  const [selectedValue, setSelectedValue] = useState(initialSelectedValue);
  const selectedOption = options.find((o) => o.value === selectedValue);

  useEffect(() => {
    if (updateOnInitialChange) {
      setSelectedValue(initialSelectedValue);
    }
  }, [initialSelectedValue])

  const dropdownOptions = options?.map((o) => ({
    ...o,
    isSelected: o.value == selectedValue,
    onClick: () => {
      if (!!o.onClick) o.onClick(o.value);
      setSelectedValue(o.value);
    }
  }))
  const { dropdownMenu: select } = useDropdownMenu({
    trigger: (
      <Button variant='outline'>
        <div className='flex flex-row justify-between gap-4'>
          {!!selectedValue
            ? <div>{selectedOption?.label}</div> 
            : <div className='text-muted-foreground'>{placeholder}</div>
          }
          {isLoading 
            ? <div className="h-4 w-4 animate-spin rounded-full border-b-2 border-current border-t-transparent"></div>
            : <div className='text-muted-foreground'><ChevronDown/></div>
          }
        </div>
      </Button>
    ),
    options: dropdownOptions || []
  });


  return {
    select,
    selectedValue,
    selectedOption
  }
}