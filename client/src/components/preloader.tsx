"use client";

import { useState, useEffect } from 'react';

export function Preloader() {
  const [showLoader, setShowLoader] = useState(true);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    if (isMounted) {
      const timer = setTimeout(() => {
        setShowLoader(false);
      }, 3000); // Duration of the loader + animation

      return () => clearTimeout(timer);
    }
  }, [isMounted]);

  if (!isMounted || !showLoader) {
    return null;
  }
  
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-background slide-out-up">
      <div className="slide-in-text">
        <div className="text-2xl font-medium tracking-tight">
          Rooted in Land, Rising in Value
        </div>
      </div>
    </div>
  );
}
