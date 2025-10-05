import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function Hero() {
  return (
    <section className="bg-background text-foreground dark:bg-gray-900 py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="text-left mb-12">
            <p className="text-lg text-muted-foreground">The Growth Accelerator</p>
        </div>
        <h1 className="text-8xl font-bold tracking-tighter text-foreground sm:text-9xl md:text-[10rem] lg:text-[12rem] leading-none -ml-1">
          TerraCredit AI
        </h1>
        <div className="mt-16 flex justify-between items-end">
            <div>
                <p className="max-w-xs text-lg text-muted-foreground md:text-xl">
                Strategy, Design, Performance.
                </p>
            </div>
            <div>
                <p className="max-w-xs text-lg text-muted-foreground md:text-xl text-right">
                Global Creative & Technology Agency.
                </p>
            </div>
        </div>
      </div>
    </section>
  );
}
