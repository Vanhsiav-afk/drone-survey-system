// src/types/index.ts
export type DroneStatus = 'idle' | 'in_mission' | 'charging';
export type MissionStatus = 'pending' | 'in_progress' | 'paused' | 'completed' | 'aborted';

export type Drone = {
  id: number;
  model: string;
  status: DroneStatus;
  battery_level: number;
};

export type Mission = {
  id: number;
  name: string;
  status: MissionStatus;
  description?: string;
  altitude?: number;
  overlap_percentage?: number;
};
