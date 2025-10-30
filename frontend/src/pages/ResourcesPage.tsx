import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

import ResourcePlanner from "../components/ResourcePlanner";

export default function ResourcesPage() {
  return (
    <Stack spacing={3}>
      <Typography variant="h4">Resource planner</Typography>
      <ResourcePlanner />
    </Stack>
  );
}
