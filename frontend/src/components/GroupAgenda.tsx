import { useEffect, useState } from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import MenuItem from "@mui/material/MenuItem";
import TextField from "@mui/material/TextField";
import Stack from "@mui/material/Stack";
import dayjs from "dayjs";

import api from "../api/client";
import { Group, Session } from "../types";

export default function GroupAgenda() {
  const [groups, setGroups] = useState<Group[]>([]);
  const [selectedGroup, setSelectedGroup] = useState<number | "">("");
  const [sessions, setSessions] = useState<Session[]>([]);

  useEffect(() => {
    api
      .get<Group[]>("/groups")
      .then((response) => setGroups(response.data))
      .catch(() => setGroups([]));
  }, []);

  useEffect(() => {
    if (!selectedGroup) {
      setSessions([]);
      return;
    }
    api
      .get<Session[]>("/sessions", { params: { group_id: selectedGroup } })
      .then((response) => setSessions(response.data))
      .catch(() => setSessions([]));
  }, [selectedGroup]);

  return (
    <Stack spacing={2}>
      <TextField
        select
        fullWidth
        label="Select group"
        value={selectedGroup}
        onChange={(event) => {
          const value = event.target.value;
          setSelectedGroup(value === "" ? "" : Number(value));
        }}
      >
        <MenuItem value="">All groups</MenuItem>
        {groups.map((group) => (
          <MenuItem key={group.id} value={group.id}>
            {group.name}
          </MenuItem>
        ))}
      </TextField>
      <Stack spacing={1}>
        {sessions.map((session) => (
          <Card key={session.id} variant="outlined">
            <CardContent>
              <Typography variant="subtitle2">
                {dayjs(session.scheduled_date).format("MMM D, YYYY")} – Session #{session.id}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {session.override_plan ?? session.lesson_plan}
              </Typography>
            </CardContent>
          </Card>
        ))}
        {sessions.length === 0 && (
          <Typography variant="body2" color="text.secondary">
            Select a group to review upcoming lessons.
          </Typography>
        )}
      </Stack>
    </Stack>
  );
}
