import Ionicons from "@expo/vector-icons/Ionicons";
import { StyleSheet, Text, View, Image } from "react-native";

import ParallaxScrollView from "@/components/ParallaxScrollView";
import { ThemedText } from "@/components/ThemedText";
import { ThemedView } from "@/components/ThemedView";

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

      <View className="flex flex-row bg-red-500 p-2" >
        <Text>Open up App.js to start working on your app!</Text>
      </View>

      <View className="flex flex-row gap-2">
        <ThemedText>Week 1</ThemedText>
        <View className="grid grid-cols-3 col-span-3 w-40 bg-ls-level-1 dark:bg-ds-level-1 border-r border-r-transparent border-l-2 border-l-ls-200 dark:border-l-ds-200 group-hover:bg-white group-hover:dark:bg-ds-level-2 group-hover:border-r group-hover:border-r-ls-200 group-hover:dark:border-r-transparent">
          <View className="grid col-span-3 gap-y-1.5 mx-2 my-2">
            <View className="grid grid-cols-3 items-center">
              <View className="flex items-center col-span-2">
                <Image
                  alt="Los Angeles Rams logo"
                  src="https://static.www.nfl.com/q_auto,f_auto,dpr_2.0/league/api/clubs/logos/LA"
                  className="w-5 lg:w-6 mr-1"
                />

                <Text className="display-7 lg:display-6 italic text-ls-800 dark:text-white">
                  LAR
                </Text>
              </View>
              <View className="col-span-1 inline-flex justify-end items-center display-6 text-ls-600 dark:text-ds-600">
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
                <Text className="display-7 lg:display-6 italic text-ls-800 dark:text-white">
                  CHI
                </Text>
              </View>
              <View className="col-span-1 inline-flex justify-end items-center display-6 text-black dark:text-white">
                <Text>24</Text>
              </View>
            </View>
          </View>
          <View className="grid col-span-3 bg-ls-100 dark:bg-ls-800 border-b border-ls-100 dark:border-ls-800">
            <View className="grid grid-cols-2 lg:grid-cols-3 mx-3 my-1 items-center">
              <View className="col-span-2 misc-1 font-stats font-medium text-ls-600 dark:text-ds-600 group-data-[variant=PRE]:pr-2 group-data-[variant=LIVE]:pr-2 whitespace-nowrap">
                <Text>FINAL</Text>
              </View>
            </View>
          </View>
        </View>
      </View>
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
