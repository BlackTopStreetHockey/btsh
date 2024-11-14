"use client";
import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Image from 'next/image';
import Link from 'next/link';
import { Instagram } from 'lucide-react';

type Team = {
  id: number;
  name: string;
  short_name: string;
  logo: string;
  jersey_colors: string[];
  established: number | null;
  description: string | null;
  instagram_url: string | null;
};

export default function TeamPage() { 
  const { team } = useParams();
  const [teamData, setTeamData] = useState<Team | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTeam = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/team/${team}`);
        if (!response.ok) {
          throw new Error('Failed to fetch team data');
        }
        const data = await response.json();
        setTeamData(data);
      } catch (err) {
        console.error('Error fetching team:', err);
        setError('Failed to load team details');
      } finally {
        setLoading(false);
      }
    };

    fetchTeam();
  }, [team]);

  if (loading) {
    return (
      <div className="container mx-auto p-4">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-64 bg-gray-200 rounded mb-4"></div>
        </div>
      </div>
    );
  }

  if (error || !teamData) {
    return (
      <div className="container mx-auto p-4">
        <div className="text-red-500">
          {error || 'Team not found'}
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-3xl font-bold">{teamData.name}</CardTitle>
              <p className="text-muted-foreground">
                {teamData.short_name} • Est. {teamData.established}
              </p>
            </div>
            {teamData.instagram_url && (
              <Link 
                href={teamData.instagram_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="hover:text-blue-500"
              >
                <Instagram size={24} />
              </Link>
            )}
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="relative w-full h-24">
            <Image
              src={teamData.logo}
              alt={`${teamData.name} logo`}
              fill
              className="object-contain"
            />
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-2">Team Colors</h3>
            <div className="flex gap-2">
              {teamData.jersey_colors?.map((color, index) => (
                <span 
                  key={index}
                  className="px-3 py-1 rounded-full text-sm bg-gray-100"
                >
                  {color}
                </span>
              ))}
            </div>
          </div>

          {teamData.description && (
            <div>
              <h3 className="text-lg font-semibold mb-2">History</h3>
              <p className="text-muted-foreground">
                {teamData.description}
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}