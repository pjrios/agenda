export interface Level {
  id: number;
  name: string;
}

export interface Subject {
  id: number;
  name: string;
  level_id: number;
}

export interface Group {
  id: number;
  name: string;
  level_id: number;
}

export interface Trimester {
  id: number;
  name: string;
  level_id: number;
  start_date: string;
  end_date: string;
}

export interface Schedule {
  id: number;
  group_id: number;
  subject_id: number;
  weekday: number;
  start_time: string;
  end_time: string;
}

export interface Session {
  id: number;
  group_id: number;
  subject_id: number;
  trimester_id: number;
  scheduled_date: string;
  lesson_plan: string;
  override_plan?: string | null;
}

export interface Material {
  id: number;
  session_id: number;
  title: string;
  description?: string | null;
  url?: string | null;
  content_text: string;
}

export interface Rubric {
  id: number;
  subject_id: number;
  name: string;
  criteria: string;
}

export interface SemanticResult {
  id: number;
  title: string;
  description: string;
  score: number;
}
