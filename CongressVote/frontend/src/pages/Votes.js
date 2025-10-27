import React, { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  CircularProgress,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { useDispatch, useSelector } from 'react-redux';
import { getVotes } from '../store/slices/votesSlice';
import { getBills } from '../store/slices/billsSlice';
import { getMembers } from '../store/slices/membersSlice';

const Votes = () => {
  const dispatch = useDispatch();
  const { votes, isLoading } = useSelector((state) => state.votes);
  const { bills } = useSelector((state) => state.bills);
  const { members } = useSelector((state) => state.members);
  
  const [filters, setFilters] = useState({
    billId: '',
    memberId: '',
    voteType: '',
  });

  useEffect(() => {
    dispatch(getVotes({}));
    dispatch(getBills({ limit: 100 }));
    dispatch(getMembers({ limit: 500 }));
  }, [dispatch]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
    
    const params = {};
    if (name === 'billId' && value) params.bill_id = value;
    if (name === 'memberId' && value) params.congress_member_id = value;
    if (name === 'voteType' && value) params.vote_type = value;
    
    dispatch(getVotes(params));
  };

  const getVoteColor = (voteType) => {
    const colors = {
      'Yea': 'success',
      'Nay': 'error',
      'Present': 'warning',
      'Not Voting': 'default',
    };
    return colors[voteType] || 'default';
  };

  const getBillInfo = (billId) => {
    const bill = bills.find(b => b.id === billId);
    return bill ? bill.bill_number : `Bill ${billId}`;
  };

  const getMemberInfo = (memberId) => {
    const member = members.find(m => m.id === memberId);
    return member ? member.full_name : `Member ${memberId}`;
  };

  const columns = [
    { 
      field: 'bill_id', 
      headerName: 'Bill',
      width: 150,
      valueGetter: (params) => getBillInfo(params.value),
    },
    { 
      field: 'congress_member_id', 
      headerName: 'Member',
      flex: 1,
      minWidth: 200,
      valueGetter: (params) => getMemberInfo(params.value),
    },
    { 
      field: 'vote_type', 
      headerName: 'Vote',
      width: 120,
      renderCell: (params) => (
        <Chip 
          label={params.value} 
          size="small" 
          color={getVoteColor(params.value)}
        />
      ),
    },
    { 
      field: 'vote_date', 
      headerName: 'Date',
      width: 120,
      valueFormatter: (params) => {
        if (!params.value) return '';
        return new Date(params.value).toLocaleDateString();
      },
    },
    { 
      field: 'notes', 
      headerName: 'Notes',
      flex: 1,
      minWidth: 200,
      renderCell: (params) => params.value || '-',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Votes
      </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Box display="flex" gap={2} alignItems="center">
          <FormControl size="small" sx={{ minWidth: 200 }}>
            <InputLabel>Bill</InputLabel>
            <Select
              name="billId"
              value={filters.billId}
              onChange={handleFilterChange}
              label="Bill"
            >
              <MenuItem value="">All Bills</MenuItem>
              {bills.map(bill => (
                <MenuItem key={bill.id} value={bill.id}>
                  {bill.bill_number} - {bill.title.substring(0, 50)}...
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl size="small" sx={{ minWidth: 200 }}>
            <InputLabel>Member</InputLabel>
            <Select
              name="memberId"
              value={filters.memberId}
              onChange={handleFilterChange}
              label="Member"
            >
              <MenuItem value="">All Members</MenuItem>
              {members.map(member => (
                <MenuItem key={member.id} value={member.id}>
                  {member.full_name} ({member.party})
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Vote Type</InputLabel>
            <Select
              name="voteType"
              value={filters.voteType}
              onChange={handleFilterChange}
              label="Vote Type"
            >
              <MenuItem value="">All Types</MenuItem>
              <MenuItem value="Yea">Yea</MenuItem>
              <MenuItem value="Nay">Nay</MenuItem>
              <MenuItem value="Present">Present</MenuItem>
              <MenuItem value="Not Voting">Not Voting</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </Paper>

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={votes}
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

export default Votes;