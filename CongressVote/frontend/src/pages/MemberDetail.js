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
  Avatar,
  Link,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import PersonIcon from '@mui/icons-material/Person';
import EmailIcon from '@mui/icons-material/Email';
import PhoneIcon from '@mui/icons-material/Phone';
import LanguageIcon from '@mui/icons-material/Language';
import TwitterIcon from '@mui/icons-material/Twitter';
import { useDispatch, useSelector } from 'react-redux';
import { getMember } from '../store/slices/membersSlice';
import { getVotes } from '../store/slices/votesSlice';

const MemberDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { member, isLoading: memberLoading } = useSelector((state) => state.members);
  const { votes, isLoading: votesLoading } = useSelector((state) => state.votes);

  useEffect(() => {
    if (id) {
      dispatch(getMember(id));
      dispatch(getVotes({ congress_member_id: id, limit: 10 }));
    }
  }, [dispatch, id]);

  const getPartyColor = (party) => {
    const colors = {
      'Democrat': '#2196f3',
      'Republican': '#f44336',
      'Independent': '#4caf50',
      'Other': '#9e9e9e',
    };
    return colors[party] || '#9e9e9e';
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

  if (memberLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!member) {
    return (
      <Box>
        <Typography variant="h5">Member not found</Typography>
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/members')}>
          Back to Members
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/members')}
        sx={{ mb: 2 }}
      >
        Back to Members
      </Button>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Avatar
              sx={{
                width: 120,
                height: 120,
                bgcolor: getPartyColor(member.party),
                mx: 'auto',
                mb: 2,
              }}
            >
              <PersonIcon sx={{ fontSize: 60 }} />
            </Avatar>
            
            <Typography variant="h5" gutterBottom>
              {member.full_name}
            </Typography>
            
            <Chip
              label={member.party}
              sx={{
                bgcolor: getPartyColor(member.party),
                color: 'white',
                mb: 2,
              }}
            />
            
            <Typography variant="body1" color="textSecondary" gutterBottom>
              {member.chamber} - {member.state}
              {member.district && ` District ${member.district}`}
            </Typography>

            <Box sx={{ mt: 3, textAlign: 'left' }}>
              {member.email && (
                <Box display="flex" alignItems="center" mb={1}>
                  <EmailIcon sx={{ mr: 1, color: 'action.active' }} />
                  <Link href={`mailto:${member.email}`} underline="hover">
                    {member.email}
                  </Link>
                </Box>
              )}
              
              {member.phone && (
                <Box display="flex" alignItems="center" mb={1}>
                  <PhoneIcon sx={{ mr: 1, color: 'action.active' }} />
                  <Link href={`tel:${member.phone}`} underline="hover">
                    {member.phone}
                  </Link>
                </Box>
              )}
              
              {member.website && (
                <Box display="flex" alignItems="center" mb={1}>
                  <LanguageIcon sx={{ mr: 1, color: 'action.active' }} />
                  <Link href={member.website} target="_blank" underline="hover">
                    Website
                  </Link>
                </Box>
              )}
              
              {member.twitter_handle && (
                <Box display="flex" alignItems="center">
                  <TwitterIcon sx={{ mr: 1, color: 'action.active' }} />
                  <Link
                    href={`https://twitter.com/${member.twitter_handle}`}
                    target="_blank"
                    underline="hover"
                  >
                    @{member.twitter_handle}
                  </Link>
                </Box>
              )}
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Votes
            </Typography>
            
            {votesLoading ? (
              <Box display="flex" justifyContent="center" p={3}>
                <CircularProgress />
              </Box>
            ) : votes.length > 0 ? (
              <List>
                {votes.map((vote) => (
                  <ListItem
                    key={vote.id}
                    divider
                    secondaryAction={
                      <Chip
                        label={vote.vote_type}
                        size="small"
                        color={getVoteColor(vote.vote_type)}
                      />
                    }
                  >
                    <ListItemText
                      primary={`Bill ${vote.bill_id}`}
                      secondary={new Date(vote.vote_date).toLocaleDateString()}
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography variant="body2" color="textSecondary">
                No votes recorded yet
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default MemberDetail;