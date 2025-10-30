import { useEffect, useState } from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Stack from "@mui/material/Stack";

import api from "../api/client";
import { Material, SemanticResult } from "../types";

export default function ResourcePlanner() {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [query, setQuery] = useState("");
  const [semanticResults, setSemanticResults] = useState<SemanticResult[]>([]);

  useEffect(() => {
    api
      .get<Material[]>("/materials")
      .then((response) => setMaterials(response.data))
      .catch(() => setMaterials([]));
  }, []);

  useEffect(() => {
    if (!query) {
      setSemanticResults([]);
      return;
    }
    const delay = setTimeout(() => {
      api
        .get<SemanticResult[]>("/semantic/search", { params: { query } })
        .then((response) => setSemanticResults(response.data))
        .catch(() => setSemanticResults([]));
    }, 300);
    return () => clearTimeout(delay);
  }, [query]);

  return (
    <Stack spacing={2}>
      <TextField
        fullWidth
        label="Search lesson materials"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
      />
      <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
        <Stack flex={1} spacing={1}>
          <Typography variant="subtitle1">Recent materials</Typography>
          {materials.map((material) => (
            <Card key={material.id} variant="outlined">
              <CardContent>
                <Typography variant="subtitle2">{material.title}</Typography>
                <Typography variant="body2" color="text.secondary">
                  {material.description ?? material.content_text.slice(0, 120)}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </Stack>
        <Stack flex={1} spacing={1}>
          <Typography variant="subtitle1">Semantic suggestions</Typography>
          {semanticResults.map((result) => (
            <Card key={result.id} variant="outlined">
              <CardContent>
                <Typography variant="subtitle2">{result.title}</Typography>
                <Typography variant="body2" color="text.secondary">
                  {result.description}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Similarity score: {result.score.toFixed(2)}
                </Typography>
              </CardContent>
            </Card>
          ))}
          {semanticResults.length === 0 && query && (
            <Typography variant="body2" color="text.secondary">
              No semantic matches found yet.
            </Typography>
          )}
        </Stack>
      </Stack>
    </Stack>
  );
}
