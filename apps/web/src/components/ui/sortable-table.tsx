import React, { useMemo } from "react";
import { useTable, useSortBy } from "react-table";
import { cn } from "@/lib/utils";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./table";

interface SortableTableProps<T extends object> {
  data: T[];
  columns: any[];
  className?: string;
  defaultSortBy?: [{ id: string; desc: boolean }];
}

export function SortableTable<T extends object>({
  data,
  columns,
  className,
  defaultSortBy,
}: SortableTableProps<T>) {
  const memoizedColumns = useMemo(() => columns, [columns]);
  const memoizedData = useMemo(() => data, [data]);

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable(
      {
        columns: memoizedColumns,
        data: memoizedData,
        initialState: {
          sortBy: defaultSortBy || [],
        },
      },
      useSortBy,
    );

  return (
    <div className={cn("relative w-full overflow-auto", className)}>
      <Table {...getTableProps()} className="w-full caption-bottom text-sm">
        <TableHeader className="border-b">
          {headerGroups.map((headerGroup) => (
            <TableRow
              key={headerGroup.getHeaderGroupProps().key}
              {...headerGroup.getHeaderGroupProps()}
            >
              {headerGroup.headers.map((column: any) => (
                <TableHead
                  key={column.getHeaderProps(column.getSortByToggleProps()).key}
                  {...column.getHeaderProps(column.getSortByToggleProps())}
                  className="h-12 px-4 text-left align-middle font-medium text-muted-foreground hover:text-foreground"
                >
                  {column.render("Header")}
                  <span>
                    {column.isSorted
                      ? column.isSortedDesc
                        ? " 🔽"
                        : " 🔼"
                      : ""}
                  </span>
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody {...getTableBodyProps()} className="border-0">
          {rows.map((row) => {
            prepareRow(row);
            return (
              <TableRow
                key={row.getRowProps().key}
                {...row.getRowProps()}
                className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
              >
                {row.cells.map((cell) => {
                  return (
                    <TableCell
                      key={cell.column.id}
                      {...cell.getCellProps()}
                      className="align-middle"
                    >
                      {cell.render("Cell")}
                    </TableCell>
                  );
                })}
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
