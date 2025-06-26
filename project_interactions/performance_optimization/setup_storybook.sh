#!/bin/bash

# GRANGER Storybook Setup Script
# This script automates the initial Storybook setup for GRANGER UI modules

set -e

echo "🚀 GRANGER Storybook Setup Script"
echo "================================="

# Check if we're in the right directory
if [ ! -d "/home/graham/workspace/granger-ui" ]; then
    echo "❌ Error: granger-ui directory not found"
    echo "Please create the unified UI repository first:"
    echo "  mkdir -p /home/graham/workspace/granger-ui"
    echo "  cd /home/graham/workspace/granger-ui"
    echo "  npm init -y"
    exit 1
fi

cd /home/graham/workspace/granger-ui

echo "📦 Step 1: Installing Storybook..."
npx storybook@latest init --type react --yes

echo "📦 Step 2: Installing additional addons..."
npm install --save-dev \
    @storybook/addon-a11y \
    @storybook/addon-interactions \
    @storybook/test-runner \
    @storybook/addon-viewport \
    @storybook/addon-measure \
    @storybook/addon-outline \
    @storybook/jest \
    @storybook/testing-library

echo "📁 Step 3: Creating directory structure..."
mkdir -p .storybook/decorators
mkdir -p src/components/{Button,Card,Input,Modal,Toast}
mkdir -p src/utils
mkdir -p docs/storybook

echo "📝 Step 4: Creating style guide constants..."
cat > src/utils/style-guide.ts << 'EOF'
export const STYLE_GUIDE = {
  colors: {
    primary_start: '#4F46E5',
    primary_end: '#6366F1',
    secondary: '#6B7280',
    background: '#F9FAFB',
    accent: '#10B981',
    error: '#EF4444',
    warning: '#F59E0B'
  },
  spacing: {
    base: 8,
    scale: [8, 16, 24, 32, 40, 48, 56, 64]
  },
  animation: {
    duration: '250ms',
    easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
  },
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '12px'
  }
};
EOF

echo "📝 Step 5: Creating Storybook configuration..."
cat > .storybook/main.js << 'EOF'
module.exports = {
  stories: [
    "../src/**/*.stories.@(js|jsx|ts|tsx|mdx)",
    "../docs/**/*.stories.mdx"
  ],
  addons: [
    "@storybook/addon-essentials",
    "@storybook/addon-a11y",
    "@storybook/addon-interactions",
    "@storybook/addon-viewport",
    "@storybook/addon-measure",
    "@storybook/addon-outline"
  ],
  framework: {
    name: "@storybook/react-vite",
    options: {}
  }
};
EOF

echo "📝 Step 6: Creating preview configuration..."
cat > .storybook/preview.js << 'EOF'
import { StyleGuideDecorator } from './decorators/StyleGuideDecorator';

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
  viewport: {
    viewports: {
      mobile: {
        name: 'Mobile',
        styles: { width: '375px', height: '667px' }
      },
      tablet: {
        name: 'Tablet',
        styles: { width: '768px', height: '1024px' }
      },
      desktop: {
        name: 'Desktop',
        styles: { width: '1440px', height: '900px' }
      }
    }
  }
};

export const decorators = [StyleGuideDecorator];
EOF

echo "📝 Step 7: Creating style guide decorator..."
cat > .storybook/decorators/StyleGuideDecorator.tsx << 'EOF'
import React from 'react';

export const StyleGuideDecorator = (Story) => {
  return (
    <div style={{ padding: '1rem' }}>
      <Story />
    </div>
  );
};
EOF

echo "📝 Step 8: Creating example Button component..."
cat > src/components/Button/Button.tsx << 'EOF'
import React from 'react';
import { STYLE_GUIDE } from '../../utils/style-guide';

export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  loading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
  disabled = false,
  loading = false
}) => {
  const baseStyles = {
    borderRadius: STYLE_GUIDE.borderRadius.md,
    transition: `all ${STYLE_GUIDE.animation.duration} ${STYLE_GUIDE.animation.easing}`,
    cursor: disabled || loading ? 'not-allowed' : 'pointer',
    opacity: disabled || loading ? 0.6 : 1
  };

  const variantStyles = {
    primary: {
      background: `linear-gradient(135deg, ${STYLE_GUIDE.colors.primary_start}, ${STYLE_GUIDE.colors.primary_end})`,
      color: 'white',
      border: 'none'
    },
    secondary: {
      background: 'transparent',
      color: STYLE_GUIDE.colors.primary_start,
      border: `2px solid ${STYLE_GUIDE.colors.primary_start}`
    },
    danger: {
      background: STYLE_GUIDE.colors.error,
      color: 'white',
      border: 'none'
    }
  };

  const sizeStyles = {
    sm: { padding: '8px 16px', fontSize: '14px' },
    md: { padding: '12px 24px', fontSize: '16px' },
    lg: { padding: '16px 32px', fontSize: '18px' }
  };

  return (
    <button
      style={{
        ...baseStyles,
        ...variantStyles[variant],
        ...sizeStyles[size]
      }}
      onClick={onClick}
      disabled={disabled || loading}
    >
      {loading ? 'Loading...' : children}
    </button>
  );
};
EOF

echo "📝 Step 9: Creating Button stories..."
cat > src/components/Button/Button.stories.tsx << 'EOF'
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Core/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger']
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg']
    }
  }
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Click me'
  }
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button'
  }
};

export const Danger: Story = {
  args: {
    variant: 'danger',
    children: 'Delete'
  }
};

export const Loading: Story = {
  args: {
    loading: true,
    children: 'Loading...'
  }
};

export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled'
  }
};
EOF

echo "📝 Step 10: Updating package.json scripts..."
npm pkg set scripts.storybook="storybook dev -p 6006"
npm pkg set scripts.build-storybook="storybook build"
npm pkg set scripts.test-storybook="test-storybook"

echo "✅ Storybook setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Start Storybook: npm run storybook"
echo "2. View the Button component story"
echo "3. Create more component stories"
echo "4. Run tests: npm run test-storybook"
echo ""
echo "📖 Documentation created at:"
echo "- /home/graham/workspace/shared_claude_docs/project_interactions/performance_optimization/STORYBOOK_IMPLEMENTATION_TASKS.md"
echo ""
echo "🎉 Happy Storybook development!"