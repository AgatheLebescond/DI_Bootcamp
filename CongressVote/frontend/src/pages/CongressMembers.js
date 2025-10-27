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
  Avatar,
  CircularProgress,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import AddIcon from '@mui/icons-material/Add';
import PersonIcon from '@mui/icons-material/Person';
import { useDispatch, useSelector } from 'react-redux';
import { getMembers } from '../store/slices/membersSlice';

const CongressMembers = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { members, isLoading } = useSelector((state) => state.members);
  const { user } = useSelector((state) => state.auth);
  
  const [filters, setFilters] = useState({
    chamber: '',
    party: '',
    state: '',
    search: '',
  });

  useEffect(() => {
    dispatch(getMembers({}));
  }, [dispatch]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const handleSearch = () => {
    const params = {};
    if (filters.chamber) params.chamber = filters.chamber;
    if (filters.party) params.party = filters.party;
    if (filters.state) params.state = filters.state;
    dispatch(getMembers(params));
  };

  const getPartyColor = (party) => {
    const colors = {
      'Democrat': '#2196f3',
      'Republican': '#f44336',
      'Independent': '#4caf50',
      'Other': '#9e9e9e',
    };
    return colors[party] || '#9e9e9e';
  };

  const columns = [
    {
      field: 'avatar',
      headerName: '',
      width: 60,
      renderCell: (params) => (
        <Avatar sx={{ bgcolor: getPartyColor(params.row.party) }}>
          <PersonIcon />
        </Avatar>
      ),
    },
    { 
      field: 'full_name', 
      headerName: 'Name', 
      flex: 1,
      minWidth: 200,
      renderCell: (params) => (
        <Button
          variant="text"
          onClick={() => navigate(`/members/${params.row.id}`)}
          sx={{ textTransform: 'none', justifyContent: 'flex-start' }}
        >
          {params.value}
        </Button>
      ),
    },
    { 
      field: 'party', 
      headerName: 'Party', 
      width: 120,
      renderCell: (params) => (
        <Chip 
          label={params.value} 
          size="small" 
          sx={{ 
            bgcolor: getPartyColor(params.value),
            color: 'white',
          }}
        />
      ),
    },
    { field: 'state', headerName: 'State', width: 80 },
    { field: 'chamber', headerName: 'Chamber', width: 100 },
    { field: 'district', headerName: 'District', width: 100 },
    { 
      field: 'email', 
      headerName: 'Email', 
      width: 200,
      renderCell: (params) => (
        params.value ? (
          <Typography
            variant="body2"
            component="a"
            href={`mailto:${params.value}`}
            sx={{ color: 'primary.main', textDecoration: 'none' }}
          >
            {params.value}
          </Typography>
        ) : '-'
      ),
    },
  ];

  const states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
  ];

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Congress Members</Typography>
        {user?.is_superuser && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => navigate('/members/new')}
          >
            Add Member
          </Button>
        )}
      </Box>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Box display="flex" gap={2} alignItems="center">
          <TextField
            name="search"
            label="Search Members"
            variant="outlined"
            size="small"
            value={filters.search}
            onChange={handleFilterChange}
            sx={{ flex: 1 }}
          />
          
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Chamber</InputLabel>
            <Select
              name="chamber"
              value={filters.chamber}
              onChange={handleFilterChange}
              label="Chamber"
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="House">House</MenuItem>
              <MenuItem value="Senate">Senate</MenuItem>
            </Select>
          </FormControl>

          <FormControl size="small" sx={{ minWidth: 140 }}>
            <InputLabel>Party</InputLabel>
            <Select
              name="party"
              value={filters.party}
              onChange={handleFilterChange}
              label="Party"
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="Democrat">Democrat</MenuItem>
              <MenuItem value="Republican">Republican</MenuItem>
              <MenuItem value="Independent">Independent</MenuItem>
              <MenuItem value="Other">Other</MenuItem>
            </Select>
          </FormControl>

          <FormControl size="small" sx={{ minWidth: 100 }}>
            <InputLabel>State</InputLabel>
            <Select
              name="state"
              value={filters.state}
              onChange={handleFilterChange}
              label="State"
            >
              <MenuItem value="">All</MenuItem>
              {states.map(state => (
                <MenuItem key={state} value={state}>{state}</MenuItem>
              ))}
            </Select>
          </FormControl>

          <Button variant="contained" onClick={handleSearch}>
            Search
          </Button>
        </Box>
      </Paper>

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={members}
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

export default CongressMembers;