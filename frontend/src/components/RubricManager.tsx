import { useEffect, useState } from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import MenuItem from "@mui/material/MenuItem";

import api from "../api/client";
import { Rubric, Subject } from "../types";

export default function RubricManager() {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [rubrics, setRubrics] = useState<Rubric[]>([]);
  const [form, setForm] = useState({ subject_id: "", name: "", criteria: "" });

  useEffect(() => {
    api
      .get<Subject[]>("/subjects")
      .then((response) => setSubjects(response.data))
      .catch(() => setSubjects([]));
  }, []);

  useEffect(() => {
    api
      .get<Rubric[]>("/rubrics")
      .then((response) => setRubrics(response.data))
      .catch(() => setRubrics([]));
  }, []);

  const handleSubmit = () => {
    if (!form.subject_id || !form.name || !form.criteria) {
      return;
    }
    api
      .post<Rubric>("/rubrics", {
        subject_id: Number(form.subject_id),
        name: form.name,
        criteria: form.criteria,
      })
      .then((response) => {
        setRubrics((prev) => [...prev, response.data]);
        setForm({ subject_id: "", name: "", criteria: "" });
      });
  };

  return (
    <Stack spacing={3}>
      <Stack spacing={2} direction={{ xs: "column", md: "row" }}>
        <TextField
          select
          label="Subject"
          value={form.subject_id}
          onChange={(event) => setForm((prev) => ({ ...prev, subject_id: event.target.value }))}
          fullWidth
        >
          {subjects.map((subject) => (
            <MenuItem key={subject.id} value={subject.id}>
              {subject.name}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          label="Rubric name"
          value={form.name}
          onChange={(event) => setForm((prev) => ({ ...prev, name: event.target.value }))}
          fullWidth
        />
      </Stack>
      <TextField
        label="Criteria"
        value={form.criteria}
        onChange={(event) => setForm((prev) => ({ ...prev, criteria: event.target.value }))}
        fullWidth
        multiline
        minRows={4}
      />
      <Button variant="contained" color="primary" onClick={handleSubmit}>
        Add rubric
      </Button>
      <Stack spacing={1}>
        {rubrics.map((rubric) => (
          <Card key={rubric.id} variant="outlined">
            <CardContent>
              <Typography variant="subtitle1">{rubric.name}</Typography>
              <Typography variant="body2" color="text.secondary">
                {rubric.criteria}
              </Typography>
            </CardContent>
          </Card>
        ))}
        {rubrics.length === 0 && (
          <Typography variant="body2" color="text.secondary">
            No rubrics available yet.
          </Typography>
        )}
      </Stack>
    </Stack>
  );
}
