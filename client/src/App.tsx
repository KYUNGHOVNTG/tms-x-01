/**
 * App Component
 *
 * React Router 설정
 * - MainLayout을 루트로 사용
 * - 홈("/")과 레거시 테스트("/legacy-test") 경로 설정
 */

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from './core/layout/MainLayout';
import { LegacyFrame } from './components/common/LegacyFrame';
import { LoadingOverlay } from './core/loading';

/**
 * 홈 페이지 컴포넌트
 */
const HomePage: React.FC = () => {
  return (
    <div className="max-w-7xl mx-auto">
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-4">
          차세대 HRIS 대시보드
        </h1>
        <p className="text-slate-600 mb-6">
          교살자 패턴(Strangler Pattern)을 활용한 레거시 시스템 마이그레이션 테스트 환경입니다.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-6 bg-indigo-50 rounded-xl border border-indigo-200">
            <h3 className="font-bold text-indigo-900 mb-2">새로운 시스템</h3>
            <p className="text-sm text-indigo-700">
              React 19, Tailwind CSS 4를 활용한 모던 UI
            </p>
          </div>
          <div className="p-6 bg-violet-50 rounded-xl border border-violet-200">
            <h3 className="font-bold text-violet-900 mb-2">레거시 통합</h3>
            <p className="text-sm text-violet-700">
              기존 시스템을 iframe으로 임베딩
            </p>
          </div>
          <div className="p-6 bg-emerald-50 rounded-xl border border-emerald-200">
            <h3 className="font-bold text-emerald-900 mb-2">점진적 마이그레이션</h3>
            <p className="text-sm text-emerald-700">
              단계적으로 기능을 이전
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

/**
 * 레거시 테스트 페이지 컴포넌트
 */
const LegacyTestPage: React.FC = () => {
  return (
    <div className="h-[calc(100vh-10rem)]">
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 mb-4">
        <h2 className="text-xl font-bold text-slate-900">
          레거시 시스템 테스트
        </h2>
        <p className="text-sm text-slate-600 mt-1">
          iframe으로 임베딩된 레거시 로그인 화면
        </p>
      </div>
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 h-[calc(100%-6rem)] overflow-hidden">
        <LegacyFrame
          src="/login.do"
          title="레거시 로그인 화면"
        />
      </div>
    </div>
  );
};

function App() {
  return (
    <>
      {/* 전역 로딩 오버레이 */}
      <LoadingOverlay />

      <BrowserRouter>
        <Routes>
          <Route element={<MainLayout />}>
            <Route index element={<HomePage />} />
            <Route path="/legacy-test" element={<LegacyTestPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;