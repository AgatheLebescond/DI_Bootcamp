import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Alert,
  CircularProgress,
  Divider,
} from '@mui/material';
import { useSelector } from 'react-redux';
import api from '../services/api';

const Profile = () => {
  const { user } = useSelector((state) => state.auth);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  
  const [profileData, setProfileData] = useState({
    username: user?.username || '',
    email: user?.email || '',
  });
  
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const handleProfileChange = (e) => {
    setProfileData({
      ...profileData,
      [e.target.name]: e.target.value,
    });
  };

  const handlePasswordChange = (e) => {
    setPasswordData({
      ...passwordData,
      [e.target.name]: e.target.value,
    });
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      await api.put('/users/me', {
        username: profileData.username,
        email: profileData.email,
      });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 5000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (passwordData.newPassword.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      await api.put('/users/me', {
        password: passwordData.newPassword,
      });
      setSuccess(true);
      setPasswordData({
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      });
      setTimeout(() => setSuccess(false), 5000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Profile
      </Typography>

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Profile updated successfully!
        </Alert>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Profile Information
            </Typography>
            <Box component="form" onSubmit={handleProfileSubmit}>
              <TextField
                fullWidth
                name="username"
                label="Username"
                value={profileData.username}
                onChange={handleProfileChange}
                margin="normal"
                required
              />
              <TextField
                fullWidth
                name="email"
                label="Email"
                type="email"
                value={profileData.email}
                onChange={handleProfileChange}
                margin="normal"
                required
              />
              <Button
                type="submit"
                variant="contained"
                fullWidth
                sx={{ mt: 2 }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Update Profile'}
              </Button>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Change Password
            </Typography>
            <Box component="form" onSubmit={handlePasswordSubmit}>
              <TextField
                fullWidth
                name="currentPassword"
                label="Current Password"
                type="password"
                value={passwordData.currentPassword}
                onChange={handlePasswordChange}
                margin="normal"
                required
              />
              <TextField
                fullWidth
                name="newPassword"
                label="New Password"
                type="password"
                value={passwordData.newPassword}
                onChange={handlePasswordChange}
                margin="normal"
                required
              />
              <TextField
                fullWidth
                name="confirmPassword"
                label="Confirm New Password"
                type="password"
                value={passwordData.confirmPassword}
                onChange={handlePasswordChange}
                margin="normal"
                required
              />
              <Button
                type="submit"
                variant="contained"
                fullWidth
                sx={{ mt: 2 }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Change Password'}
              </Button>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Account Information
            </Typography>
            <Divider sx={{ my: 2 }} />
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="textSecondary">
                  Account Type
                </Typography>
                <Typography variant="body1">
                  {user?.is_superuser ? 'Administrator' : 'Regular User'}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="textSecondary">
                  Account Status
                </Typography>
                <Typography variant="body1">
                  {user?.is_active ? 'Active' : 'Inactive'}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="textSecondary">
                  Member Since
                </Typography>
                <Typography variant="body1">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Profile;