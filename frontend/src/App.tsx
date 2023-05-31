import * as React from "react";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";

export default function App() {
  return (
    <Container maxWidth="sm">
      <div className="my-4">
        <Typography variant="h4" component="h1" gutterBottom>
          🔍 Bloog
        </Typography>
        <TextField id="search-field" label="Search" variant="standard" />
      </div>
    </Container>
  );
}
