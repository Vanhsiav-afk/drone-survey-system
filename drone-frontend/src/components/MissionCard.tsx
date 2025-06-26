import React from 'react';
import type { Mission } from '../types';

export default function MissionCard({ mission, onStart }: {
  mission: Mission;
  onStart: (id: number) => void;
}) {
  return (
    <div className="mission-card">
      <h3>{mission.name}</h3>
      <p>Status: {mission.status}</p>
      <button onClick={() => onStart(mission.id)} disabled={mission.status !== 'pending'}>
        Start Mission
      </button>
    </div>
  );
}
