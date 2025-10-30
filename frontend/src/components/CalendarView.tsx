import { useEffect, useState } from "react";
import dayjs, { Dayjs } from "dayjs";
import { DateCalendar } from "@mui/x-date-pickers/DateCalendar";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";

import api from "../api/client";
import { Session } from "../types";

interface CalendarViewProps {
  groupId?: number;
}

export default function CalendarView({ groupId }: CalendarViewProps) {
  const [selectedDate, setSelectedDate] = useState<Dayjs>(dayjs());
  const [sessions, setSessions] = useState<Session[]>([]);

  useEffect(() => {
    const start = selectedDate.startOf("week").format("YYYY-MM-DD");
    const end = selectedDate.endOf("week").format("YYYY-MM-DD");

    api
      .get<Session[]>("/calendar/agenda", {
        params: { start, end, group_id: groupId },
      })
      .then((response) => setSessions(response.data))
      .catch(() => setSessions([]));
  }, [groupId, selectedDate]);

  return (
    <Stack direction={{ xs: "column", md: "row" }} spacing={3}>
      <DateCalendar value={selectedDate} onChange={(value) => value && setSelectedDate(value)} />
      <Stack spacing={2} flex={1}>
        {sessions.map((session) => (
          <Card key={session.id} variant="outlined">
            <CardContent>
              <Typography variant="subtitle1">
                {dayjs(session.scheduled_date).format("MMM D")} — Lesson #{session.id}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {session.override_plan ?? session.lesson_plan}
              </Typography>
            </CardContent>
          </Card>
        ))}
        {sessions.length === 0 && (
          <Typography variant="body2" color="text.secondary">
            No scheduled sessions for the selected range.
          </Typography>
        )}
      </Stack>
    </Stack>
  );
}
