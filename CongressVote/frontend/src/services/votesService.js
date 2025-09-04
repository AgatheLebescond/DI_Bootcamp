import api from './api';

const getVotes = async (params) => {
  const response = await api.get('/votes', { params });
  return response.data;
};

const getVoteStats = async (billId) => {
  const response = await api.get(`/votes/stats/${billId}`);
  return response.data;
};

const createVote = async (voteData) => {
  const response = await api.post('/votes', voteData);
  return response.data;
};

const updateVote = async (id, voteData) => {
  const response = await api.put(`/votes/${id}`, voteData);
  return response.data;
};

const deleteVote = async (id) => {
  const response = await api.delete(`/votes/${id}`);
  return response.data;
};

const votesService = {
  getVotes,
  getVoteStats,
  createVote,
  updateVote,
  deleteVote,
};

export default votesService;