import api from './api';

const getMembers = async (params) => {
  const response = await api.get('/congress-members', { params });
  return response.data;
};

const getMember = async (id) => {
  const response = await api.get(`/congress-members/${id}`);
  return response.data;
};

const createMember = async (memberData) => {
  const response = await api.post('/congress-members', memberData);
  return response.data;
};

const updateMember = async (id, memberData) => {
  const response = await api.put(`/congress-members/${id}`, memberData);
  return response.data;
};

const deleteMember = async (id) => {
  const response = await api.delete(`/congress-members/${id}`);
  return response.data;
};

const membersService = {
  getMembers,
  getMember,
  createMember,
  updateMember,
  deleteMember,
};

export default membersService;