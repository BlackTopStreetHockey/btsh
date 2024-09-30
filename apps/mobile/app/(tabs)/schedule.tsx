import Ionicons from "@expo/vector-icons/Ionicons";
import { StyleSheet, View, Image } from "react-native";

import ParallaxScrollView from "@/components/ParallaxScrollView";
import { ThemedText } from "@/components/ThemedText";
import { ThemedView } from "@/components/ThemedView";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "~/components/ui/card";
import { Text } from "~/components/ui/text";

export default function ScheduleScreen() {
  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: "#DDDDDD", dark: "#333333" }}
      headerImage={
        <Ionicons
          name="calendar"
          style={styles.headerImage}
          size={310}
          color="black"
        />
      }
    >
      <ThemedView>
        <ThemedText type="title">Schedule</ThemedText>
      </ThemedView>
      <ThemedText type="subtitle">
        An 18 week schedule for the 2024 season.
      </ThemedText>

      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle>Week 1</CardTitle>
          <CardDescription>Opener: Lbs &mdash; Closer: WTP</CardDescription>
        </CardHeader>
        <CardContent>
          <View className="flex flex-row gap-2">
            <View className="grid grid-cols-3 col-span-3 w-40 bg-gray-100 border-r border-r-transparent border-l-2 border-l-gray-200 dark:border-l-gray-200 group-hover:bg-white">
              <View className="grid col-span-3 gap-y-2 mx-2 my-2">
                <View className="grid grid-cols-3 items-center">
                  <View className="flex items-center col-span-2">
                    <Image
                      alt="Los Angeles Rams logo"
                      src="https://static.www.nfl.com/q_auto,f_auto,dpr_2.0/league/api/clubs/logos/LA"
                      className="w-5 lg:w-6 mr-1"
                    />

                    <Text className="display-7 lg:display-6 italic text-gray-800 dark:text-white">
                      LAR
                    </Text>
                  </View>
                  <View className="col-span-1 inline-flex justify-end items-center display-6 text-gray-600 dark:text-gray-600">
                    <Text>18</Text>
                  </View>
                </View>
                <View className="grid grid-cols-3 items-center">
                  <View className="flex items-center col-span-2">
                    <Image
                      alt="Chicago Bears logo"
                      src="https://static.www.nfl.com/q_auto,f_auto,dpr_2.0/league/api/clubs/logos/CHI"
                      className="w-5 lg:w-6 mr-1"
                    />
                    <Text className="display-7 lg:display-6 italic text-gray-800 dark:text-white">
                      CHI
                    </Text>
                  </View>
                  <View className="col-span-1 inline-flex justify-end items-center display-6 text-black dark:text-white">
                    <Text>24</Text>
                  </View>
                </View>
              </View>
              <View className="grid col-span-3 bg-gray-100 dark:bg-gray-800 border-b border-gray-100 dark:border-gray-800">
                <View className="grid grid-cols-2 lg:grid-cols-3 mx-3 my-1 items-center">
                  <View className="col-span-2 font-mono font-medium text-gray-600 dark:text-gray-600 whitespace-nowrap">
                    <Text>FINAL</Text>
                  </View>
                </View>
              </View>
            </View>
          </View>
        </CardContent>
        <CardFooter>
          <Text>Card Footer</Text>
        </CardFooter>
      </Card>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  headerImage: {
    color: "#000000",
    bottom: -90,
    left: -30,
    position: "absolute",
  },
});
