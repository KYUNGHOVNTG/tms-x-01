/**
 * MainLayout Component
 *
 * 메인 레이아웃 - Header, Sidebar, Content 영역 구성
 * - React Router Outlet 사용
 * - Zustand로 사이드바 상태 관리
 *
 * @example
 * <Route element={<MainLayout />}>
 *   <Route path="/" element={<HomePage />} />
 * </Route>
 */

import React from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { useMenuStore } from '@/store/useMenuStore';

export const MainLayout: React.FC = () => {
  const { isSidebarOpen } = useMenuStore();

  return (
    <div className="min-h-screen bg-slate-50">
      {/* 헤더 */}
      <Header />

      {/* 사이드바 */}
      <Sidebar />

      {/* 메인 콘텐츠 영역 */}
      <main
        className={`
          pt-16 min-h-screen
          transition-all duration-300 ease-in-out
          ${isSidebarOpen ? 'pl-[200px]' : 'pl-16'}
        `}
      >
        <div className="p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
};
