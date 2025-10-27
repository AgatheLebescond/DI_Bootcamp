import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import billsReducer from './slices/billsSlice';
import membersReducer from './slices/membersSlice';
import votesReducer from './slices/votesSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    bills: billsReducer,
    members: membersReducer,
    votes: votesReducer,
  },
});