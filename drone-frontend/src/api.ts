// src/api.ts
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export const fetchDrones = async () => {
  const res = await axios.get(`${API_BASE}/drones`);
  return res.data;
};

export const fetchMissions = async () => {
  const res = await axios.get(`${API_BASE}/missions`);
  return res.data;
};

export const startMission = async (id: number) => {
  const res = await axios.post(`${API_BASE}/mission-control/${id}/start`);
  return res.data;
};
