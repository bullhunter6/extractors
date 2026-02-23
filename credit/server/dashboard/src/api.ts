import axios from 'axios';
import type { Extractor, ExtractorRun, SystemMetrics, ExtractorCategory, ExtractorStatus } from './types';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const extractorAPI = {
  list: async (params?: {
    category?: ExtractorCategory;
    enabled?: boolean;
    status?: ExtractorStatus;
    skip?: number;
    limit?: number;
  }) => {
    const response = await api.get<{ extractors: Extractor[]; total: number }>('/extractors', { params });
    return response.data;
  },

  get: async (id: number) => {
    const response = await api.get<Extractor>(`/extractors/${id}`);
    return response.data;
  },

  trigger: async (id: number) => {
    const response = await api.post(`/extractors/${id}/trigger`);
    return response.data;
  },

  triggerBatch: async (ids: number[]) => {
    const response = await api.post('/extractors/trigger-batch', { extractor_ids: ids });
    return response.data;
  },

  update: async (id: number, data: Partial<Extractor>) => {
    const response = await api.patch(`/extractors/${id}`, data);
    return response.data;
  },

  getRuns: async (id: number, params?: { skip?: number; limit?: number }) => {
    const response = await api.get<{ runs: ExtractorRun[]; total: number }>(`/extractors/${id}/runs`, { params });
    return response.data;
  },
};

export const metricsAPI = {
  getSystem: async () => {
    const response = await api.get<SystemMetrics>('/metrics/system');
    return response.data;
  },

  getExtractorMetrics: async (days = 7) => {
    const response = await api.get('/metrics/extractors', { params: { days } });
    return response.data;
  },

  getRecentRuns: async (limit = 20) => {
    const response = await api.get('/metrics/runs/recent', { params: { limit } });
    return response.data;
  },
};

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private handlers: Map<string, (data: any) => void> = new Map();

  connect(onOpen?: () => void) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.hostname}:${window.location.port}/ws/status`;
    
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      onOpen?.();
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        const handler = this.handlers.get(message.type);
        if (handler) {
          handler(message.data);
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected, reconnecting...');
      this.reconnectTimeout = setTimeout(() => this.connect(onOpen), 3000);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  on(type: string, handler: (data: any) => void) {
    this.handlers.set(type, handler);
  }

  send(data: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  disconnect() {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }
    this.ws?.close();
  }
}
