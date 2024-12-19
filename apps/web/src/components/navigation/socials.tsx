import { Facebook, Instagram, Twitter } from "lucide-react";
import Link from "next/link";
export default function Socials() {
  const socialLinks = [
    {
      url: "https://www.facebook.com/groups/blacktopstreethockey",
      label: "Facebook",
      icon: Facebook,
    },
    {
      url: "https://www.instagram.com/btsh_official/",
      label: "Instagram",
      icon: Instagram,
    },
    { url: "https://twitter.com/BTSH/", label: "X", icon: Twitter },
  ];
  return (
    <div className="flex gap-4 justify-center my-4">
      {socialLinks.map(({ url, label, icon: Icon }) => (
        <Link key={label} href={url} passHref>
          <Icon />
        </Link>
      ))}
    </div>
  );
}
