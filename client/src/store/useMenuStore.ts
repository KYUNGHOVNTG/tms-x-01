/**
 * Menu Store (Zustand)
 *
 * 사이드바의 접힘/펼침 상태를 관리하는 전역 스토어
 */

import { create } from 'zustand';

interface MenuState {
  /** 사이드바 열림/닫힘 상태 */
  isSidebarOpen: boolean;
  /** 사이드바 토글 함수 */
  toggleSidebar: () => void;
  /** 사이드바 열기 */
  openSidebar: () => void;
  /** 사이드바 닫기 */
  closeSidebar: () => void;
}

export const useMenuStore = create<MenuState>((set) => ({
  isSidebarOpen: true,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  openSidebar: () => set({ isSidebarOpen: true }),
  closeSidebar: () => set({ isSidebarOpen: false }),
}));
