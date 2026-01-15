/**
 * LegacyFrame Component
 *
 * 레거시 시스템을 iframe으로 임베딩하는 래퍼 컴포넌트
 * "교살자 패턴(Strangler Pattern)"을 위한 컴포넌트
 *
 * @example
 * <LegacyFrame src="/legacy/login.do" title="레거시 로그인" />
 */

import React from 'react';

interface LegacyFrameProps {
  /** iframe에 로드할 URL (로컬 Proxy 경로 가능) */
  src: string;
  /** iframe의 title 속성 (접근성) */
  title: string;
  /** 추가 CSS 클래스 (선택사항) */
  className?: string;
}

export const LegacyFrame: React.FC<LegacyFrameProps> = ({
  src,
  title,
  className = '',
}) => {
  return (
    <div className={`w-full h-full ${className}`}>
      <iframe
        src={src}
        title={title}
        className="w-full h-full border-0"
        sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
        loading="lazy"
      />
    </div>
  );
};
