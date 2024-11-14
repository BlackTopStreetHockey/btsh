import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Image from "next/image";
import Link from "next/link";
// Define the shape of our team data
interface Team {
  id: number;
  name: string;
  logo: string;
  jersey_colors?: string;
}

// Add this interface
interface ApiResponse {
  results: Team[];
}

// This is a Server Component
export default async function SchedulePage() {
  let response: ApiResponse;
  let teams: Team[] = [];
  let error: string | null = null;

  try {
    // Fetch data from the API
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/teams`, {
      next: { revalidate: 60 },
    });

    if (!res.ok) {
      throw new Error("Failed to fetch data");
    }

    response = await res.json();
    teams = response.results;
  } catch (e) {
    console.error(e);
    error = "Failed to load teams. Please try again later.";
  }

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Hockey League Teams</h1>

      {error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {teams.map((team) => (
            <Link href={`/teams/${team.id}`} key={team.id} className="no-underline hover:shadow-md">
              <Card key={team.id}>
                <CardHeader>
                <CardTitle>{team.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4">
                  <Image
                    src={team.logo}
                    alt={team.name}
                    width={100}
                    height={100}
                  />
                  <div className="flex flex-col justify-center gap-4">
                    {team.jersey_colors?.map((color) => (
                      <div
                        key={color}
                        className="w-8 h-8 rounded-full border"
                        style={{ backgroundColor: color }}
                      />
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
