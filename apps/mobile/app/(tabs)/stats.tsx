import { useState } from "react";
import Ionicons from "@expo/vector-icons/Ionicons";
import { StyleSheet } from "react-native";

import ParallaxScrollView from "@/components/ParallaxScrollView";
import { ThemedText } from "@/components/ThemedText";
import { ThemedView } from "@/components/ThemedView";

import { View } from "react-native";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Text } from "@/components/ui/text";
import { Select, SelectItem } from "@/components/ui/select";
export default function StatsScreen() {
  const [homeScore, setHomeScore] = useState(0);
  const [awayScore, setAwayScore] = useState(0);
  const [period, setPeriod] = useState(1);

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

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: "#D0D0D0", dark: "#353636" }}
      headerImage={
        <Ionicons size={310} name="code-slash" style={styles.headerImage} />
      }
    >
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">Stats</ThemedText>
      </ThemedView>

      <Card>
        <CardHeader>
          <CardTitle className="text-center text-2xl font-bold">
            Score Sheet
          </CardTitle>
        </CardHeader>
        <CardContent>
          <View className="flex justify-between items-center mb-6">
            <View className="text-center">
              <Text className="text-xl font-semibold mb-2">Home Team</Text>
              <Select>
                <SelectItem value="1" label="1" />
                <SelectItem value="2" label="2" />
                <SelectItem value="3" label="3" />
              </Select>
              <Text className="text-4xl font-bold mb-2">{homeScore}</Text>
              <Button size="sm" onClick={() => incrementScore("home")}><Text>+1</Text></Button>
            </View>
            <View className="text-center">
              <Text className="text-3xl font-bold mb-2">Period {period}</Text>
              <Text className="text-xl mb-2">00:00</Text>
              <Button size="sm" onClick={nextPeriod}><Text>Next Period</Text></Button>
            </View>
            <View className="text-center">
              <Text className="text-xl font-semibold mb-2">Away Team</Text>
              <Text className="text-4xl font-bold mb-2">{awayScore}</Text>
              <Button size="sm" onClick={() => incrementScore("away")}><Text>+1</Text></Button>
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
