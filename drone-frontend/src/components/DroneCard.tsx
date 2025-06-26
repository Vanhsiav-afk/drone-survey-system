import React from 'react';
import type { Drone } from '../types';

export default function DroneCard({ drone }: { drone: Drone }) {
  return (
    <div className="drone-card">
      <h3>🚁 {drone.model}</h3>
      <p>Status: {drone.status}</p>
      <p>Battery: 🔋 {drone.battery_level}%</p>
    </div>
  );
}
