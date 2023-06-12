import React, { useState } from "react";
import Button from "@mui/material/Button";
import {
  AppBar,
  Card,
  CardActions,
  CardContent,
  Chip,
  Pagination,
  TextField,
  Toolbar,
  Typography,
} from "@mui/material";
import { useQuery } from "@tanstack/react-query";

const SEARCH_SUGGESTIONS = ["AI", "ML", "Database", "React", "Index"];

interface SearchResponse {
  total: number;
  results: SearchResult[];
}

interface SearchResult {
  id: string;
  title: string;
  createdAt: string;
  description: string;
  source: string;
  url: string;
}

const API_URL = "http://localhost:8000";
const PAGE_SIZE = 9;

const App = () => {
  const [rawSearchQuery, setRawSearchQuery] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [pageNumber, setPageNumber] = useState(0);

  const { data, error } = useQuery({
    queryKey: ["searchQuery", searchQuery, pageNumber],
    queryFn: () => {
      if (searchQuery.trim() === "") {
        return null;
      }
      return fetch(
        `${API_URL}/search?q=${searchQuery}&page=${pageNumber}`
      ).then((res) => res.json());
    },
  });

  const onSearch = (query?: string) => {
    setRawSearchQuery(query ?? rawSearchQuery);
    setSearchQuery(query ?? rawSearchQuery);
    setPageNumber(0);
  };

  const onInputKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Enter") {
      onSearch();
    }
  };

  const renderResults = () => {
    if (error != null) {
      return <Typography>Error searching for "{searchQuery}"</Typography>;
    }

    if (data == null) {
      return null;
    }

    if (data.results.length === 0) {
      return <Typography>No Results for "{searchQuery}"</Typography>;
    }

    const pageCount = Math.ceil(data.total / PAGE_SIZE);

    return (
      <div>
        <Pagination
          count={pageCount}
          page={pageNumber + 1}
          onChange={(_, page) => setPageNumber(page - 1)}
        />
        <ul className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 px-0">
          {data.results.map((result: SearchResult) => (
            <SearchResult key={result.id} {...result} />
          ))}
        </ul>
      </div>
    );
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
          <Button
            href={result.url}
            target="_blank"
            color="secondary"
            size="small"
          >
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
            🔍 bloog
          </Typography>
        </Toolbar>
      </AppBar>
      <div className="pt-8 pb-4">
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
                  value={rawSearchQuery}
                  onChange={(e) => setRawSearchQuery(e.target.value)}
                  onKeyDown={onInputKeyDown}
                />
              </div>
              <Button
                color="secondary"
                size="medium"
                variant="outlined"
                className="ml-4"
                onClick={() => onSearch()}
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
                  onClick={() => onSearch(suggestion)}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto pb-6 px-4 sm:px-6 lg:px-8">
        {renderResults()}
      </div>
    </div>
  );
};

export default App;
