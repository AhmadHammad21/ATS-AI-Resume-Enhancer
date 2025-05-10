import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
} from '@mui/material';

const DetailsModal = ({ open, onClose, details }) => {
  if (!details) return null;

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          minHeight: '60vh',
          maxHeight: '80vh',
        },
      }}
    >
      <DialogTitle>
        <Typography variant="h6" component="div">
          Resume Analysis Details
        </Typography>
      </DialogTitle>
      <DialogContent dividers>
        <Box sx={{ whiteSpace: 'pre-line' }}>
          <Typography variant="body1" component="div">
            {details}
          </Typography>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DetailsModal; 