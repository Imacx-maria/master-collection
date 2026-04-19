"use client";

import { SunMoon } from "lucide-react";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();

  return (
    <Button
      aria-label="Toggle theme"
      onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
      size="sm"
      type="button"
      variant="outline"
    >
      <SunMoon aria-hidden="true" className="size-3" />
      <span className="hidden sm:inline">Theme</span>
    </Button>
  );
}
