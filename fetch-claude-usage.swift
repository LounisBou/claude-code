#!/usr/bin/env swift
//
// ╔═══════════════════════════════════════════════════════════════════════════╗
// ║                    CLAUDE API USAGE FETCHER                               ║
// ╚═══════════════════════════════════════════════════════════════════════════╝
//
// Fetches Claude API usage data from claude.ai and outputs it in a format
// suitable for the statusline script.
//
// CONFIGURATION:
//   Reads credentials from .env file in the same directory:
//   - CLAUDE_SESSION_KEY: Session key from claude.ai browser cookies
//   - CLAUDE_ORGANIZATION_ID: Organization ID from claude.ai
//
// OUTPUT FORMAT:
//   Success: "UTILIZATION|RESETS_AT" (e.g., "42|2024-01-29T15:30:00Z")
//   Error:   "ERROR:description"
//
// ─────────────────────────────────────────────────────────────────────────────

import Foundation

// ─────────────────────────────────────────────────────────────────────────────
// ENVIRONMENT FILE PARSING
// ─────────────────────────────────────────────────────────────────────────────

/// Parses a .env file and returns a dictionary of key-value pairs.
func parseEnvFile(at path: URL) -> [String: String]? {
    guard let contents = try? String(contentsOf: path, encoding: .utf8) else {
        return nil
    }

    var env: [String: String] = [:]

    for line in contents.components(separatedBy: .newlines) {
        let trimmed = line.trimmingCharacters(in: .whitespaces)

        // Skip comments and empty lines
        if trimmed.isEmpty || trimmed.hasPrefix("#") {
            continue
        }

        // Split on first '='
        if let equalIndex = trimmed.firstIndex(of: "=") {
            let key = String(trimmed[..<equalIndex]).trimmingCharacters(in: .whitespaces)
            let value = String(trimmed[trimmed.index(after: equalIndex)...]).trimmingCharacters(in: .whitespaces)
            env[key] = value
        }
    }

    return env
}

/// Loads .env file with fallback chain:
///   1. Script directory (./.claude/.env)
///   2. CLAUDE_CONFIG_DIR/.env (from environment variable)
/// Returns a dictionary of key-value pairs.
func loadEnvFile() -> [String: String] {
    // Try 1: Script directory
    let scriptPath = CommandLine.arguments[0]
    let scriptURL = URL(fileURLWithPath: scriptPath)
    let scriptDir = scriptURL.deletingLastPathComponent()
    let localEnvPath = scriptDir.appendingPathComponent(".env")

    if let env = parseEnvFile(at: localEnvPath) {
        return env
    }

    // Try 2: CLAUDE_CONFIG_DIR from environment
    if let configDir = ProcessInfo.processInfo.environment["CLAUDE_CONFIG_DIR"] {
        let configEnvPath = URL(fileURLWithPath: configDir).appendingPathComponent(".env")
        if let env = parseEnvFile(at: configEnvPath) {
            return env
        }
    }

    return [:]
}

// ─────────────────────────────────────────────────────────────────────────────
// CREDENTIAL READERS
// ─────────────────────────────────────────────────────────────────────────────

/// Reads the session key from .env file
func readSessionKey(from env: [String: String]) -> String? {
    guard let key = env["CLAUDE_SESSION_KEY"] else { return nil }
    let trimmed = key.trimmingCharacters(in: .whitespacesAndNewlines)
    return trimmed.isEmpty ? nil : trimmed
}

/// Reads the organization ID from .env file
func readOrganizationId(from env: [String: String]) -> String? {
    guard let orgId = env["CLAUDE_ORGANIZATION_ID"] else { return nil }
    let trimmed = orgId.trimmingCharacters(in: .whitespacesAndNewlines)
    return trimmed.isEmpty ? nil : trimmed
}

// ─────────────────────────────────────────────────────────────────────────────
// API FETCH
// ─────────────────────────────────────────────────────────────────────────────

/// Fetches usage data from Claude API
/// Returns utilization percentage and reset timestamp
func fetchUsageData(sessionKey: String, orgId: String) async throws -> (utilization: Int, resetsAt: String?) {
    // Validate orgId doesn't contain path traversal
    guard !orgId.contains(".."), !orgId.contains("/") else {
        throw NSError(domain: "ClaudeAPI", code: 5,
                      userInfo: [NSLocalizedDescriptionKey: "Invalid organization ID"])
    }

    guard let url = URL(string: "https://claude.ai/api/organizations/\(orgId)/usage") else {
        throw NSError(domain: "ClaudeAPI", code: 0,
                      userInfo: [NSLocalizedDescriptionKey: "Invalid URL"])
    }

    var request = URLRequest(url: url)
    request.setValue("sessionKey=\(sessionKey)", forHTTPHeaderField: "Cookie")
    request.setValue("application/json", forHTTPHeaderField: "Accept")
    request.httpMethod = "GET"

    let (data, response) = try await URLSession.shared.data(for: request)

    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw NSError(domain: "ClaudeAPI", code: 3,
                      userInfo: [NSLocalizedDescriptionKey: "Failed to fetch usage"])
    }

    // Parse JSON response
    if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
       let fiveHour = json["five_hour"] as? [String: Any],
       let utilization = fiveHour["utilization"] as? Int {
        let resetsAt = fiveHour["resets_at"] as? String
        return (utilization, resetsAt)
    }

    throw NSError(domain: "ClaudeAPI", code: 4,
                  userInfo: [NSLocalizedDescriptionKey: "Invalid response format"])
}

// ─────────────────────────────────────────────────────────────────────────────
// MAIN EXECUTION
// ─────────────────────────────────────────────────────────────────────────────

Task {
    // Load environment variables from .env file
    let env = loadEnvFile()

    guard let sessionKey = readSessionKey(from: env) else {
        print("ERROR:NO_SESSION_KEY")
        exit(1)
    }

    guard let orgId = readOrganizationId(from: env) else {
        print("ERROR:NO_ORG_CONFIGURED")
        exit(1)
    }

    do {
        let (utilization, resetsAt) = try await fetchUsageData(sessionKey: sessionKey, orgId: orgId)

        // Output format: UTILIZATION|RESETS_AT
        if let resets = resetsAt {
            print("\(utilization)|\(resets)")
        } else {
            print("\(utilization)|")
        }
        exit(0)
    } catch {
        print("ERROR:\(error.localizedDescription)")
        exit(1)
    }
}

// Keep script alive while async Task executes
RunLoop.main.run()
