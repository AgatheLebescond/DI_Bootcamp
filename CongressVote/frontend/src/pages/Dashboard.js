import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Paper,
  CircularProgress,
} from '@mui/material';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import DescriptionIcon from '@mui/icons-material/Description';
import PeopleIcon from '@mui/icons-material/People';
import HowToVoteIcon from '@mui/icons-material/HowToVote';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import billsService from '../services/billsService';
import membersService from '../services/membersService';
import votesService from '../services/votesService';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const Dashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalBills: 0,
    totalMembers: 0,
    totalVotes: 0,
    recentActivity: 0,
    billsByStatus: [],
    membersByParty: [],
  });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch bills
      const bills = await billsService.getBills({ limit: 1000 });
      const totalBills = bills.length;
      
      // Calculate bills by status
      const statusCounts = bills.reduce((acc, bill) => {
        acc[bill.status] = (acc[bill.status] || 0) + 1;
        return acc;
      }, {});
      
      const billsByStatus = Object.entries(statusCounts).map(([status, count]) => ({
        name: status,
        value: count,
      }));

      // Fetch members
      const members = await membersService.getMembers({ limit: 1000 });
      const totalMembers = members.length;
      
      // Calculate members by party
      const partyCounts = members.reduce((acc, member) => {
        acc[member.party] = (acc[member.party] || 0) + 1;
        return acc;
      }, {});
      
      const membersByParty = Object.entries(partyCounts).map(([party, count]) => ({
        name: party,
        value: count,
      }));

      // Fetch recent votes (simplified for now)
      const votes = await votesService.getVotes({ limit: 100 });
      const totalVotes = votes.length;

      setStats({
        totalBills,
        totalMembers,
        totalVotes,
        recentActivity: votes.length,
        billsByStatus,
        membersByParty,
      });
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, icon, color, onClick }) => (
    <Card 
      sx={{ 
        height: '100%', 
        cursor: onClick ? 'pointer' : 'default',
        '&:hover': onClick ? { 
          boxShadow: 3,
          transform: 'translateY(-2px)',
          transition: 'all 0.3s'
        } : {}
      }}
      onClick={onClick}
    >
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography color="textSecondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h4">
              {value}
            </Typography>
          </Box>
          <Box sx={{ color }}>
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Bills"
            value={stats.totalBills}
            icon={<DescriptionIcon sx={{ fontSize: 40 }} />}
            color="#1976d2"
            onClick={() => navigate('/bills')}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Congress Members"
            value={stats.totalMembers}
            icon={<PeopleIcon sx={{ fontSize: 40 }} />}
            color="#388e3c"
            onClick={() => navigate('/members')}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Votes"
            value={stats.totalVotes}
            icon={<HowToVoteIcon sx={{ fontSize: 40 }} />}
            color="#f57c00"
            onClick={() => navigate('/votes')}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Recent Activity"
            value={stats.recentActivity}
            icon={<TrendingUpIcon sx={{ fontSize: 40 }} />}
            color="#d32f2f"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Bills by Status
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={stats.billsByStatus}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {stats.billsByStatus.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Members by Party
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stats.membersByParty}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8">
                  {stats.membersByParty.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;