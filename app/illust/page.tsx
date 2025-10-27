// app/tweet/page.tsx
import Image from "next/image";

export default function IllustPage() {
  return (
    <main
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        backgroundColor: "#000000ff",
      }}
    >
      <Image
        src="/img/illust0001.png"
        alt=""
        width={700}
        height={700}
        priority
      />
    </main>
  );
}
