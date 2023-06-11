import React, { useState } from "react";
import Button from "@mui/material/Button";
import {
  AppBar,
  Card,
  CardActions,
  CardContent,
  Chip,
  TextField,
  Toolbar,
  Typography,
} from "@mui/material";

const SEARCH_SUGGESTIONS = ["AI", "ML", "Database", "React", "Index"];

interface SearchResult {
  source: string;
  id: number;
  title: string;
  description: string;
}

// https://collegecompendium.org/explore
const App = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([
    { id: 1, source: "Source", title: "Hello", description: "World" },
  ]);

  const onSearch = async (query: string) => {
    const response = await fetch(`http://localhost:8000/search?q=${query}`);

    if (!response.ok) {
      throw new Error("Failed to fetch search results");
    }

    const data = await response.json();
    setSearchResults(data.results);
  };

  const SearchResult = (result: SearchResult) => {
    return (
      <Card sx={{ minWidth: 275 }} variant="outlined">
        <CardContent>
          <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
            {result.source}
          </Typography>
          <Typography variant="h5" component="div" sx={{ mb: 1.5 }}>
            {result.title}
          </Typography>
          <Typography variant="body2">{result.description}</Typography>
        </CardContent>
        <CardActions>
          <Button color="secondary" size="small">
            View
          </Button>
        </CardActions>
      </Card>
    );
  };

  return (
    <div className="min-h-screen bg-white">
      <AppBar position="static" color="transparent" elevation={0}>
        <Toolbar>
          <Typography variant="h5" component="div" sx={{ fontWeight: 800 }}>
            🔍 Bloog
          </Typography>
        </Toolbar>
      </AppBar>
      <div className="py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="px-4 py-5 sm:p-6">
            <Typography variant="h4" align="center" sx={{ fontWeight: 800 }}>
              Technical Blog Search Engine
            </Typography>
            <div className="mt-6 flex">
              <div className="relative flex-1">
                <TextField
                  id="outlined-basic"
                  placeholder="Search"
                  variant="outlined"
                  size="small"
                  fullWidth
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
              <Button
                color="secondary"
                size="medium"
                variant="outlined"
                className="ml-4"
                onClick={() => onSearch(searchQuery)}
              >
                Search
              </Button>
            </div>

            <div className="mt-4 flex flex-wrap">
              {SEARCH_SUGGESTIONS.map((suggestion) => (
                <Chip
                  key={suggestion}
                  label={suggestion}
                  variant="outlined"
                  className="mr-2 mt-2"
                  onClick={() => {
                    setSearchQuery(suggestion);
                    onSearch(suggestion);
                  }}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <ul className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 px-0">
          {searchResults.map((result) => (
            <SearchResult key={result.id} {...result} />
          ))}
        </ul>
      </div>
    </div>
  );
};

export default App;
