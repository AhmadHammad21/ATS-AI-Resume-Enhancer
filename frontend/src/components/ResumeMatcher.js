import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Grid,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import { toast } from 'react-toastify';
import DeleteIcon from '@mui/icons-material/Delete';
import DescriptionIcon from '@mui/icons-material/Description';
import { analyzeResumes } from '../api';

const ResumeMatcher = () => {
  const [jobDescription, setJobDescription] = useState('');
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const onDrop = (acceptedFiles) => {
    const pdfFiles = acceptedFiles.filter(file => file.type === 'application/pdf');
    if (pdfFiles.length !== acceptedFiles.length) {
      toast.warning('Only PDF files are accepted');
    }
    setFiles(prev => [...prev, ...pdfFiles]);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    }
  });

  const handleAnalyze = async () => {
    if (!jobDescription.trim()) {
      toast.error('Please enter a job description');
      return;
    }
    if (files.length === 0) {
      toast.error('Please upload at least one resume');
      return;
    }

    setLoading(true);
    try {
      const response = await analyzeResumes(jobDescription, files);
      setResults(response);
      toast.success('Analysis completed successfully!');
    } catch (error) {
      toast.error('Error analyzing resumes. Please try again.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const removeFile = (index) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography 
        variant="h3" 
        component="h1" 
        gutterBottom 
        align="center" 
        sx={{ 
          mb: 4,
          background: 'linear-gradient(45deg, #2563eb 30%, #475569 90%)',
          backgroundClip: 'text',
          textFillColor: 'transparent',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
        }}
      >
        ATS Resume Matcher
      </Typography>

      <Grid container spacing={4}>
        {/* Job Description Section */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom sx={{ color: 'primary.main' }}>
              Job Description
            </Typography>
            <TextField
              fullWidth
              multiline
              rows={6}
              variant="outlined"
              placeholder="Enter the job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              sx={{ mb: 2 }}
            />
          </Paper>
        </Grid>

        {/* Resume Upload Section */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom sx={{ color: 'primary.main' }}>
              Upload Resumes
            </Typography>
            <Box
              {...getRootProps()}
              sx={{
                border: '2px dashed',
                borderColor: isDragActive ? 'primary.main' : 'grey.300',
                borderRadius: 2,
                p: 3,
                textAlign: 'center',
                cursor: 'pointer',
                bgcolor: isDragActive ? 'action.hover' : 'background.paper',
                mb: 2,
                transition: 'all 0.2s ease-in-out',
                '&:hover': {
                  borderColor: 'primary.main',
                  bgcolor: 'action.hover',
                },
              }}
            >
              <input {...getInputProps()} />
              <DescriptionIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography>
                {isDragActive
                  ? 'Drop the PDF files here'
                  : 'Drag and drop PDF files here, or click to select files'}
              </Typography>
            </Box>

            {files.length > 0 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Uploaded Files:
                </Typography>
                {files.map((file, index) => (
                  <Chip
                    key={index}
                    icon={<DescriptionIcon />}
                    label={file.name}
                    onDelete={() => removeFile(index)}
                    sx={{ m: 0.5 }}
                  />
                ))}
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Analyze Button */}
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'center' }}>
            <Button
              variant="contained"
              size="large"
              onClick={handleAnalyze}
              disabled={loading || files.length === 0 || !jobDescription.trim()}
              sx={{ 
                minWidth: 200,
                height: 48,
                fontSize: '1.1rem',
                background: 'linear-gradient(45deg, #2563eb 30%, #475569 90%)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #1d4ed8 30%, #334155 90%)',
                },
              }}
            >
              {loading ? <CircularProgress size={24} color="inherit" /> : 'Analyze Resumes'}
            </Button>
          </Box>
        </Grid>

        {/* Results Section */}
        {results && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom sx={{ color: 'primary.main' }}>
                Analysis Results
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Candidate Name</TableCell>
                      <TableCell>File Name</TableCell>
                      <TableCell align="right">Match Percentage</TableCell>
                      <TableCell align="right">Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {results.map((result, index) => (
                      <TableRow 
                        key={index}
                        sx={{ 
                          '&:hover': { 
                            bgcolor: 'action.hover' 
                          } 
                        }}
                      >
                        <TableCell>{result.candidateName}</TableCell>
                        <TableCell>{result.fileName}</TableCell>
                        <TableCell align="right">
                          <Chip
                            label={result.matchPercentage}
                            color={
                              parseInt(result.matchPercentage) >= 80
                                ? 'success'
                                : parseInt(result.matchPercentage) >= 60
                                ? 'warning'
                                : 'error'
                            }
                          />
                        </TableCell>
                        <TableCell align="right">
                          <Tooltip title="View Details">
                            <IconButton 
                              size="small"
                              onClick={() => {
                                // TODO: Implement detailed view
                                toast.info('Detailed view coming soon!');
                              }}
                            >
                              <DescriptionIcon />
                            </IconButton>
                          </Tooltip>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Container>
  );
};

export default ResumeMatcher; 