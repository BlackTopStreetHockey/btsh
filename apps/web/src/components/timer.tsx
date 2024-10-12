"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { PlayCircleIcon, PauseCircleIcon, RefreshCcwIcon } from "lucide-react";

type Period = "1st" | "2nd" | "OT" | "SO";

export function Timer({ resetTimeouts }: { resetTimeouts: () => void }) {
  const [period, setPeriod] = useState<Period>("1st");
  const [totalSeconds, setTotalSeconds] = useState(20 * 60); // 20 minutes for regular periods
  const [timeLeft, setTimeLeft] = useState(totalSeconds);
  const [isActive, setIsActive] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const PERIOD_DURATION = 25 * 60;
  const OT_DURATION = 5 * 60;

  const switchPeriod = (newPeriod: Period) => {
    setPeriod(newPeriod);
    setIsActive(false);
    resetTimeouts();
    switch (newPeriod) {
      case "1st":
      case "2nd":
        setTotalSeconds(PERIOD_DURATION);
        setTimeLeft(PERIOD_DURATION);
        break;
      case "OT":
        setTotalSeconds(OT_DURATION);
        setTimeLeft(OT_DURATION);
        break;
      case "SO":
        setTotalSeconds(0);
        setTimeLeft(0);
        break;
    }
  };

  const toggleTimer = () => {
    setIsActive(!isActive);
  };

  const resetTimer = () => {
    setIsActive(false);
    setPeriod("1st");
    setTotalSeconds(PERIOD_DURATION);
    setTimeLeft(PERIOD_DURATION);
    resetTimeouts();
  };

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, "0")}:${remainingSeconds
      .toString()
      .padStart(2, "0")}`;
  };

  const handleTimeClick = () => {
    if (!isActive && period !== "SO") {
      setIsEditing(true);
      setTimeout(() => inputRef.current?.focus(), 0);
    }
  };

  const handleTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const [minutes, seconds] = e.target.value.split(":").map(Number);
    if (!isNaN(minutes) && !isNaN(seconds)) {
      const newTotalSeconds = minutes * 60 + seconds;
      setTotalSeconds(newTotalSeconds);
      setTimeLeft(newTotalSeconds);
    }
  };

  const handleTimeBlur = () => {
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleTimeBlur();
    }
  };

  const progress = period === "SO" ? 1 : 1 - timeLeft / totalSeconds;
  const circumference = 2 * Math.PI * 60; // 60 is the radius of the circle
  const strokeDashoffset = circumference * (1 - progress);

  // Calculate color based on progress
  const getColor = (progress: number) => {
    const hue = ((1 - progress) * 120).toString(10);
    return `hsl(${hue}, 100%, 50%)`;
  };

  const handlePeriodEnd = useCallback(() => {
    switch (period) {
      case "1st":
        setPeriod("2nd");
        setTimeLeft(PERIOD_DURATION);
        resetTimeouts();
        break;
      case "2nd":
        setPeriod("OT");
        setTimeLeft(OT_DURATION);
        resetTimeouts();
        break;
      case "OT":
        setPeriod("SO");
        setTimeLeft(0);
        resetTimeouts();
        break;
      case "SO":
        // Game ends after shootout
        break;
    }
  }, [period, setPeriod, setTimeLeft, resetTimeouts]);

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    if (isActive && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft((prevTime) => prevTime - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      setIsActive(false);
      handlePeriodEnd();
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isActive, timeLeft, handlePeriodEnd]);

  return (
    <>
      <div className="relative w-48 h-48">
        <svg className="w-full h-full">
          <circle
            cx="50%"
            cy="50%"
            r="60"
            fill="none"
            stroke="currentColor"
            strokeWidth="4"
            className="text-gray-200 dark:text-gray-700"
          />
          <circle
            cx="50%"
            cy="50%"
            r="60"
            fill="none"
            stroke={getColor(progress)}
            strokeWidth="4"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-300 ease-in-out"
            transform="rotate(-90 96 96)"
          />
        </svg>
        <div
          className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-3xl font-bold text-gray-800 dark:text-gray-200 cursor-pointer"
          onClick={handleTimeClick}
        >
          {period === "SO" ? (
            "Shootout"
          ) : isEditing ? (
            <input
              ref={inputRef}
              type="text"
              value={formatTime(timeLeft)}
              onChange={handleTimeChange}
              onBlur={handleTimeBlur}
              onKeyDown={handleKeyDown}
              className="w-full text-center bg-transparent outline-none"
            />
          ) : (
            formatTime(timeLeft)
          )}
        </div>
      </div>

      <div className="flex space-x-4 mb-4">
        <Button
          onClick={toggleTimer}
          variant="outline"
          disabled={isEditing || period === "SO"}
        >
          {isActive ? <PauseCircleIcon /> : <PlayCircleIcon />}
        </Button>
        <Button onClick={resetTimer} variant="outline" disabled={isEditing}>
          <RefreshCcwIcon className="h-4 w-4" />
        </Button>
        {period === "SO" && (
          <Button onClick={handlePeriodEnd} variant="outline">
            End Game
          </Button>
        )}
      </div>

      <div className="flex space-x-2 mb-4">
        {["1st", "2nd", "3rd", "OT", "SO"].map((p) => (
          <button
            key={p}
            onClick={() => switchPeriod(p as Period)}
            className={`w-8 h-8 rounded-full text-xs font-bold ${
              period === p
                ? "bg-primary text-primary-foreground"
                : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
            } ${period > p ? "bg-slate-500" : ""}`}
          >
            {p}
          </button>
        ))}
      </div>


    </>
  );
}
