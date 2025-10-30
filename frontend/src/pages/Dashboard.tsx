import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";

import CalendarView from "../components/CalendarView";
import TrimesterTimeline from "../components/TrimesterTimeline";
import GroupAgenda from "../components/GroupAgenda";

export default function Dashboard() {
  return (
    <Stack spacing={3}>
      <Typography variant="h4">Teacher dashboard</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} lg={7}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Calendar overview
            </Typography>
            <CalendarView />
          </Paper>
        </Grid>
        <Grid item xs={12} lg={5}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Trimester roadmap
            </Typography>
            <TrimesterTimeline />
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Group-specific agenda
            </Typography>
            <GroupAgenda />
          </Paper>
        </Grid>
      </Grid>
    </Stack>
  );
}
