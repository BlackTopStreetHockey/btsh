"use client";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { useRegistration } from "../../context/registration-context";
import { useTeams } from "@/hooks/requests/useTeams";

export default function RegistrationStep1() {
  const router = useRouter();
  const { formData, updateFormData } = useRegistration();
  const { data: teams, loading: teamsLoading } = useTeams();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Navigate to next step
    router.push("/register/2");
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Player Information</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Name Fields */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="firstName" className="text-base font-semibold">
                First Name <span className="text-red-500">*</span>
              </Label>
              <Input
                id="firstName"
                required
                value={formData.firstName}
                onChange={(e) => updateFormData({ firstName: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="lastName" className="text-base font-semibold">
                Last Name <span className="text-red-500">*</span>
              </Label>
              <Input
                id="lastName"
                required
                value={formData.lastName}
                onChange={(e) => updateFormData({ lastName: e.target.value })}
              />
            </div>
          </div>

          {/* Gender */}
          <div className="space-y-2">
            <Label className="text-base font-semibold">
              Gender <span className="text-red-500">*</span>
            </Label>
            <RadioGroup
              value={formData.gender}
              onValueChange={(value) => updateFormData({ gender: value })}
              className="flex flex-col space-y-2"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="female" id="female" />
                <Label htmlFor="female">Female</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="male" id="male" />
                <Label htmlFor="male">Male</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="non-binary" id="non-binary" />
                <Label htmlFor="non-binary">Non-binary</Label>
              </div>
            </RadioGroup>
          </div>

          {/* Position */}
          <div className="space-y-2">
            <Label htmlFor="position" className="text-base font-semibold">
              What position do you play? <span className="text-red-500">*</span>
            </Label>
            <Select
              value={formData.position}
              onValueChange={(value) => updateFormData({ position: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select a position" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="defense">Defense</SelectItem>
                <SelectItem value="forward">Forward</SelectItem>
                <SelectItem value="goalie">Goalie</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Team Selection */}
          <div className="space-y-2">
            <Label htmlFor="team" className="text-base font-semibold">
              2025 BTSH Team <span className="text-red-500">*</span>
            </Label>
            <Select
              value={formData.team}
              onValueChange={(value) => updateFormData({ team: value })}
            >
              <SelectTrigger className="w-full">
                <SelectValue
                  placeholder={
                    teamsLoading ? "Loading teams..." : "Select your team"
                  }
                />
              </SelectTrigger>
              <SelectContent>
                {teams &&
                  teams?.results.map((team: Team) => (
                    <SelectItem key={team.id} value={team.short_name}>
                      {team.name}
                    </SelectItem>
                  ))}
                {!teams && <SelectItem value="NA">No teams found</SelectItem>}
              </SelectContent>
            </Select>
            {teamsLoading && (
              <p className="text-sm text-muted-foreground">Loading teams...</p>
            )}
          </div>

          {/* Location */}
          <div className="space-y-2">
            <Label htmlFor="location" className="text-base font-semibold">
              Where do you live? <span className="text-red-500">*</span>
            </Label>
            <Input
              id="location"
              required
              value={formData.location}
              onChange={(e) => updateFormData({ location: e.target.value })}
            />
          </div>

          {/* League Help */}
          <div className="space-y-4">
            <Label className="text-base font-semibold">
              I care about the League and am interested in helping out with:{" "}
              <span className="text-red-500">*</span>
            </Label>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="reffing"
                  checked={formData.helpingInterests.includes("reffing")}
                  onCheckedChange={(checked) => {
                    if (checked) {
                      updateFormData({
                        helpingInterests: [
                          ...formData.helpingInterests,
                          "reffing",
                        ],
                      });
                    } else {
                      updateFormData({
                        helpingInterests: formData.helpingInterests.filter(
                          (i) => i !== "reffing"
                        ),
                      });
                    }
                  }}
                />
                <Label htmlFor="reffing">Reffing (paid)</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="opening-closing"
                  checked={formData.helpingInterests.includes(
                    "opening-closing"
                  )}
                  onCheckedChange={(checked) => {
                    if (checked) {
                      updateFormData({
                        helpingInterests: [
                          ...formData.helpingInterests,
                          "opening-closing",
                        ],
                      });
                    } else {
                      updateFormData({
                        helpingInterests: formData.helpingInterests.filter(
                          (i) => i !== "opening-closing"
                        ),
                      });
                    }
                  }}
                />
                <Label htmlFor="opening-closing">Opening/Closing (paid)</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="other"
                  checked={formData.helpingInterests.includes("other")}
                  onCheckedChange={(checked) => {
                    if (checked) {
                      updateFormData({
                        helpingInterests: [
                          ...formData.helpingInterests,
                          "other",
                        ],
                      });
                    } else {
                      updateFormData({
                        helpingInterests: formData.helpingInterests.filter(
                          (i) => i !== "other"
                        ),
                      });
                    }
                  }}
                />
                <Label htmlFor="other">
                  Some other capacity that I&apos;m good at
                </Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="next-year"
                  checked={formData.helpingInterests.includes("next-year")}
                  onCheckedChange={(checked) => {
                    if (checked) {
                      updateFormData({
                        helpingInterests: [
                          ...formData.helpingInterests,
                          "next-year",
                        ],
                      });
                    } else {
                      updateFormData({
                        helpingInterests: formData.helpingInterests.filter(
                          (i) => i !== "next-year"
                        ),
                      });
                    }
                  }}
                />
                <Label htmlFor="next-year">Sorry, maybe next year</Label>
              </div>
            </div>
          </div>

          {/* Other Skills */}
          <div className="space-y-2">
            <Label htmlFor="otherSkills" className="text-base font-semibold">
              I&apos;d like to help! I&apos;m good at:
            </Label>
            <Textarea
              id="otherSkills"
              value={formData.otherSkills}
              onChange={(e) => updateFormData({ otherSkills: e.target.value })}
              placeholder="Share your skills (handyperson skills, web design, etc.)"
            />
          </div>

          {/* Party Theme */}
          <div className="space-y-2">
            <Label htmlFor="partyTheme" className="text-base font-semibold">
              Theme ideas for the 2024 mid-season party?!
            </Label>
            <Textarea
              id="partyTheme"
              value={formData.partyTheme}
              onChange={(e) => updateFormData({ partyTheme: e.target.value })}
              placeholder="Share your theme ideas"
            />
          </div>

          <Button type="submit" className="w-full">
            Next
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
