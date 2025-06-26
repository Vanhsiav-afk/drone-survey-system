import { useEffect, useState } from 'react';
import { fetchDrones, fetchMissions, startMission } from '../api';
import type { Drone, Mission } from '../types';
import DroneCard from '../components/DroneCard';
import MissionCard from '../components/MissionCard';

export default function Dashboard() {
  const [drones, setDrones] = useState<Drone[]>([]);
  const [missions, setMissions] = useState<Mission[]>([]);

  const load = async () => {
    const [d, m] = await Promise.all([fetchDrones(), fetchMissions()]);
    setDrones(d);
    setMissions(m);
  };

  const handleStart = async (id: number) => {
    await startMission(id);
    load(); // Refresh data
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div>
      <h1>🚀 Drone Fleet Dashboard</h1>

      <section>
        <h2>🛸 Drones</h2>
        {drones.map(d => <DroneCard key={d.id} drone={d} />)}
      </section>

      <section>
        <h2>📍 Missions</h2>
        {missions.map(m => <MissionCard key={m.id} mission={m} onStart={handleStart} />)}
      </section>
    </div>
  );
}
