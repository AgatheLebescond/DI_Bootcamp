import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Button,
  Chip,
  Grid,
  CircularProgress,
  Divider,
  Link,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import LinkIcon from '@mui/icons-material/Link';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { useDispatch, useSelector } from 'react-redux';
import { getBill } from '../store/slices/billsSlice';
import { getVoteStats } from '../store/slices/votesSlice';

const COLORS = {
  'Yea': '#4caf50',
  'Nay': '#f44336',
  'Present': '#ff9800',
  'Not Voting': '#9e9e9e',
};

const BillDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { bill, isLoading: billLoading } = useSelector((state) => state.bills);
  const { voteStats, isLoading: voteLoading } = useSelector((state) => state.votes);

  useEffect(() => {
    if (id) {
      dispatch(getBill(id));
      dispatch(getVoteStats(id));
    }
  }, [dispatch, id]);

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

  if (billLoading || voteLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!bill) {
    return (
      <Box>
        <Typography variant="h5">Bill not found</Typography>
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/bills')}>
          Back to Bills
        </Button>
      </Box>
    );
  }

  const voteData = voteStats?.vote_breakdown
    ? Object.entries(voteStats.vote_breakdown).map(([key, value]) => ({
        name: key,
        value: value,
      }))
    : [];

  const partyData = voteStats?.party_breakdown
    ? Object.entries(voteStats.party_breakdown).map(([party, votes]) => ({
        party,
        ...votes,
      }))
    : [];

  return (
    <Box>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/bills')}
        sx={{ mb: 2 }}
      >
        Back to Bills
      </Button>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="start" mb={2}>
          <Box>
            <Typography variant="h4" gutterBottom>
              {bill.bill_number}
            </Typography>
            <Chip
              label={bill.status}
              color={getStatusColor(bill.status)}
              sx={{ mb: 2 }}
            />
          </Box>
          {bill.full_text_url && (
            <Button
              variant="outlined"
              startIcon={<LinkIcon />}
              href={bill.full_text_url}
              target="_blank"
              component={Link}
            >
              View Full Text
            </Button>
          )}
        </Box>

        <Typography variant="h6" gutterBottom>
          {bill.title}
        </Typography>
        
        {bill.short_title && (
          <Typography variant="subtitle1" color="textSecondary" gutterBottom>
            {bill.short_title}
          </Typography>
        )}

        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={12} md={6}>
            <Typography variant="body2" color="textSecondary">
              Type: <strong>{bill.bill_type}</strong>
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Introduced: <strong>{bill.introduced_date ? new Date(bill.introduced_date).toLocaleDateString() : 'N/A'}</strong>
            </Typography>
            {bill.sponsor_id && (
              <Typography variant="body2" color="textSecondary">
                Sponsor ID: <strong>{bill.sponsor_id}</strong>
              </Typography>
            )}
          </Grid>
          <Grid item xs={12} md={6}>
            {bill.house_passage_date && (
              <Typography variant="body2" color="textSecondary">
                House Passage: <strong>{new Date(bill.house_passage_date).toLocaleDateString()}</strong>
              </Typography>
            )}
            {bill.senate_passage_date && (
              <Typography variant="body2" color="textSecondary">
                Senate Passage: <strong>{new Date(bill.senate_passage_date).toLocaleDateString()}</strong>
              </Typography>
            )}
            {bill.enacted_date && (
              <Typography variant="body2" color="textSecondary">
                Enacted: <strong>{new Date(bill.enacted_date).toLocaleDateString()}</strong>
              </Typography>
            )}
          </Grid>
        </Grid>

        {bill.summary && (
          <>
            <Divider sx={{ my: 3 }} />
            <Typography variant="h6" gutterBottom>
              Summary
            </Typography>
            <Typography variant="body1" paragraph>
              {bill.summary}
            </Typography>
          </>
        )}
      </Paper>

      {voteStats && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Vote Results
              </Typography>
              <Box display="flex" justifyContent="space-around" mb={2}>
                <Box textAlign="center">
                  <Typography variant="h4">{voteStats.yea_votes}</Typography>
                  <Typography color="success.main">Yea</Typography>
                </Box>
                <Box textAlign="center">
                  <Typography variant="h4">{voteStats.nay_votes}</Typography>
                  <Typography color="error">Nay</Typography>
                </Box>
                <Box textAlign="center">
                  <Typography variant="h4">{voteStats.present_votes}</Typography>
                  <Typography color="warning.main">Present</Typography>
                </Box>
                <Box textAlign="center">
                  <Typography variant="h4">{voteStats.not_voting}</Typography>
                  <Typography color="textSecondary">Not Voting</Typography>
                </Box>
              </Box>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={voteData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {voteData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#000'} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Party Breakdown
              </Typography>
              {partyData.map((party) => (
                <Box key={party.party} mb={2}>
                  <Typography variant="subtitle1" gutterBottom>
                    {party.party}
                  </Typography>
                  <Grid container spacing={1}>
                    {Object.entries(party).map(([key, value]) => {
                      if (key === 'party') return null;
                      return (
                        <Grid item xs={6} sm={3} key={key}>
                          <Typography variant="body2" color="textSecondary">
                            {key}: <strong>{value}</strong>
                          </Typography>
                        </Grid>
                      );
                    })}
                  </Grid>
                </Box>
              ))}
            </Paper>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default BillDetail;