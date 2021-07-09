import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

import './index.css';

import CssBaseline from '@material-ui/core/CssBaseline';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';


// Fonts
import './fonts/Montserrat_Subrayada/MontserratSubrayada-Regular.ttf';
import './fonts/Montserrat/Montserrat-Regular.ttf';

const theme = createMuiTheme({
  palette: {
    primary: {
      main: '#CD5360'
    }
  },
});

ReactDOM.render(
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <App />
  </ThemeProvider>,
  document.getElementById('root')
);
