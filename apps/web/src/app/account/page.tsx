"use client";

import { useState } from "react";
import { Check, ChevronsUpDown, Loader2, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "@/components/ui/command";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { useToast } from "@/hooks/use-toast";
import { useTeams } from "@/hooks/requests/useTeams";

export default function AccountSettings() {
  const [isLoading, setIsLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const { teams, loading, error } = useTeams();
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);
  const { toast } = useToast();

  const [formData, setFormData] = useState({
    name: "Alex Johnson",
    email: "alex.johnson@company.com",
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleAvatarUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      // Handle file upload logic here
      toast({
        title: "Avatar updated",
        description: "Your profile picture has been successfully updated.",
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000));

    toast({
      title: "Settings updated",
      description: "Your account settings have been updated successfully.",
    });

    setIsLoading(false);
  };

  return (
    <Card className="my-10">
      <CardHeader>
        <CardTitle>Account Settings</CardTitle>
        <CardDescription>
          Update your account information and preferences.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="space-y-4">
            <div className="flex items-center gap-x-6">
              <Avatar className="h-20 w-20">
                <AvatarImage src="/placeholder.svg" alt={formData.name} />
                <AvatarFallback>AJ</AvatarFallback>
              </Avatar>
              <div>
                <Label htmlFor="avatar-upload" className="cursor-pointer">
                  <div className="flex items-center gap-x-2 text-sm text-muted-foreground hover:text-foreground transition-colors">
                    <Upload className="h-4 w-4" />
                    Change avatar
                  </div>
                </Label>
                <Input
                  id="avatar-upload"
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={handleAvatarUpload}
                />
                <p className="text-[0.8rem] text-muted-foreground mt-1">
                  JPG, GIF or PNG. Max size of 2MB.
                </p>
              </div>
            </div>

            <div className="grid gap-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleInputChange}
              />
            </div>

            <div className="grid gap-2">
              <Label>Team</Label>
              {loading && <Loader2 className="h-4 w-4 animate-spin" />}
              {!loading && !error && (
                <Popover open={open} onOpenChange={setOpen}>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      role="combobox"
                      aria-expanded={open}
                      className="justify-between"
                    >
                      {selectedTeam?.name || "Select your current team"}
                      <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-[200px] p-0">
                    <Command>
                      <CommandInput placeholder="Search team..." />
                      <CommandEmpty>No team found.</CommandEmpty>
                      <CommandGroup>
                        {teams?.map((team: Team) => (
                          <CommandItem
                            key={team.id}
                            onSelect={() => {
                              setSelectedTeam(team);
                              setOpen(false);
                            }}
                          >
                            <Check
                              className={cn(
                                "mr-2 h-4 w-4",
                                selectedTeam?.id === team.id
                                  ? "opacity-100"
                                  : "opacity-0",
                              )}
                            />
                            {team.name}
                          </CommandItem>
                        ))}
                      </CommandGroup>
                    </Command>
                  </PopoverContent>
                </Popover>
              )}

              {teams?.length === 0 && <p className="text-red-500">No teams found</p>}
              {<p className="text-blue-500">{teams?.length} teams found</p>}
              {error && <p className="text-red-500">{error}</p>}
            </div>
          </div>

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Saving changes...
              </>
            ) : (
              "Save changes"
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
