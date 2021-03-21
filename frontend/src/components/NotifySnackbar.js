import React, { useState } from 'react';

import {
  Snackbar,
} from '@material-ui/core';
import MuiAlert from '@material-ui/lab/Alert';

const useSnackbar = () => {
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarStatus, setSnackbarStatus] = useState('error');

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackbarOpen(false);
  };

  const showSnackbar = (message, status) => {
    setSnackbarMessage(message);
    setSnackbarStatus(status);
    setSnackbarOpen(true);
  };

  return {
    handleSnackbarClose,
    showSnackbar,
    snackbarStatus: {
      snackbarOpen,
      snackbarMessage,
      snackbarStatus,
    },
  };
};


const NotifySnackbar = (props) => {
  const {
    snackbarOpen,
    handleSnackbarClose,
    snackbarStatus,
    snackbarMessage
  } = props;

  const Alert = (props) => {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
  };

  return (
    <Snackbar
      open={snackbarOpen}
      autoHideDuration={6000}
      onClose={handleSnackbarClose}
    >
      <Alert severity={snackbarStatus}>{snackbarMessage}</Alert>
    </Snackbar>
  );
};

export default NotifySnackbar;

export {
  useSnackbar,
};
