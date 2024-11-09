"use client";
import { useParams } from 'next/navigation';


export default function Team() { 
  const { team } = useParams();
  return <p>Team: {team}</p>
}