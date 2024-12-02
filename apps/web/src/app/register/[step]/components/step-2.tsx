"use client";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { useRegistration } from "../../context/registration-context";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useTeams } from "@/hooks/requests/useTeams";

export default function RegistrationStep2() {
  const { formData, updateFormData } = useRegistration();
  const router = useRouter();
  const { data: teams } = useTeams({});

  // Redirect to step 1 if no data is present
  useEffect(() => {
    if (!formData.firstName || !formData.lastName) {
      router.push('/register/1');
    }
  }, [formData.firstName, formData.lastName, router]);

  // Add email handling
  useEffect(() => {
    if (formData.firstName && formData.lastName && !formData.email) {
      const generatedEmail = `${formData.firstName.toLowerCase()}.${formData.lastName.toLowerCase()}@btsh.org`;
      updateFormData({ email: generatedEmail });
    }
  }, [formData.firstName, formData.lastName, formData.email, updateFormData]);

  const formatHelpingInterests = (interests: string[]) => {
    if (interests.length === 0) return "None selected";
    return interests.map(interest => {
      switch(interest) {
        case "reffing": return "Reffing (paid)";
        case "opening-closing": return "Opening/Closing (paid)";
        case "other": return "Other capacity";
        case "next-year": return "Maybe next year";
        default: return interest;
      }
    }).join(", ");
  };

  const getTeamName = (shortName: string) => {
    const team = teams?.results.find(t => t.short_name === shortName);
    return team ? team.name : shortName;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Review Your Information</CardTitle>
        <CardDescription>
          Please review the following information before creating your account.
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        {formData.waiverAccepted && (
          <div className="bg-green-50 p-4 rounded-lg mb-4">
            <h3 className="font-semibold text-green-800">Waiver Accepted</h3>
            <p className="text-sm text-green-700">
              Signed by {formData.waiverSignature} on {new Date().toLocaleDateString()}
            </p>
          </div>
        )}

        <div>
          <h3 className="font-semibold">Name</h3>
          <p>{formData.fullName || "Not provided"}</p>
        </div>
        
        <div>
          <h3 className="font-semibold">Email</h3>
          <p>{formData.waiverEmail || formData.email || "Not provided"}</p>
          <p className="text-sm text-muted-foreground mt-1">
            This email will be used for your BTSH account
          </p>
        </div>

        <div>
          <h3 className="font-semibold">Gender</h3>
          <p className="capitalize">{formData.gender || "Not provided"}</p>
        </div>
        <div>
          <h3 className="font-semibold">Position</h3>
          <p className="capitalize">{formData.position || "Not provided"}</p>
        </div>
        <div>
          <h3 className="font-semibold">Team</h3>
          <p>{formData.team ? getTeamName(formData.team) : "Not provided"}</p>
        </div>
        <div>
          <h3 className="font-semibold">Location</h3>
          <p>{formData.location || "Not provided"}</p>
        </div>
        <div>
          <h3 className="font-semibold">League Help Interests</h3>
          <p>{formatHelpingInterests(formData.helpingInterests)}</p>
        </div>
        {formData.otherSkills && (
          <div>
            <h3 className="font-semibold">Other Skills</h3>
            <p>{formData.otherSkills}</p>
          </div>
        )}
        {formData.partyTheme && (
          <div>
            <h3 className="font-semibold">Party Theme Ideas</h3>
            <p>{formData.partyTheme}</p>
          </div>
        )}
      </CardContent>

      <CardFooter className="flex justify-between">
        <Link href="/register/1">
          <Button variant="outline">Back</Button>
        </Link>
        <Link href="/auth/signup">
          <Button>Create Account</Button>
        </Link>
      </CardFooter>
    </Card>
  );
}
