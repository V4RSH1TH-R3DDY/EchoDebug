import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '../services/apiClient';
import type { BackendStatus } from '../types/types';

const HEALTH_CHECK_INTERVAL = 10000; // 10 seconds

export const useBackendStatus = () => {
    const [status, setStatus] = useState<BackendStatus>({
        connected: false,
        lastChecked: Date.now(),
    });

    const checkHealth = useCallback(async () => {
        try {
            const isHealthy = await apiClient.healthCheck();
            setStatus({
                connected: isHealthy,
                lastChecked: Date.now(),
            });
        } catch {
            setStatus({
                connected: false,
                lastChecked: Date.now(),
            });
        }
    }, []);

    useEffect(() => {
        // Initial check
        checkHealth();

        // Periodic health checks
        const interval = setInterval(checkHealth, HEALTH_CHECK_INTERVAL);

        return () => clearInterval(interval);
    }, [checkHealth]);

    return { status, checkHealth };
};
