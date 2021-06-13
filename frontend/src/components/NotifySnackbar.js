import React, { useState } from 'react';

import {
  Snackbar,
} from '@material-ui/core';
import MuiAlert from '@material-ui/lab/Alert';

const useSnackbar = () => {
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('error');

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackbarOpen(false);
  };

  const showSnackbar = (message, severity) => {
    setSnackbarMessage(message);
    setSnackbarSeverity(severity);
    setSnackbarOpen(true);
  };

  return {
    handleSnackbarClose,
    showSnackbar,
    snackbarStatus: {
      snackbarOpen,
      snackbarMessage,
      snackbarSeverity,
    },
  };
};


const NotifySnackbar = (props) => {
  const {
    snackbarOpen,
    handleSnackbarClose,
    snackbarSeverity,
    snackbarMessage,
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
      <Alert severity={snackbarSeverity}>{snackbarMessage}</Alert>
    </Snackbar>
  );
};

export default NotifySnackbar;

export {
  useSnackbar,
};
