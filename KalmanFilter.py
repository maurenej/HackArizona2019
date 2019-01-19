from pykalman import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt

# Data description
#  Time
#  AccX_HP - high precision acceleration signal
#  AccX_LP - low precision acceleration signal
#  RefPosX - real position (ground truth)
#  RefVelX - real velocity (ground truth)
def kalmanFilterPositionChange(initial_state_mean, initial_state_covariance, initial_AccX_Value, new_AccX_Value):

  AccX_Value = np.array([initial_AccX_Value, new_AccX_Value])
  AccX_Variance = 0.0007

  # time step
  dt = 1

  # transition_matrix  
  F = [[1, dt, 0.5*dt**2], 
       [0,  1,       dt],
       [0,  0,        1]]

  # observation_matrix   
  H = [0, 0, 1]

  # transition_covariance 
  Q = [[0.2,    0,      0], 
       [  0,  0.1,      0],
       [  0,    0,  10e-4]]

  # observation_covariance 
  R = AccX_Variance

  # initial_state_mean
  X0 = [0,
        0,
        AccX_Value[0, 0]]

  # initial_state_covariance
  P0 = [[  0,    0,               0], 
        [  0,    0,               0],
        [  0,    0,   AccX_Variance]]

  n_timesteps = AccX_Value.shape[0]
  n_dim_state = 3
  filtered_state_means = np.zeros((n_timesteps, n_dim_state))
  filtered_state_covariances = np.zeros((n_timesteps, n_dim_state, n_dim_state))

  kf = KalmanFilter(transition_matrices = F, 
                    observation_matrices = H, 
                    transition_covariance = Q, 
                    observation_covariance = R, 
                    initial_state_mean = X0, 
                    initial_state_covariance = P0)

  # iterative estimation for the new measurement
  for t in range(n_timesteps):
      if t == 0:
          filtered_state_means[t] = initial_state_mean
          filtered_state_covariances[t] = initial_state_covariance
      else:
          filtered_state_means[t], filtered_state_covariances[t] = (
          kf.filter_update(
              filtered_state_means[t-1],
              filtered_state_covariances[t-1],
              AccX_Value[t, 0]))

  return (filtered_state_means[1], filtered_state_covariances[1], new_AccX_Value, filtered_state_means[1, 0] - filtered_state_means[0, 0])

