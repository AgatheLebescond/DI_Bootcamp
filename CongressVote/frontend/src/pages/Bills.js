import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  CircularProgress,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import AddIcon from '@mui/icons-material/Add';
import { useDispatch, useSelector } from 'react-redux';
import { getBills } from '../store/slices/billsSlice';

const Bills = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { bills, isLoading } = useSelector((state) => state.bills);
  const { user } = useSelector((state) => state.auth);
  
  const [filters, setFilters] = useState({
    status: '',
    billType: '',
    search: '',
  });

  useEffect(() => {
    dispatch(getBills({}));
  }, [dispatch]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const handleSearch = () => {
    const params = {};
    if (filters.status) params.status = filters.status;
    if (filters.billType) params.bill_type = filters.billType;
    dispatch(getBills(params));
  };

  const getStatusColor = (status) => {
    const colors = {
      'Introduced': 'default',
      'In Committee': 'info',
      'Passed House': 'primary',
      'Passed Senate': 'primary',
      'To President': 'warning',
      'Signed': 'success',
      'Vetoed': 'error',
      'Enacted': 'success',
    };
    return colors[status] || 'default';
  };

  const columns = [
    { 
      field: 'bill_number', 
      headerName: 'Bill Number', 
      width: 130,
      renderCell: (params) => (
        <Button
          variant="text"
          onClick={() => navigate(`/bills/${params.row.id}`)}
          sx={{ textTransform: 'none' }}
        >
          {params.value}
        </Button>
      ),
    },
    { field: 'title', headerName: 'Title', flex: 1, minWidth: 300 },
    { field: 'bill_type', headerName: 'Type', width: 100 },
    { 
      field: 'status', 
      headerName: 'Status', 
      width: 150,
      renderCell: (params) => (
        <Chip 
          label={params.value} 
          size="small" 
          color={getStatusColor(params.value)}
        />
      ),
    },
    { 
      field: 'introduced_date', 
      headerName: 'Introduced', 
      width: 120,
      valueFormatter: (params) => {
        if (!params.value) return '';
        return new Date(params.value).toLocaleDateString();
      },
    },
  ];

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Bills</Typography>
        {user?.is_superuser && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => navigate('/bills/new')}
          >
            Add Bill
          </Button>
        )}
      </Box>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Box display="flex" gap={2} alignItems="center">
          <TextField
            name="search"
            label="Search Bills"
            variant="outlined"
            size="small"
            value={filters.search}
            onChange={handleFilterChange}
            sx={{ flex: 1 }}
          />
          
          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Status</InputLabel>
            <Select
              name="status"
              value={filters.status}
              onChange={handleFilterChange}
              label="Status"
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="Introduced">Introduced</MenuItem>
              <MenuItem value="In Committee">In Committee</MenuItem>
              <MenuItem value="Passed House">Passed House</MenuItem>
              <MenuItem value="Passed Senate">Passed Senate</MenuItem>
              <MenuItem value="To President">To President</MenuItem>
              <MenuItem value="Signed">Signed</MenuItem>
              <MenuItem value="Vetoed">Vetoed</MenuItem>
              <MenuItem value="Enacted">Enacted</MenuItem>
            </Select>
          </FormControl>

          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Bill Type</InputLabel>
            <Select
              name="billType"
              value={filters.billType}
              onChange={handleFilterChange}
              label="Bill Type"
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="H.R.">H.R.</MenuItem>
              <MenuItem value="S.">S.</MenuItem>
              <MenuItem value="H.J.Res.">H.J.Res.</MenuItem>
              <MenuItem value="S.J.Res.">S.J.Res.</MenuItem>
              <MenuItem value="H.Con.Res.">H.Con.Res.</MenuItem>
              <MenuItem value="S.Con.Res.">S.Con.Res.</MenuItem>
              <MenuItem value="H.Res.">H.Res.</MenuItem>
              <MenuItem value="S.Res.">S.Res.</MenuItem>
            </Select>
          </FormControl>

          <Button variant="contained" onClick={handleSearch}>
            Search
          </Button>
        </Box>
      </Paper>

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={bills}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10, 25, 50]}
          loading={isLoading}
          disableSelectionOnClick
        />
      </Paper>
    </Box>
  );
};

export default Bills;