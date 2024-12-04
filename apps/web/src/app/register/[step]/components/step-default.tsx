import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from "@/components/ui/card";

export default function RegistrationStep2() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Registration</CardTitle>
        <CardDescription>
          You&apos;ve found an interesting league. Please register to join us.
        </CardDescription>
      </CardHeader>

      <CardFooter>
        <Link href="/auth/signup">
          <Button>Create Account</Button>
        </Link>

        <Link href="/">
          <Button>Back to Homepage</Button>
        </Link>
      </CardFooter>
    </Card>
  );
}
