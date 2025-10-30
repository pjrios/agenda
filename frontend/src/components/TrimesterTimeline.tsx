import { useEffect, useMemo, useState } from "react";
import { Timeline, TimelineConnector, TimelineContent, TimelineDot, TimelineItem, TimelineSeparator } from "@mui/lab";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import dayjs from "dayjs";

import api from "../api/client";
import { Trimester } from "../types";

interface TrimesterTimelineProps {
  levelId?: number;
}

export default function TrimesterTimeline({ levelId }: TrimesterTimelineProps) {
  const [trimesters, setTrimesters] = useState<Trimester[]>([]);

  useEffect(() => {
    api
      .get<Trimester[]>("/trimesters", { params: { level_id: levelId } })
      .then((response) => setTrimesters(response.data))
      .catch(() => setTrimesters([]));
  }, [levelId]);

  const sorted = useMemo(
    () => [...trimesters].sort((a, b) => a.start_date.localeCompare(b.start_date)),
    [trimesters]
  );

  if (sorted.length === 0) {
    return (
      <Typography variant="body2" color="text.secondary">
        No trimesters defined yet.
      </Typography>
    );
  }

  return (
    <Timeline position="right">
      {sorted.map((trimester, index) => (
        <TimelineItem key={trimester.id}>
          <TimelineSeparator>
            <TimelineDot color="primary" />
            {index < sorted.length - 1 && <TimelineConnector />}
          </TimelineSeparator>
          <TimelineContent>
            <Paper elevation={1} sx={{ p: 2 }}>
              <Stack spacing={0.5}>
                <Typography variant="subtitle1">{trimester.name}</Typography>
                <Typography variant="body2" color="text.secondary">
                  {dayjs(trimester.start_date).format("MMM D")} – {dayjs(trimester.end_date).format("MMM D")}
                </Typography>
              </Stack>
            </Paper>
          </TimelineContent>
        </TimelineItem>
      ))}
    </Timeline>
  );
}
