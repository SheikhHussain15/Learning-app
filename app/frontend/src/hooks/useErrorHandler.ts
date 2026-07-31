'use client';

import { useState, useCallback } from 'react';

interface ErrorHandlerOptions {
  retries?: number;
  retryDelay?: number;
  onError?: (error: Error) => void;
  onRetry?: (attempt: number) => void;
}

interface ErrorHandlerResult {
  error: Error | null;
  isLoading: boolean;
  retryCount: number;
  execute: <T>(fn: () => Promise<T>) => Promise<T | null>;
  clearError: () => void;
}

export function useErrorHandler(options: ErrorHandlerOptions = {}): ErrorHandlerResult {
  const { retries = 3, retryDelay = 1000, onError, onRetry } = options;
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [retryCount, setRetryCount] = useState(0);

  const clearError = useCallback(() => {
    setError(null);
    setRetryCount(0);
  }, []);

  const execute = useCallback(
    async <T,>(fn: () => Promise<T>): Promise<T | null> => {
      setIsLoading(true);
      setError(null);

      for (let attempt = 0; attempt <= retries; attempt++) {
        try {
          const result = await fn();
          setIsLoading(false);
          setRetryCount(0);
          return result;
        } catch (err) {
          const error = err instanceof Error ? err : new Error(String(err));

          if (attempt < retries) {
            setRetryCount(attempt + 1);
            onRetry?.(attempt + 1);
            await new Promise((resolve) =>
              setTimeout(resolve, retryDelay * Math.pow(2, attempt))
            );
          } else {
            setError(error);
            onError?.(error);
            setIsLoading(false);
            return null;
          }
        }
      }
      return null;
    },
    [retries, retryDelay, onError, onRetry]
  );

  return { error, isLoading, retryCount, execute, clearError };
}

export default useErrorHandler;
