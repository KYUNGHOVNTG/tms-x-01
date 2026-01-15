/**
 * Sidebar Component
 *
 * 사이드바 네비게이션
 * - 넓이: 접힘 상태 64px, 펼침 상태 200px
 * - Zustand로 상태 관리
 *
 * @example
 * <Sidebar />
 */

import React from 'react';
import { Home, Users, Settings, FileText, ChevronLeft, ChevronRight } from 'lucide-react';
import { useMenuStore } from '@/store/useMenuStore';
import { Link, useLocation } from 'react-router-dom';

interface MenuItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  path: string;
}

const menuItems: MenuItem[] = [
  { id: 'home', label: '홈', icon: <Home size={20} />, path: '/' },
  { id: 'legacy-test', label: '레거시 테스트', icon: <FileText size={20} />, path: '/legacy-test' },
  { id: 'users', label: '사용자', icon: <Users size={20} />, path: '/users' },
  { id: 'settings', label: '설정', icon: <Settings size={20} />, path: '/settings' },
];

export const Sidebar: React.FC = () => {
  const { isSidebarOpen, toggleSidebar } = useMenuStore();
  const location = useLocation();

  return (
    <aside
      className={`
        fixed left-0 top-16 h-[calc(100vh-4rem)]
        bg-white border-r border-slate-200
        transition-all duration-300 ease-in-out
        ${isSidebarOpen ? 'w-[200px]' : 'w-16'}
        z-40
      `}
    >
      {/* 토글 버튼 */}
      <button
        onClick={toggleSidebar}
        className="absolute -right-3 top-6 w-6 h-6 bg-white border border-slate-200 rounded-full flex items-center justify-center hover:bg-slate-50 transition-colors shadow-sm"
        aria-label={isSidebarOpen ? '사이드바 닫기' : '사이드바 열기'}
      >
        {isSidebarOpen ? <ChevronLeft size={14} /> : <ChevronRight size={14} />}
      </button>

      {/* 메뉴 리스트 */}
      <nav className="pt-6">
        <ul className="space-y-1 px-2">
          {menuItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <li key={item.id}>
                <Link
                  to={item.path}
                  className={`
                    flex items-center gap-3 px-3 py-2.5 rounded-lg
                    transition-all duration-200
                    ${isActive
                      ? 'bg-indigo-50 text-indigo-600 font-semibold'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                    }
                    ${!isSidebarOpen && 'justify-center'}
                  `}
                  title={!isSidebarOpen ? item.label : ''}
                >
                  <span className="flex-shrink-0">{item.icon}</span>
                  {isSidebarOpen && (
                    <span className="text-sm whitespace-nowrap">{item.label}</span>
                  )}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
};
