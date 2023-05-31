import * as React from "react";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import { useState } from "react";
import Button from "@mui/material/Button";

export default function App() {
  const [searchText, setSearchText] = useState("");
  const [searchResults, setSearchResults] = useState<string[]>([]);

  const onSearch = async () => {
    const response = await fetch(
      `http://localhost:8000/search?q=${searchText}`
    );

    if (!response.ok) {
      throw new Error("Failed to fetch search results");
    }

    const data = await response.json();
    setSearchResults(data.results);
  };

  return (
    <Container maxWidth="sm">
      <div className="my-4">
        <Typography variant="h4" component="h1" gutterBottom>
          🔍 Bloog
        </Typography>
        <TextField
          id="search-field"
          label="Search"
          variant="outlined"
          value={searchText}
          onChange={(event) => setSearchText(event.target.value)}
        />
      </div>
      <Button variant="outlined" onClick={onSearch}>
        Search
      </Button>
      {searchResults.map((result) => (
        <div key={result} className="my-4">
          <Typography variant="body1" gutterBottom>
            {result}
          </Typography>
        </div>
      ))}
    </Container>
  );
}
