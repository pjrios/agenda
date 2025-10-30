import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

import RubricManager from "../components/RubricManager";

export default function RubricManagement() {
  return (
    <Stack spacing={3}>
      <Typography variant="h4">Rubric management</Typography>
      <RubricManager />
    </Stack>
  );
}
