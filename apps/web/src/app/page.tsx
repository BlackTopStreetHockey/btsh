import ScheduleCarousel from "@/components/schedule/schedule-carousel";
import Socials from "@/components/navigation/socials";
export default function Home() {
  return (
    <div>
      <div className="text-3xl font-bold text-center my-4">
        Black Top Street Hockey
      </div>
      <ScheduleCarousel />

      <Socials />
    </div>
  );
}
