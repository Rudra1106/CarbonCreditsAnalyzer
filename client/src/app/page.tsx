import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";
import { Hero } from "@/components/landing/hero";
import { HowItWorks } from "@/components/landing/how-it-works";
import { Features } from "@/components/landing/features";
import { Faq } from "@/components/landing/faq";
import { Suspense } from "react";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <Suspense>
        <Header />
      </Suspense>
      <main className="flex-1">
        <Hero />
        <HowItWorks />
        <Features />
        <Faq />
      </main>
      <Footer />
    </div>
  );
}
