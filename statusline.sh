#!/bin/bash
#
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                     CLAUDE CODE STATUSLINE SCRIPT                         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
#
# A customizable statusline for Claude Code that displays:
#   • Current directory name
#   • Git branch with status indicators
#   • Claude API usage with visual progress bar
#   • Usage reset countdown
#
# ─────────────────────────────────────────────────────────────────────────────
# EXAMPLE OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
#
#   my-project │ ⎇ main*+ ⇡2 {1} │ Usage: 67% ██████▋░░░ ↻ 3:30 PM
#   ─────────    ───────────────    ─────────────────────────────────
#       │              │                          │
#       │              │                          └─ API usage with:
#       │              │                             • Color-coded percentage (green→red)
#       │              │                             • Smooth progress bar
#       │              │                             • Reset time
#       │              │
#       │              └─ Git info:
#       │                 • Branch name
#       │                 • Status indicators (+*?)
#       │                 • Remote sync (⇡⇣≡○)
#       │                 • Stash count {n}
#       │
#       └─ Current directory basename
#
# ─────────────────────────────────────────────────────────────────────────────
# GIT STATUS INDICATORS
# ─────────────────────────────────────────────────────────────────────────────
#
#   Symbol │ Color  │ Meaning
#   ───────┼────────┼──────────────────────────────────────────
#     +    │ Cyan   │ Staged changes ready to commit
#     *    │ Yellow │ Unstaged modifications in working tree
#     ?    │ Gray   │ Untracked files present
#   ───────┼────────┼──────────────────────────────────────────
#     ⇡n   │ Green  │ n commits ahead of remote
#     ⇣n   │ Red    │ n commits behind remote
#     ≡    │ Gray   │ In sync with remote (nothing to push/pull)
#     ○    │ Gray   │ No remote tracking branch configured
#   ───────┼────────┼──────────────────────────────────────────
#    {n}   │ Gray   │ n stashed changes
#
# ─────────────────────────────────────────────────────────────────────────────
# USAGE DISPLAY
# ─────────────────────────────────────────────────────────────────────────────
#
#   State          │ Display
#   ───────────────┼──────────────────────────────────────────
#   Fresh data     │ Usage: 42% ████▍░░░░░ ↻ 3:30 PM
#   Stale cache    │ Usage: 42% ████▍░░░░░ ⚠ ↻ 3:30 PM
#   No data        │ Usage: --
#
#   The progress bar uses partial block characters for smooth rendering:
#   ▏▎▍▌▋▊▉█ (1/8 to 8/8 increments)
#
#   Color gradient from green (low usage) to red (high usage):
#   0-10%   dark green      60-70%  muted yellow-orange
#   10-20%  soft green      70-80%  darker orange
#   20-30%  medium green    80-90%  dark red
#   30-40%  yellow-green    90-100% deep red
#   40-50%  olive
#   50-60%  muted yellow
#
# ─────────────────────────────────────────────────────────────────────────────
# PERFORMANCE
# ─────────────────────────────────────────────────────────────────────────────
#
#   • Usage data is cached for CACHE_TTL seconds (default: 60)
#   • Cached renders: ~10ms | Fresh API call: ~500ms+
#   • Git commands use 1-second timeout to prevent hangs
#   • Swift API calls use 3-second timeout
#
# ─────────────────────────────────────────────────────────────────────────────
# DEPENDENCIES
# ─────────────────────────────────────────────────────────────────────────────
#
#   Required:
#     • bash (v3.2+)
#     • git (for branch/status display)
#
#   Optional:
#     • fetch-claude-usage.swift (in same directory, for usage display)
#     • timeout or gtimeout (for command timeouts, falls back to bg job)
#
# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Directory display: Show the current directory basename
# Example: /Users/me/projects/my-app → "my-app"
SHOW_DIRECTORY=1

# Git branch: Show current branch name with ⎇ icon
# Example: "⎇ main", "⎇ feature/auth"
SHOW_BRANCH=1

# Git status indicators: Show working tree state (+, *, ?)
# Requires SHOW_BRANCH=1
SHOW_GIT_STATUS=1

# Git remote status: Show ahead/behind counts and sync state (⇡, ⇣, ≡, ○)
# Requires SHOW_BRANCH=1
SHOW_GIT_REMOTE=1

