import React, { useState, useEffect, useCallback } from 'react';
import { MessageSquare, FileText, Terminal, Search, ChevronRight, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// Types
export type UITarget = 'chat' | 'annotator' | 'terminal';

interface QuickSwitchBarProps {
  currentUI: UITarget;
  onSwitch: (target: UITarget) => Promise<void>;
  className?: string;
}

interface SwitchButtonProps {
  label: string;
  icon: React.ReactNode;
  active: boolean;
  onClick: () => void;
  disabled?: boolean;
  shortcut?: string;
}

interface TransitionState {
  isTransitioning: boolean;
  target: UITarget | null;
  progress: number;
}

// Utility function for class names
const cn = (...classes: (string | boolean | undefined)[]) => {
  return classes.filter(Boolean).join(' ');
};

// Switch Button Component
const SwitchButton: React.FC<SwitchButtonProps> = ({
  label,
  icon,
  active,
  onClick,
  disabled,
  shortcut
}) => {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "relative flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all duration-200",
        active 
          ? "bg-gradient-to-r from-purple-600 to-purple-700 text-white shadow-lg" 
          : "bg-white hover:bg-gray-50 text-gray-700 border border-gray-200",
        disabled && "opacity-50 cursor-not-allowed"
      )}
    >
      {/* Active indicator */}
      {active && (
        <motion.div
          layoutId="activeIndicator"
          className="absolute inset-0 bg-gradient-to-r from-purple-600 to-purple-700 rounded-lg"
          initial={false}
          transition={{ type: "spring", stiffness: 500, damping: 30 }}
        />
      )}
      
      <span className="relative z-10 flex items-center gap-2">
        {icon}
        <span>{label}</span>
        {shortcut && (
          <kbd className={cn(
            "hidden sm:inline-block text-xs px-1.5 py-0.5 rounded",
            active ? "bg-purple-800/50" : "bg-gray-100"
          )}>
            {shortcut}
          </kbd>
        )}
      </span>
    </motion.button>
  );
};

// Progress Indicator Component
const ProgressIndicator: React.FC<{ progress: number }> = ({ progress }) => {
  return (
    <div className="w-32 h-1 bg-gray-200 rounded-full overflow-hidden">
      <motion.div
        className="h-full bg-gradient-to-r from-purple-600 to-purple-700"
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.3 }}
      />
    </div>
  );
};

// Current Context Display
const CurrentContext: React.FC<{ context?: string }> = ({ context }) => {
  if (!context) return null;
  
  return (
    <div className="flex items-center gap-2 text-sm text-gray-600">
      <ChevronRight className="w-4 h-4" />
      <span className="truncate max-w-[200px]">{context}</span>
    </div>
  );
};

