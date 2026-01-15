/**
 * Header Component
 *
 * 상단 네비게이션 헤더
 * - 로고 영역
 * - 사용자 프로필 영역
 *
 * @example
 * <Header />
 */

import React from 'react';
import { Bell, User, ChevronDown } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="fixed top-0 left-0 right-0 h-16 bg-white border-b border-slate-200 z-50">
      <div className="h-full px-6 flex items-center justify-between">
        {/* 로고 영역 */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-violet-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">TMS</span>
          </div>
          <h1 className="text-lg font-bold text-slate-900">차세대 HRIS</h1>
        </div>

        {/* 우측 액션 영역 */}
        <div className="flex items-center gap-4">
          {/* 알림 아이콘 */}
          <button
            className="relative p-2 hover:bg-slate-100 rounded-lg transition-colors"
            aria-label="알림"
          >
            <Bell size={20} className="text-slate-600" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          {/* 사용자 프로필 */}
          <button className="flex items-center gap-2 px-3 py-1.5 hover:bg-slate-100 rounded-lg transition-colors">
            <div className="w-8 h-8 bg-slate-200 rounded-full flex items-center justify-center">
              <User size={16} className="text-slate-600" />
            </div>
            <div className="hidden md:block text-left">
              <p className="text-sm font-semibold text-slate-900">관리자</p>
              <p className="text-xs text-slate-500">admin@tms.com</p>
            </div>
            <ChevronDown size={16} className="text-slate-400" />
          </button>
        </div>
      </div>
    </header>
  );
};