# Git stash count: Show number of stashed changes as {n}
# Requires SHOW_BRANCH=1
SHOW_GIT_STASH=1

# Usage display: Show Claude API usage percentage
# Requires fetch-claude-usage.swift in the same directory
SHOW_USAGE=1

# Progress bar: Show visual usage bar with partial block characters
# Requires SHOW_USAGE=1
SHOW_PROGRESS_BAR=1

# Reset time: Show when usage limit resets (respects system 12h/24h preference)
# Requires SHOW_USAGE=1
SHOW_RESET_TIME=1

# Cache TTL: Seconds before refreshing usage data from API
# Lower = more current data, higher = faster renders
CACHE_TTL=60

# ═══════════════════════════════════════════════════════════════════════════
# INTERNAL IMPLEMENTATION - Modify below at your own risk
# ═══════════════════════════════════════════════════════════════════════════

# Resolve script directory for locating companion files (fetch-claude-usage.swift)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ─────────────────────────────────────────────────────────────────────────────
# COLOR DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

# Standard ANSI colors for UI elements
BLUE=$'\033[0;34m'    # Directory name
GREEN=$'\033[0;32m'   # Branch name, commits ahead
GRAY=$'\033[0;90m'    # Separators, secondary info
YELLOW=$'\033[0;33m'  # Unstaged changes, warnings
RED=$'\033[0;31m'     # Commits behind
CYAN=$'\033[0;36m'    # Staged changes
RESET=$'\033[0m'      # Reset to default

# 10-level usage gradient using 256-color palette
# Progression: dark green → soft green → olive → yellow → orange → red
LEVEL_1=$'\033[38;5;22m'   #   0-10%  dark green (minimal usage)
LEVEL_2=$'\033[38;5;28m'   #  10-20%  soft green
LEVEL_3=$'\033[38;5;34m'   #  20-30%  medium green
LEVEL_4=$'\033[38;5;100m'  #  30-40%  green-yellowish
LEVEL_5=$'\033[38;5;142m'  #  40-50%  olive/yellow-green
LEVEL_6=$'\033[38;5;178m'  #  50-60%  muted yellow
LEVEL_7=$'\033[38;5;172m'  #  60-70%  yellow-orange
LEVEL_8=$'\033[38;5;166m'  #  70-80%  darker orange
LEVEL_9=$'\033[38;5;160m'  #  80-90%  dark red
LEVEL_10=$'\033[38;5;124m' #  90-100% deep red (critical usage)

# ─────────────────────────────────────────────────────────────────────────────
# CACHE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Cache file stores usage data to avoid repeated API calls
# Format: Line 1 = Unix timestamp, Line 2 = "UTILIZATION|RESETS_AT"
CACHE_FILE="/tmp/claude-usage-cache"

# ─────────────────────────────────────────────────────────────────────────────
# INPUT PARSING
# ─────────────────────────────────────────────────────────────────────────────

# Claude Code passes JSON via stdin containing session context
# We extract "current_dir" to display the working directory name
input=$(cat)
current_dir_path=$(echo "$input" | grep -o '"current_dir":"[^"]*"' | sed 's/"current_dir":"//;s/"$//')
current_dir=$(basename "$current_dir_path")

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

# get_usage_color <percentage>
# Returns the appropriate color escape code for the given usage percentage.
# Uses a 10-level gradient from green (low) to red (high).
get_usage_color() {
  local util=$1
  if   [ "$util" -le 10 ]; then echo "$LEVEL_1"
  elif [ "$util" -le 20 ]; then echo "$LEVEL_2"
  elif [ "$util" -le 30 ]; then echo "$LEVEL_3"
  elif [ "$util" -le 40 ]; then echo "$LEVEL_4"
  elif [ "$util" -le 50 ]; then echo "$LEVEL_5"
  elif [ "$util" -le 60 ]; then echo "$LEVEL_6"
  elif [ "$util" -le 70 ]; then echo "$LEVEL_7"
  elif [ "$util" -le 80 ]; then echo "$LEVEL_8"
  elif [ "$util" -le 90 ]; then echo "$LEVEL_9"
  else echo "$LEVEL_10"
  fi
}

