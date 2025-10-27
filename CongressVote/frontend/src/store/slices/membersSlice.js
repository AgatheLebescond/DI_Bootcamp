import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import membersService from '../../services/membersService';

const initialState = {
  members: [],
  member: null,
  isLoading: false,
  isError: false,
  isSuccess: false,
  message: '',
};

// Get all congress members
export const getMembers = createAsyncThunk(
  'members/getAll',
  async (params, thunkAPI) => {
    try {
      return await membersService.getMembers(params);
    } catch (error) {
      const message =
        (error.response && error.response.data && error.response.data.detail) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

// Get single member
export const getMember = createAsyncThunk(
  'members/get',
  async (id, thunkAPI) => {
    try {
      return await membersService.getMember(id);
    } catch (error) {
      const message =
        (error.response && error.response.data && error.response.data.detail) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

export const membersSlice = createSlice({
  name: 'members',
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
      .addCase(getMembers.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getMembers.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.members = action.payload;
      })
      .addCase(getMembers.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      })
      .addCase(getMember.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getMember.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.member = action.payload;
      })
      .addCase(getMember.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      });
  },
});

export const { reset } = membersSlice.actions;
export default membersSlice.reducer;