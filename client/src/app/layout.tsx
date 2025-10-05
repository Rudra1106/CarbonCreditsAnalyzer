import type {Metadata} from 'next';
import './globals.css';
// If you want to avoid the TypeScript error, add this file:
// src/app/globals.css.d.ts
// declare module '*.css';
import { Toaster } from "@/components/ui/toaster";
import { Inter } from 'next/font/google';
import { cn } from '@/lib/utils';
import { Preloader } from '@/components/preloader';

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });

export const metadata: Metadata = {
  title: 'TerraCredit AI',
  description: 'Turn Your Farmland into Carbon Credits with AI-powered analysis.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth" suppressHydrationWarning>
      <body className={cn("min-h-screen bg-background font-sans antialiased", inter.variable)}>
          <Preloader />
          {children}
          <Toaster />
      </body>
    </html>
  );
}