# build_progress_bar <percentage>
# Renders a 10-character progress bar using Unicode block characters.
# Uses partial blocks (▏▎▍▌▋▊▉█) for smooth sub-character precision.
# Example: 67% → "██████▋░░░"
build_progress_bar() {
  local util=$1
  local width=10  # Total bar width in characters

  # Convert percentage to eighths (0-80 for 10 chars × 8 eighths each)
  # The +50 provides rounding to nearest eighth
  local eighths=$(( (util * width * 8 + 50) / 100 ))
  local full_blocks=$((eighths / 8))
  local remainder=$((eighths % 8))

  # Partial block characters indexed by eighths (0=empty, 7=almost full)
  local partials=(" " "▏" "▎" "▍" "▌" "▋" "▊" "▉")

  local bar=""

  # Render full blocks (█)
  local i=0
  while [ $i -lt $full_blocks ] && [ $i -lt $width ]; do
    bar="${bar}█"
    i=$((i + 1))
  done

  # Render partial block if there's a remainder and space available
  if [ $remainder -gt 0 ] && [ $full_blocks -lt $width ]; then
    bar="${bar}${partials[$remainder]}"
    full_blocks=$((full_blocks + 1))
  fi

  # Fill remaining space with empty blocks (░)
  local empty=$((width - full_blocks))
  i=0
  while [ $i -lt $empty ]; do
    bar="${bar}░"
    i=$((i + 1))
  done

  echo "$bar"
}

# is_cache_fresh
# Returns 0 (true) if cache exists and is younger than CACHE_TTL seconds.
# Returns 1 (false) if cache is missing, empty, or expired.
is_cache_fresh() {
  [ ! -f "$CACHE_FILE" ] && return 1

  local cache_time
  cache_time=$(head -1 "$CACHE_FILE" 2>/dev/null | cut -d'|' -f1)
  [ -z "$cache_time" ] && return 1

  local now age
  now=$(date +%s)
  age=$((now - cache_time))

  [ "$age" -lt "$CACHE_TTL" ]
}

# read_cache
# Outputs the cached usage data (second line of cache file).
# Format: "UTILIZATION|RESETS_AT" (e.g., "42|2024-01-29T15:30:00Z")
read_cache() {
  [ -f "$CACHE_FILE" ] && tail -1 "$CACHE_FILE" 2>/dev/null
}

# write_cache <data>
# Writes usage data to cache with current timestamp.
# Format: Line 1 = Unix timestamp, Line 2 = data
write_cache() {
  local data=$1
  local now
  now=$(date +%s)
  printf "%s\n%s\n" "$now" "$data" > "$CACHE_FILE" 2>/dev/null
}

# fetch_usage
# Retrieves Claude API usage, using cache when fresh or falling back gracefully.
#
# Output formats:
#   "42|2024-01-29T15:30:00Z"  - Fresh data (utilization|reset_time)
#   "STALE|42|..."            - Stale cached data (API call failed)
#   "ERROR|"                   - No data available
#
# Fallback chain:
#   1. Return cached data if fresh (< CACHE_TTL seconds old)
#   2. Call Swift script with 3-second timeout
#   3. On failure, return stale cache with STALE prefix
#   4. If no cache exists, return ERROR
fetch_usage() {
  local swift_path="$SCRIPT_DIR/fetch-claude-usage.swift"

  # Verify Swift script exists before attempting to run
  if [ ! -f "$swift_path" ]; then
    echo "ERROR|"
    return 1
  fi

  # Return cached data if still fresh
  if is_cache_fresh; then
    read_cache
    return 0
  fi

  # Attempt to fetch fresh data with timeout protection
  # Tries: timeout (Linux/GNU), gtimeout (macOS Homebrew), background job fallback
  local result
  if command -v timeout >/dev/null 2>&1; then
    result=$(timeout 3 swift "$swift_path" 2>/dev/null)
  elif command -v gtimeout >/dev/null 2>&1; then
    result=$(gtimeout 3 swift "$swift_path" 2>/dev/null)
  else
    # Fallback: run Swift in background with manual timeout via racing sleep
    result=$(swift "$swift_path" 2>/dev/null &
      pid=$!
      sleep 3 &
      sleep_pid=$!
      wait -n $pid $sleep_pid 2>/dev/null
      if kill -0 $pid 2>/dev/null; then
        kill $pid 2>/dev/null
        echo "ERROR|"
      else
        wait $pid
      fi
    )
  fi

  # Success: cache and return fresh data
  if [ $? -eq 0 ] && [ -n "$result" ] && [[ ! "$result" =~ ^ERROR ]]; then
    write_cache "$result"
    echo "$result"
    return 0
  fi

  # Failure: try to serve stale cache with warning indicator
  local cached
  cached=$(read_cache)
  if [ -n "$cached" ]; then
    echo "STALE|$cached"
    return 0
  fi

  # Complete failure: no fresh data and no cache
  echo "ERROR|"
  return 1
}

# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT BUILDERS
# ═══════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# DIRECTORY COMPONENT
# ─────────────────────────────────────────────────────────────────────────────

dir_text=""
if [ "$SHOW_DIRECTORY" = "1" ]; then
  dir_text="${BLUE}${current_dir}${RESET}"
fi

# ─────────────────────────────────────────────────────────────────────────────
# GIT BRANCH & STATUS COMPONENT
# ─────────────────────────────────────────────────────────────────────────────

branch_text=""
if [ "$SHOW_BRANCH" = "1" ]; then
  # Only proceed if we're inside a git repository
  if git rev-parse --git-dir > /dev/null 2>&1; then

    # Fetch all git info in a single call for efficiency
    # --porcelain=v2 provides machine-readable output with branch tracking info
    # --branch includes upstream tracking information
    git_status=$(timeout 1 git status --porcelain=v2 --branch 2>/dev/null || \
                 git status --porcelain=v2 --branch 2>/dev/null)

    # Extract branch name from "# branch.head <name>" line
    branch=$(echo "$git_status" | grep "^# branch.head" | cut -d' ' -f3)

    if [ -n "$branch" ]; then
      branch_text="${GREEN}⎇ ${branch}${RESET}"

      # ─────────────────────────────────────────────────────────────────────
      # Working tree status indicators (+, *, ?)
      # ─────────────────────────────────────────────────────────────────────
      if [ "$SHOW_GIT_STATUS" = "1" ]; then

        # Staged changes (+): Lines starting with "1 X." or "2 X." where X is M/A/D/R/C
        # porcelain v2 format: "1 <XY> ..." where X=staged, Y=unstaged
        if echo "$git_status" | grep -q "^[12] [MADRC]"; then
          branch_text="${branch_text}${CYAN}+${RESET}"
        fi

        # Unstaged changes (*): Lines with modifications in working tree (second char)
        if echo "$git_status" | grep -q "^[12] .[MADRC]"; then
          branch_text="${branch_text}${YELLOW}*${RESET}"
        fi

        # Untracked files (?): Lines starting with "?"
        if echo "$git_status" | grep -q "^?"; then
          branch_text="${branch_text}${GRAY}?${RESET}"
        fi
      fi

      # ─────────────────────────────────────────────────────────────────────
      # Remote tracking status (⇡, ⇣, ≡, ○)
      # ─────────────────────────────────────────────────────────────────────
      if [ "$SHOW_GIT_REMOTE" = "1" ]; then
        # Extract ahead/behind from "# branch.ab +<ahead> -<behind>" line
        ahead=$(echo "$git_status" | grep "^# branch.ab" | sed 's/.*+\([0-9]*\).*/\1/')
        behind=$(echo "$git_status" | grep "^# branch.ab" | sed 's/.*-\([0-9]*\).*/\1/')

        remote_text=""

        # Commits ahead of remote (need to push)
        if [ -n "$ahead" ] && [ "$ahead" != "0" ]; then
          remote_text="${remote_text}${GREEN}⇡${ahead}${RESET}"
        fi

        # Commits behind remote (need to pull)
        if [ -n "$behind" ] && [ "$behind" != "0" ]; then
          remote_text="${remote_text}${RED}⇣${behind}${RESET}"
        fi

        # Determine tracking state
        if echo "$git_status" | grep -q "^# branch.upstream"; then
          # Has upstream: show ≡ if fully synced (no ahead/behind shown)
          [ -z "$remote_text" ] && remote_text="${GRAY}≡${RESET}"
        else
          # No upstream configured
          remote_text="${GRAY}○${RESET}"
        fi

        [ -n "$remote_text" ] && branch_text="${branch_text} ${remote_text}"
      fi

      # ─────────────────────────────────────────────────────────────────────
      # Stash count {n}
      # ─────────────────────────────────────────────────────────────────────
      if [ "$SHOW_GIT_STASH" = "1" ]; then
        stash_count=$(git stash list 2>/dev/null | wc -l | tr -d ' ')
        if [ "$stash_count" -gt 0 ]; then
          branch_text="${branch_text} ${GRAY}{${stash_count}}${RESET}"
        fi
      fi
    fi
  fi
