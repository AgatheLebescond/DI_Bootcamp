import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import votesService from '../../services/votesService';

const initialState = {
  votes: [],
  voteStats: null,
  isLoading: false,
  isError: false,
  isSuccess: false,
  message: '',
};

// Get all votes
export const getVotes = createAsyncThunk(
  'votes/getAll',
  async (params, thunkAPI) => {
    try {
      return await votesService.getVotes(params);
    } catch (error) {
      const message =
        (error.response && error.response.data && error.response.data.detail) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

// Get vote statistics for a bill
export const getVoteStats = createAsyncThunk(
  'votes/getStats',
  async (billId, thunkAPI) => {
    try {
      return await votesService.getVoteStats(billId);
    } catch (error) {
      const message =
        (error.response && error.response.data && error.response.data.detail) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

export const votesSlice = createSlice({
  name: 'votes',
  initialState,
  reducers: {
    reset: (state) => {
      state.isLoading = false;
      state.isError = false;
      state.isSuccess = false;
      state.message = '';
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getVotes.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getVotes.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.votes = action.payload;
      })
      .addCase(getVotes.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      })
      .addCase(getVoteStats.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getVoteStats.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.voteStats = action.payload;
      })
      .addCase(getVoteStats.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      });
  },
});

export const { reset } = votesSlice.actions;
export default votesSlice.reducer;