import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface SeasonState {
  selectedSeasonId: number | null
  setSelectedSeason: (id: number) => void
}

export const useSeasonStore = create<SeasonState>()(
  persist(
    (set) => ({
      selectedSeasonId: null,
      setSelectedSeason: (id) => set({ selectedSeasonId: id }),
    }),
    {
      name: 'season-storage',
    }
  )
) 