fi

# ─────────────────────────────────────────────────────────────────────────────
# USAGE COMPONENT
# ─────────────────────────────────────────────────────────────────────────────

usage_text=""
if [ "$SHOW_USAGE" = "1" ]; then
  usage_result=$(fetch_usage)

  # Check if data is stale (API failed but cache was available)
  stale_indicator=""
  if [[ "$usage_result" =~ ^STALE\| ]]; then
    stale_indicator=" ${YELLOW}⚠${RESET}"
    usage_result="${usage_result#STALE|}"  # Strip STALE prefix
  fi

  # Parse and display usage if we have valid data
  if [ -n "$usage_result" ] && [[ ! "$usage_result" =~ ^ERROR ]]; then
    utilization=$(echo "$usage_result" | cut -d'|' -f1)
    resets_at=$(echo "$usage_result" | cut -d'|' -f2)

    # Validate utilization is a number
    if [ -n "$utilization" ] && [[ "$utilization" =~ ^[0-9]+$ ]]; then
      usage_color=$(get_usage_color "$utilization")

      # Build progress bar if enabled
      progress_bar=""
      if [ "$SHOW_PROGRESS_BAR" = "1" ]; then
        progress_bar=" $(build_progress_bar "$utilization")"
      fi

      # Build reset time display if enabled and data available
      reset_time_display=""
      if [ "$SHOW_RESET_TIME" = "1" ] && [ -n "$resets_at" ] && [ "$resets_at" != "null" ]; then
        # Parse ISO 8601 timestamp (strip fractional seconds and Z suffix)
        iso_time=$(echo "$resets_at" | sed 's/\.[0-9]*Z$//')
        epoch=$(date -ju -f "%Y-%m-%dT%H:%M:%S" "$iso_time" "+%s" 2>/dev/null)

        if [ -n "$epoch" ]; then
          # Respect system time format preference (12h vs 24h)
          # macOS stores this in AppleICUForce24HourTime (1 = 24h, 0/missing = 12h)
          time_format=$(defaults read -g AppleICUForce24HourTime 2>/dev/null)
          if [ "$time_format" = "1" ]; then
            reset_time=$(date -r "$epoch" "+%H:%M" 2>/dev/null)
          else
            reset_time=$(date -r "$epoch" "+%-I:%M %p" 2>/dev/null)
          fi
          [ -n "$reset_time" ] && reset_time_display=" ${GRAY}↻ ${reset_time}${RESET}"
        fi
      fi

      # Assemble usage display
      usage_text="${usage_color}Usage: ${utilization}%${progress_bar}${RESET}${stale_indicator}${reset_time_display}"
    else
      # Invalid utilization value
      usage_text="${GRAY}Usage: --${RESET}"
    fi
  else
    # No data available (ERROR or empty)
    usage_text="${GRAY}Usage: --${RESET}"
  fi
fi

# ═══════════════════════════════════════════════════════════════════════════
# OUTPUT ASSEMBLY
# ═══════════════════════════════════════════════════════════════════════════

# Combine all enabled components with separator
output=""
separator="${GRAY} │ ${RESET}"

# Add directory (first component, no leading separator)
[ -n "$dir_text" ] && output="${dir_text}"

# Add git branch/status
if [ -n "$branch_text" ]; then
  [ -n "$output" ] && output="${output}${separator}"
  output="${output}${branch_text}"
fi

# Add usage display
if [ -n "$usage_text" ]; then
  [ -n "$output" ] && output="${output}${separator}"
  output="${output}${usage_text}"
fi

# Output final statusline
printf "%s\n" "$output"
