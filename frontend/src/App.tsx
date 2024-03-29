import React, { useState } from "react";
import Button from "@mui/material/Button";
import {
  AppBar,
  Card,
  CardActions,
  CardContent,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  Pagination,
  TextField,
  Toolbar,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import SortIcon from "@mui/icons-material/Sort";
import { useQuery } from "@tanstack/react-query";
import { LoadingButton } from "@mui/lab";
import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en";

TimeAgo.addDefaultLocale(en);
const timeAgo = new TimeAgo("en-US");

const API_URL = "http://localhost:8000";
const PAGE_SIZE = 9;
const MAX_DESCRIPTION_LENGTH = 140;

const SEARCH_SUGGESTIONS = [
  "AI",
  "React",
  "Python",
  "Kafka",
  "Database",
  "Index",
  "Interview",
];

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

enum SortOption {
  Relevancy = "relevancy",
  Newest = "newest",
}

const App = () => {
  const [rawSearchQuery, setRawSearchQuery] = useState("");
  const [searchQuery, setSearchQuery] = useState("*");
  const [pageNumber, setPageNumber] = useState(0);
  const [sortOption, setSortOption] = useState<SortOption>(
    SortOption.Relevancy
  );

  const isAllQuery = () => searchQuery === "*";

  const getSortOption = () => (isAllQuery() ? SortOption.Newest : sortOption);

  const fetchSearchResults = async () => {
    const sort = getSortOption();
    const resp = await fetch(
      `${API_URL}/search?q=${searchQuery}&sort=${sort}&page=${pageNumber}`
    );
    return await resp.json();
  };

  const { data, isLoading, error } = useQuery<SearchResponse>({
    queryKey: ["search", { searchQuery, sortOption, pageNumber }],
    queryFn: fetchSearchResults,
    keepPreviousData: true,
  });

  const onSearch = (query?: string) => {
    const q = query ?? rawSearchQuery;
    setRawSearchQuery(q);
    setSearchQuery(q.trim() === "" ? "*" : q);
    setPageNumber(0);
  };

  const onInputKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Enter") {
      onSearch();
    }
  };

  const SearchResults = () => {
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
        <div className="columns-2">
          <Pagination
            count={pageCount}
            page={pageNumber + 1}
            onChange={(_, page) => setPageNumber(page - 1)}
          />
          <span className="float-right">
            <SortMenu />
          </span>
        </div>
        <ul className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 px-0">
          {data.results.map((result: SearchResult) => (
            <SearchResultCard key={result.id} {...result} />
          ))}
        </ul>
      </div>
    );
  };

  const SortMenu = () => {
    const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
    const isOpen = anchorEl != null;
    const onSortOption = (option: SortOption) => {
      setSortOption(option);
      setAnchorEl(null);
    };

    return (
      <>
        <IconButton
          id="sort-button"
          title="Sort"
          color="secondary"
          aria-controls={isOpen ? "sort-menu" : undefined}
          aria-expanded={isOpen ? "true" : undefined}
          aria-haspopup="true"
          onClick={(e) => setAnchorEl(e.currentTarget)}
        >
          <SortIcon />
        </IconButton>
        <Menu
          id="sort-menu"
          anchorEl={anchorEl}
          open={isOpen}
          onClose={() => setAnchorEl(null)}
          MenuListProps={{
            "aria-labelledby": "sort-button",
          }}
        >
          <MenuItem
            selected={getSortOption() === SortOption.Relevancy}
            disabled={isAllQuery()}
            onClick={() => onSortOption(SortOption.Relevancy)}
          >
            Relevancy
          </MenuItem>
          <MenuItem
            selected={getSortOption() === SortOption.Newest}
            onClick={() => onSortOption(SortOption.Newest)}
          >
            Newest
          </MenuItem>
        </Menu>
      </>
    );
  };

  const SearchResultCard = (result: SearchResult) => (
    <Card sx={{ minWidth: 275, height: 275 }} variant="outlined">
      <CardContent>
        <div className="flex flex-row justify-between">
          <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
            {result.source}
          </Typography>
          <Typography sx={{ fontSize: 14 }} color="text.secondary">
            {timeAgo.format(new Date(result.createdAt))}
          </Typography>
        </div>
        <Typography
          variant="h5"
          component="div"
          title={result.title}
          sx={{
            overflow: "hidden",
            display: "-webkit-box",
            lineClamp: 3,
            WebkitLineClamp: 3,
            WebkitBoxOrient: "vertical",
            mb: 1.5,
          }}
        >
          {result.title}
        </Typography>
        <Typography
          variant="body2"
          sx={{
            overflow: "hidden",
            display: "-webkit-box",
            lineClamp: 4,
            WebkitLineClamp: 4,
            WebkitBoxOrient: "vertical",
          }}
        >
          {result.description}
          {result.description.length >= MAX_DESCRIPTION_LENGTH && "..."}
        </Typography>
      </CardContent>
      <div className="flex-grow" />
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
                  color="secondary"
                  size="small"
                  variant="outlined"
                  fullWidth
                  sx={{
                    "& .MuiOutlinedInput-root": {
                      fieldset: { borderRight: "none" },
                      "&:hover fieldset": {
                        borderColor: "rgba(0, 0, 0, 0.23)",
                        backgroundColor: "rgba(0, 0, 0, 0.04)",
                      },
                      "&.Mui-focused fieldset": {
                        borderColor: "rgba(0, 0, 0, 0.23)",
                        borderWidth: "1px",
                      },
                    },
                  }}
                  InputProps={{
                    style: {
                      borderTopRightRadius: 0,
                      borderBottomRightRadius: 0,
                    },
                  }}
                  value={rawSearchQuery}
                  onChange={(e) => setRawSearchQuery(e.target.value)}
                  onKeyDown={onInputKeyDown}
                />
              </div>
              <LoadingButton
                loading={isLoading}
                color="secondary"
                size="medium"
                variant="outlined"
                className="rounded-l-none"
                onClick={() => onSearch()}
              >
                <SearchIcon />
              </LoadingButton>
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
        <SearchResults />
      </div>
    </div>
  );
};

export default App;
