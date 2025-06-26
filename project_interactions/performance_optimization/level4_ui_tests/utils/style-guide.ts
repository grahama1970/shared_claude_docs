/**
 * 2025 Style Guide Constants
 * Based on Vercel v0 aesthetics
 */

export const STYLE_GUIDE = {
  colors: {
    primary_start: '#4F46E5',
    primary_end: '#6366F1',
    secondary: '#6B7280',
    background: '#F9FAFB',
    accent: '#10B981',
    white: '#FFFFFF',
    error: '#EF4444',
    warning: '#F59E0B',
    dark: {
      background: '#111827',
      surface: '#1F2937',
      text: '#F9FAFB'
    }
  },
  spacing: {
    base: 8,
    scale: [8, 16, 24, 32, 40, 48, 56, 64, 72, 80]
  },
  animation: {
    duration_min: 150,
    duration_max: 300,
    fps_target: 60,
    easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
  },
  typography: {
    font_family: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
    weights: {
      regular: 400,
      medium: 500,
      semibold: 600,
      bold: 700
    },
    sizes: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem'
    },
    line_heights: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75
    }
  },
  border_radius: {
    none: 0,
    sm: 4,
    base: 8,
    md: 12,
    lg: 16,
    full: 9999
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
  },
  breakpoints: {
    sm: 640,
    md: 768,
    lg: 1024,
    xl: 1280,
    '2xl': 1536
  }
};

/**
 * Helper function to validate if a color matches style guide
 */
export function isValidStyleGuideColor(color: string): boolean {
  const validColors = Object.values(STYLE_GUIDE.colors).filter(c => typeof c === 'string');
  const darkColors = Object.values(STYLE_GUIDE.colors.dark);
  return validColors.includes(color) || darkColors.includes(color);
}

/**
 * Helper function to validate spacing against 8px grid
 */
export function isValidSpacing(pixels: number): boolean {
  return pixels % STYLE_GUIDE.spacing.base === 0;
}

/**
 * Helper to check if animation duration is within style guide range
 */
export function isValidAnimationDuration(ms: number): boolean {
  return ms >= STYLE_GUIDE.animation.duration_min && ms <= STYLE_GUIDE.animation.duration_max;
}