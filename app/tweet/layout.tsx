import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Illust Page",
  description: "Simple illustration page",
};

export default function IllustLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
