
"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Logo } from "@/components/shared/logo";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 max-w-screen-2xl items-center justify-between">
        <Logo />
        <div className="flex items-center gap-4">
          <nav className="hidden items-center gap-6 text-sm md:flex">
            <Link
              href="/#features"
              className="text-muted-foreground transition-colors hover:text-foreground"
            >
              Features
            </Link>
            <Link
              href="/chat"
              className="text-muted-foreground transition-colors hover:text-foreground"
            >
              Chat
            </Link>
            <Link
              href="/#faq"
              className="text-muted-foreground transition-colors hover:text-foreground"
            >
              FAQ
            </Link>
          </nav>
          <div className="flex items-center gap-2">
            <Button variant="ghost" asChild>
              <Link href="/signin">Sign In</Link>
            </Button>
            <Button asChild>
              <Link href="/analyze">Analyze My Land</Link>
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}
