import Image from "next/image";
import Link from "next/link";
import { SidebarGroup } from "@/components/ui/sidebar";

export default function BTSHLogo() {
  return (
    <Link href="/" className="flex items-center gap-2">
      <Image src="/btsh-head.svg" alt="BTSH" width={36} height={36} />
      <SidebarGroup className="group-data-[collapsible=icon]:hidden">
        <h2 className="text-lg font-bold">BTSH</h2>
      </SidebarGroup>
    </Link>
  );
}
