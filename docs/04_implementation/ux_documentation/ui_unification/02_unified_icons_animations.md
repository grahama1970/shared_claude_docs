# Unified Iconography & Animation System for GRANGER UI

## 1. Iconography Strategy

### 1.1 Primary Icon Library: Lucide React
Following the 2025 Style Guide's recommendation for simple, line-based icons:

```typescript
// packages/ui-core/src/icons/index.ts
export * from 'lucide-react';

// Custom icon wrapper for consistent styling
export const Icon = ({ icon: IconComponent, size = 20, className = "" }) => {
  return (
    <IconComponent 
      size={size} 
      className={cn(
        "stroke-2", // Consistent stroke width
        className
      )}
    />
  );
};
```

### 1.2 Icon Categories & Mapping

```typescript
// packages/ui-core/src/icons/icon-map.ts
import {
  // System Icons
  Activity,
  AlertCircle,
  CheckCircle2,
  XCircle,
  Info,
  HelpCircle,
  Settings,
  RefreshCw,
  Loader2,
  
  // Navigation
  ChevronLeft,
  ChevronRight,
  ChevronUp,
  ChevronDown,
  Menu,
  X,
  Home,
  ArrowLeft,
  ArrowRight,
  
  // Data & Analytics
  BarChart3,
  LineChart,
  PieChart,
  TrendingUp,
  TrendingDown,
  Database,
  
  // Module/Network
  Network,
  GitBranch,
  Share2,
  Workflow,