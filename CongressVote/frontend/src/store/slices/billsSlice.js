import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import billsService from '../../services/billsService';

const initialState = {
  bills: [],
  bill: null,
  isLoading: false,
  isError: false,
  isSuccess: false,
  message: '',
};

// Get all bills
export const getBills = createAsyncThunk(
  'bills/getAll',
  async (params, thunkAPI) => {
    try {
      return await billsService.getBills(params);
    } catch (error) {
      const message =
        (error.response && error.response.data && error.response.data.detail) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

// Get single bill
export const getBill = createAsyncThunk(
  'bills/get',
  async (id, thunkAPI) => {
    try {
      return await billsService.getBill(id);
    } catch (error) {
      const message =
        (error.response && error.response.data && error.response.data.detail) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

export const billsSlice = createSlice({
  name: 'bills',
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
      .addCase(getBills.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getBills.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.bills = action.payload;
      })
      .addCase(getBills.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      })
      .addCase(getBill.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getBill.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.bill = action.payload;
      })
      .addCase(getBill.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      });
  },
});

export const { reset } = billsSlice.actions;
export default billsSlice.reducer;