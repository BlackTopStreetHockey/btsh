import { useState, useCallback, useEffect } from "react";
import Ionicons from "@expo/vector-icons/Ionicons";
import { StyleSheet } from "react-native";

import ParallaxScrollView from "@/components/ParallaxScrollView";
import { ThemedText } from "@/components/ThemedText";
import { ThemedView } from "@/components/ThemedView";

import { View } from "react-native";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Text } from "@/components/ui/text";
import { PlayIcon, PauseIcon, SquareIcon } from "lucide-react-native";

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
export default function StatsScreen() {
  const [homeScore, setHomeScore] = useState(0);
  const [awayScore, setAwayScore] = useState(0);
  const [period, setPeriod] = useState(1);
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(false);

  const incrementScore = (team: "home" | "away") => {
    if (team === "home") {
      setHomeScore((prev) => prev + 1);
    } else {
      setAwayScore((prev) => prev + 1);
    }
  };

  const nextPeriod = () => {
    setPeriod((prev) => (prev < 3 ? prev + 1 : 1));
  };

  const toggleTimer = () => {
    setIsActive(!isActive);
  };

  const resetTimer = () => {
    setSeconds(0);
    setIsActive(false);
  };

  const formatTime = useCallback((totalSeconds: number) => {
    const minutes = Math.floor(totalSeconds / 60);
    const remainingSeconds = totalSeconds % 60;
    return `${minutes.toString().padStart(2, "0")}:${remainingSeconds
      .toString()
      .padStart(2, "0")}`;
  }, []);

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    if (isActive) {
      interval = setInterval(() => {
        setSeconds((seconds) => seconds + 1);
      }, 1000);
    } else if (!isActive && seconds !== 0 && interval) {
      clearInterval(interval);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isActive, seconds]);

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: "#D0D0D0", dark: "#353636" }}
      headerImage={
        <Ionicons size={310} name="timer" style={styles.headerImage} />
      }
    >
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">Referee</ThemedText>
      </ThemedView>

      <Card>
        <CardHeader>
          <CardTitle className="text-center text-2xl font-bold">
            Score Sheet
          </CardTitle>
        </CardHeader>
        <CardContent>
          <View className="flex flex-row native:flex-col justify-between items-center mb-6 gap-4">
            <View className="text-center flex flex-col gap-2">
              <Text className="text-xl font-semibold mb-2">Home:</Text>
              <Select>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select a team" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>Division 1</SelectLabel>
                    <SelectItem value="fuzz" label="Fuzz" />
                    <SelectItem value="lbs" label="Lbs" />
                    <SelectItem value="vert" label="Vertz" />
                    <SelectItem value="ck" label="Cobra Kai" />
                    <SelectItem value="fk" label="Fresk Kills" />
                  </SelectGroup>
                </SelectContent>
              </Select>
              <Text className="text-4xl font-bold mb-2">{homeScore}</Text>
              <Button size="sm" onPress={() => incrementScore("home")}>
                <Text>+Goal</Text>
              </Button>
            </View>
            <View className="text-center flex flex-col gap-2">
              <Text className="text-3xl font-bold mb-2">Period {period}</Text>
              <Text className="text-3xl mb-2">{formatTime(seconds)}</Text>
              <Text className="text-sm text-gray-400 mb-2">
                {formatTime(1500 - seconds)}
              </Text>
              <View className="flex flex-row gap-2">
                <Button onPress={toggleTimer} variant="outline" size="icon">
                  {isActive ? (
                    <PauseIcon className="h-4 w-4" />
                  ) : (
                    <PlayIcon className="h-4 w-4" />
                  )}
                </Button>
                <Button onPress={resetTimer} variant="outline" size="icon">
                  <SquareIcon className="h-4 w-4" />
                </Button>
              </View>
              <Button size="sm" onPress={nextPeriod}>
                <Text>Next Period</Text>
              </Button>
            </View>
            <View className="text-center">
              <Text className="text-xl font-semibold mb-2">Away Team</Text>
              <Select>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select a team" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>Division 1</SelectLabel>
                    <SelectItem value="fuzz" label="Fuzz" />
                    <SelectItem value="lbs" label="Lbs" />
                    <SelectItem value="vert" label="Vertz" />
                    <SelectItem value="ck" label="Cobra Kai" />
                    <SelectItem value="fk" label="Fresk Kills" />
                  </SelectGroup>
                </SelectContent>
              </Select>
              <Text className="text-4xl font-bold mb-2">{awayScore}</Text>
              <Button size="sm" onPress={() => incrementScore("away")}>
                <Text>+ Goal</Text>
              </Button>
            </View>
          </View>
          <View className="bg-muted p-4 rounded-lg">
            <Text className="font-semibold mb-2">Game Summary</Text>
            <Text>
              Home: {homeScore} - Away: {awayScore}
            </Text>
            <Text>Current Period: {period}</Text>
          </View>
        </CardContent>
      </Card>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  headerImage: {
    color: "#808080",
    bottom: -90,
    left: -35,
    position: "absolute",
  },
  titleContainer: {
    flexDirection: "row",
    gap: 8,
  },
});