// Main Quick Switch Bar Component
export const QuickSwitchBar: React.FC<QuickSwitchBarProps> = ({
  currentUI,
  onSwitch,
  className
}) => {
  const [transitionState, setTransitionState] = useState<TransitionState>({
    isTransitioning: false,
    target: null,
    progress: 0
  });
  
  const [showSearch, setShowSearch] = useState(false);
  const [currentContext, setCurrentContext] = useState<string>('');

  // Handle UI switch
  const handleSwitch = useCallback(async (target: UITarget) => {
    if (target === currentUI || transitionState.isTransitioning) return;
    
    setTransitionState({
      isTransitioning: true,
      target,
      progress: 0
    });
    
    // Simulate progress (in real implementation, this would track actual progress)
    const progressInterval = setInterval(() => {
      setTransitionState(prev => ({
        ...prev,
        progress: Math.min(prev.progress + 20, 90)
      }));
    }, 200);
    
    try {
      await onSwitch(target);
      
      // Complete the progress
      setTransitionState(prev => ({
        ...prev,
        progress: 100
      }));
      
      // Reset after animation
      setTimeout(() => {
        setTransitionState({
          isTransitioning: false,
          target: null,
          progress: 0
        });
      }, 300);
    } catch (error) {
      console.error('Switch failed:', error);
      setTransitionState({
        isTransitioning: false,
        target: null,
        progress: 0
      });
    } finally {
      clearInterval(progressInterval);
    }
  }, [currentUI, onSwitch, transitionState.isTransitioning]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // Check for modifier keys
      const isCmd = e.metaKey || e.ctrlKey;
      const isAlt = e.altKey;
      
      if (isCmd && isAlt) {
        switch (e.key.toLowerCase()) {
          case 'c':
            e.preventDefault();
            handleSwitch('chat');
            break;
          case 'a':
            e.preventDefault();
            handleSwitch('annotator');
            break;
          case 't':
            e.preventDefault();
            handleSwitch('terminal');
            break;
        }
      }
      
      // Quick search
      if (isCmd && e.key === 'k') {
        e.preventDefault();
        setShowSearch(true);
      }
      
      // Cycle through interfaces
      if (isCmd && e.key === 'Tab') {
        e.preventDefault();
        const interfaces: UITarget[] = ['chat', 'annotator', 'terminal'];
        const currentIndex = interfaces.indexOf(currentUI);
        const nextIndex = (currentIndex + 1) % interfaces.length;
        handleSwitch(interfaces[nextIndex]);
      }
    };
    
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [currentUI, handleSwitch]);

  // Update context (in real implementation, this would come from the current UI)
  useEffect(() => {
    const contexts = {
      chat: 'Conversation with Claude',
      annotator: 'Document: Research Paper.pdf',
      terminal: '~/workspace/granger'
    };
    setCurrentContext(contexts[currentUI]);
  }, [currentUI]);

  return (
    <>
      <div className={cn(
        "fixed top-0 left-0 right-0 z-40 bg-white/80 backdrop-blur-lg border-b border-gray-200",
        className
      )}>
        <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
          {/* UI Switcher Buttons */}
          <div className="flex items-center gap-2">
            <SwitchButton
              label="Chat"
              icon={<MessageSquare className="w-4 h-4" />}
              active={currentUI === 'chat'}
              onClick={() => handleSwitch('chat')}
              disabled={transitionState.isTransitioning}
              shortcut="⌘⌥C"
            />
            <SwitchButton
              label="Annotator"
              icon={<FileText className="w-4 h-4" />}
              active={currentUI === 'annotator'}
              onClick={() => handleSwitch('annotator')}
              disabled={transitionState.isTransitioning}
              shortcut="⌘⌥A"
            />
            <SwitchButton
              label="Terminal"
              icon={<Terminal className="w-4 h-4" />}
              active={currentUI === 'terminal'}
              onClick={() => handleSwitch('terminal')}
              disabled={transitionState.isTransitioning}
              shortcut="⌘⌥T"
            />
          </div>
          
          {/* Center Section - Progress or Context */}
          <div className="flex-1 flex items-center justify-center">
            {transitionState.isTransitioning ? (
              <div className="flex items-center gap-3">
                <Loader2 className="w-4 h-4 animate-spin text-purple-600" />
                <span className="text-sm text-gray-600">
                  Switching to {transitionState.target}...
                </span>
                <ProgressIndicator progress={transitionState.progress} />
              </div>
            ) : (
              <CurrentContext context={currentContext} />
            )}
          </div>
          
          {/* Right Section - Quick Actions */}
          <div className="flex items-center gap-4">
            <button
              onClick={() => setShowSearch(true)}
              className="flex items-center gap-2 px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <Search className="w-4 h-4" />
              <span className="hidden sm:inline">Quick Search</span>
              <kbd className="text-xs bg-gray-100 px-1.5 py-0.5 rounded">⌘K</kbd>
            </button>
          </div>
        </div>
      </div>
      
      {/* Transition Overlay */}
      <AnimatePresence>
        {transitionState.isTransitioning && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-white/90 backdrop-blur-lg flex items-center justify-center"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="text-center"
            >
              <div className="mb-6">
                {transitionState.target === 'chat' && <MessageSquare className="w-16 h-16 mx-auto text-purple-600" />}
                {transitionState.target === 'annotator' && <FileText className="w-16 h-16 mx-auto text-purple-600" />}
                {transitionState.target === 'terminal' && <Terminal className="w-16 h-16 mx-auto text-purple-600" />}
              </div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                Switching to {transitionState.target}
              </h2>
              <p className="text-gray-600 mb-4">Preserving your context...</p>
              <div className="w-64 mx-auto">
                <ProgressIndicator progress={transitionState.progress} />
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Quick Search Modal (placeholder) */}
      <AnimatePresence>
        {showSearch && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4"
            onClick={() => setShowSearch(false)}
          >
            <motion.div
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.95 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white rounded-xl shadow-2xl p-6 max-w-lg w-full"
            >
              <h3 className="text-lg font-semibold mb-4">Quick Search</h3>
              <input
                type="text"
                placeholder="Search across all interfaces..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600"
                autoFocus
              />
              <p className="text-sm text-gray-500 mt-2">
                Press ESC to close
              </p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default QuickSwitchBar;