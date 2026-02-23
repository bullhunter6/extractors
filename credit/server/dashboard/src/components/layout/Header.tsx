import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Activity, RefreshCw, Calendar } from 'lucide-react';
import { useQueryClient } from '@tanstack/react-query';

export default function Header() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const handleRefresh = () => {
    queryClient.invalidateQueries();
  };

  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass border-b border-white/5 backdrop-blur-xl sticky top-0 z-50"
    >
      <div className="max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-br from-primary to-accent rounded-xl flex items-center justify-center glow">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold font-display tracking-tight">
                <span className="gradient-text">EXTRACTOR</span>
                <span className="text-white"> CONTROL</span>
              </h1>
              <p className="text-sm text-gray-400 font-sans mt-0.5">
                Monitor & control credit rating article extractors
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/scheduler')}
              className="px-6 py-3 bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/50 rounded-xl font-display text-sm tracking-wide transition-all flex items-center space-x-2 group"
            >
              <Calendar className="w-4 h-4 text-purple-400" />
              <span className="text-purple-300">DASHBOARD</span>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleRefresh}
              className="px-6 py-3 bg-primary/20 hover:bg-primary/30 border border-primary/50 rounded-xl font-display text-sm tracking-wide transition-all flex items-center space-x-2 group"
            >
              <RefreshCw className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" />
              <span>REFRESH</span>
            </motion.button>
          </div>
        </div>
      </div>
    </motion.header>
  );
}
