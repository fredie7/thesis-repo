import { createSlice } from "@reduxjs/toolkit";

interface ToggleState {
  sidebarVisible: boolean;
}

const initialState: ToggleState = {
  sidebarVisible: false,
};

export const toggleSlice = createSlice({
  name: "toggle",
  initialState,
  reducers: {
    toggleSidebar: (state) => {
      state.sidebarVisible = !state.sidebarVisible;
    },
    closeSidebar: (state) => {
      state.sidebarVisible = false;
    },
    openSidebar: (state) => {
      state.sidebarVisible = true;
    },
  },
});

export const { toggleSidebar, closeSidebar, openSidebar } = toggleSlice.actions;

export default toggleSlice.reducer;
