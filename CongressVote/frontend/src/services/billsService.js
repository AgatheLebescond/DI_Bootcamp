import api from './api';

const getBills = async (params) => {
  const response = await api.get('/bills', { params });
  return response.data;
};

const getBill = async (id) => {
  const response = await api.get(`/bills/${id}`);
  return response.data;
};

const createBill = async (billData) => {
  const response = await api.post('/bills', billData);
  return response.data;
};

const updateBill = async (id, billData) => {
  const response = await api.put(`/bills/${id}`, billData);
  return response.data;
};

const deleteBill = async (id) => {
  const response = await api.delete(`/bills/${id}`);
  return response.data;
};

const billsService = {
  getBills,
  getBill,
  createBill,
  updateBill,
  deleteBill,
};

export default billsService;