import ScheduleCarousel from "@/components/schedule/schedule-carousel";

export default function Home() {
  return (
    <div className="flex flex-col bg-white h-screen">
      <div className="text-3xl font-bold text-center my-4">
        Black Top Street Hockey
      </div>
      <ScheduleCarousel />
    </div>
  );
}
