
import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";
import { cn } from "@/lib/utils";

export function MainLayout({ children, className }: { children: React.ReactNode, className?: string }) {
  return (
    <div className={cn("flex min-h-screen flex-col", className)}>
      <Header />
      <main className="flex-1">{children}</main>
      <Footer />
    </div>
  );
}
