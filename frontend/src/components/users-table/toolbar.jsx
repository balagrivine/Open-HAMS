import { Input } from "@/components/ui/input";
import { DataTableViewOptions } from "./view-options";
import { Button } from "../ui/button";

export function DataTableToolbar({ table }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <div className=" flex flex-1 items-center space-x-2">
        <Input
          placeholder="Search Users..."
          value={table.getColumn("name")?.getFilterValue() ?? ""}
          onChange={(event) =>
            table.getColumn("name")?.setFilterValue(event.target.value)
          }
          className="w-full"
        />
        <Button variant="outline">Export</Button>
      </div>
      <DataTableViewOptions table={table} />
    </div>
  );
}
