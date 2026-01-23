# Sandbox Documentation - Claude Code

## Table of Contents

1. [Introduction](#1-introduction)
2. [How Sandboxing Works](#2-how-sandboxing-works)
3. [Getting Started](#3-getting-started)
4. [Complete Configuration](#4-complete-configuration)
5. [Use Cases](#5-use-cases)
6. [Practical Examples](#6-practical-examples)
7. [Limitations and Security Considerations](#7-limitations-and-security-considerations)

---

## 1. Introduction

### 1.1 What is Sandboxing?

**Sandboxing** is a native Claude Code feature that provides a secure execution environment for agents while drastically reducing the number of permission prompts.

Instead of asking for approval for each bash command, sandboxing creates **predefined boundaries** within which Claude Code can work freely with reduced risk.

> 💡 According to Anthropic, sandboxing reduces permission prompts by **84%** in internal usage.

### 1.2 Why Use Sandboxing?

Traditional permission-based security poses several problems:

| Problem | Description |
|---------|-------------|
| **Approval fatigue** | Repeatedly clicking "approve" causes users to pay less attention to what they're approving |
| **Reduced productivity** | Constant interruptions slow down development workflows |
| **Limited autonomy** | Claude Code cannot work efficiently while waiting for approvals |

Sandboxing addresses these challenges by:

- **Defining clear boundaries**: specify exactly which directories and network hosts are accessible
- **Reducing prompts**: safe commands within the sandbox don't require approval
- **Maintaining security**: attempts to access resources outside the sandbox trigger notifications
- **Enabling autonomy**: Claude Code operates more independently within defined limits

### 1.3 Fundamental Principle

> ⚠️ **Important**: Effective sandboxing requires **both**: filesystem isolation AND network isolation.
> 
> - Without network isolation → a compromised agent could exfiltrate sensitive files (SSH keys, etc.)
> - Without filesystem isolation → a compromised agent could backdoor system resources to gain network access

---

## 2. How Sandboxing Works

### 2.1 Filesystem Isolation

The sandboxed bash tool restricts filesystem access:

| Behavior | Description |
|----------|-------------|
| **Default writes** | Read/write access to current working directory and its subdirectories |
| **Default reads** | Read access to the entire computer, except certain denied directories |
| **Blocked access** | Cannot modify files outside the working directory without explicit permission |
| **Configurable** | Custom allowed/denied paths via settings |

### 2.2 Network Isolation

Network access is controlled through a proxy server running outside the sandbox:

- **Domain restrictions**: only approved domains can be accessed
- **User confirmation**: new domain requests trigger permission prompts
- **Custom proxy support**: advanced users can implement custom rules on outgoing traffic
- **Comprehensive coverage**: restrictions apply to all scripts, programs, and subprocesses

### 2.3 OS-Level Enforcement

The sandbox uses native OS security primitives:

| System | Technology Used |
|--------|-----------------|
| **Linux** | [bubblewrap](https://github.com/containers/bubblewrap) |
| **macOS** | Seatbelt (native framework) |
| **WSL2** | bubblewrap (same as Linux) |
| **WSL1** | ❌ Not supported (bubblewrap requires WSL2 kernel features) |
| **Native Windows** | ❌ Planned but not yet available |

---

## 3. Getting Started

### 3.1 Enabling Sandboxing

**Method 1: Slash command (temporary for session)**
```
> /sandbox
```

**Method 2: Permanent configuration in settings.json**
```json
{
  "sandbox": {
    "enabled": true
  }
}
```

### 3.2 Sandbox Modes

Claude Code offers two operating modes:

#### Auto-allow Mode (recommended)
Bash commands attempt to run inside the sandbox and are **automatically allowed** without permission. Commands that cannot be sandboxed fall back to the regular permission flow.

#### Regular Permissions Mode
All commands go through the standard permission flow, even when sandboxed. More control, but more approvals required.

> 📝 In both modes, the sandbox enforces the **same restrictions** for files and network. Only auto-approval differs.

---

## 4. Complete Configuration

### 4.1 Configuration File Locations

| Level | Path | Usage |
|-------|------|-------|
| **User** | `~/.claude/settings.json` | Applies to all projects |
| **Project (shared)** | `.claude/settings.json` | Shared with team via git |
| **Project (local)** | `.claude/settings.local.json` | Personal preferences, git-ignored |
| **Enterprise** | `/Library/Application Support/ClaudeCode/managed-settings.json` (macOS) | Non-overridable policies |

### 4.2 Main Sandbox Settings

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker", "git"],
    "allowUnsandboxedCommands": true,
    "enableWeakerNestedSandbox": false
  }
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | boolean | `false` | Enable bash sandboxing (macOS/Linux only) |
| `autoAllowBashIfSandboxed` | boolean | `true` | Auto-approve sandboxed bash commands |
| `excludedCommands` | string[] | `[]` | Commands that run outside the sandbox |
| `allowUnsandboxedCommands` | boolean | `true` | Allow escape via `dangerouslyDisableSandbox` parameter |
| `enableWeakerNestedSandbox` | boolean | `false` | Enable weaker sandbox for unprivileged Docker environments (Linux). **Reduces security.** |

### 4.3 Network Settings

```json
{
  "sandbox": {
    "network": {
      "allowUnixSockets": ["~/.ssh/agent-socket"],
      "allowLocalBinding": true,
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `network.allowUnixSockets` | string[] | `[]` | Unix socket paths accessible in sandbox (SSH agents, Docker, etc.) |
| `network.allowLocalBinding` | boolean | `false` | Allow binding to localhost ports (macOS only) |
| `network.httpProxyPort` | number | - | Custom HTTP proxy port. If not specified, Claude runs its own proxy |
| `network.socksProxyPort` | number | - | Custom SOCKS5 proxy port |

### 4.4 File and Network Access Control

File and network restrictions use **standard permission rules** (not sandbox settings):

```json
{
  "permissions": {
    "deny": [
      "Read(.envrc)",
      "Read(~/.aws/**)",
      "Read(~/.ssh/**)",
      "Edit(/etc/**)"
    ],
    "allow": [
      "Edit(../docs/)",
      "WebFetch(github.com)",
      "WebFetch(*.npmjs.org)"
    ]
  }
}
```

| Rule | Effect |
|------|--------|
| `Read(pattern)` deny | Block reading matching files |
| `Edit(pattern)` allow | Allow writing beyond working directory |
| `Edit(pattern)` deny | Block writing within allowed paths |
| `WebFetch(domain)` allow | Allow network domains |
| `WebFetch(domain)` deny | Block network domains |

---

## 5. Use Cases

### 5.1 When to Use Sandbox?

| Situation | Recommendation |
|-----------|----------------|
| Daily development on a trusted project | ✅ Sandbox enabled with auto-allow |
| Executing third-party or unaudited code | ✅ Strict sandbox with minimal permissions |
| Working with npm/pip dependencies | ✅ Sandbox with allowed registry domains |
| Using Docker | ⚠️ Exclude Docker from sandbox or disable |
| Automated CI/CD | ✅ Sandbox with `--dangerously-skip-permissions` in isolated container |
| Debugging network issues | ⚠️ May require temporary disable |

### 5.2 When NOT to Use Sandbox?

- **WSL1**: Not technically supported
- **Commands requiring Docker**: Incompatible with sandbox
- **Tools requiring watchman**: Use `jest --no-watchman` as alternative
- **Unprivileged Docker environments**: Unless you accept a weakened sandbox

---

## 6. Practical Examples

### 6.1 Basic Secure Configuration

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true
  },
  "permissions": {
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(~/.aws/**)",
      "Read(~/.ssh/**)"
    ]
  }
}
```

### 6.2 Node.js/Next.js Development

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "network": {
      "allowLocalBinding": true
    }
  },
  "permissions": {
    "allow": [
      "WebFetch(registry.npmjs.org)",
      "WebFetch(*.githubusercontent.com)",
      "WebFetch(api.github.com)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(~/.npmrc)"
    ]
  }
}
```

### 6.3 Python Development with Docker Access

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker", "docker-compose"],
    "network": {
      "allowUnixSockets": ["/var/run/docker.sock"]
    }
  },
  "permissions": {
    "allow": [
      "WebFetch(pypi.org)",
      "WebFetch(files.pythonhosted.org)"
    ],
    "deny": [
      "Read(.env)",
      "Read(~/.aws/**)"
    ]
  }
}
```

### 6.4 Strict Enterprise Configuration

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": false,
    "allowUnsandboxedCommands": false
  },
  "permissions": {
    "deny": [
      "Read(**/.env)",
      "Read(**/*.key)",
      "Read(**/*.pem)",
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(sudo:*)"
    ],
    "disableBypassPermissionsMode": "disable"
  }
}
```

### 6.5 Configuration with Custom Proxy

For organizations requiring traffic inspection:

```json
{
  "sandbox": {
    "enabled": true,
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

This enables:
- Decrypting and inspecting HTTPS traffic
- Applying custom filtering rules
- Logging all network requests
- Integrating with existing security infrastructure

---

## 7. Limitations and Security Considerations

### 7.1 Technical Limitations

| Limitation | Impact |
|------------|--------|
| **Performance overhead** | Minimal, but some filesystem operations may be slightly slower |
| **Compatibility** | Some tools requiring specific system access may need configuration adjustments |
| **Platform support** | Linux and macOS only; Windows planned |

### 7.2 Security Limitations

#### Network Filtering
The network filtering system restricts accessible domains but **does not inspect traffic content**. Users must ensure they only allow trusted domains.

> ⚠️ Be cautious with broad domains like `github.com` which could allow data exfiltration. [Domain fronting](https://en.wikipedia.org/wiki/Domain_fronting) may also bypass filtering in some cases.

#### Unix Sockets
`allowUnixSockets` can grant access to powerful system services. For example, allowing `/var/run/docker.sock` effectively grants access to the host system through Docker.

#### File Permissions
Overly broad write permissions can enable privilege escalation through modifying:
- Executables in `$PATH`
- System configuration directories
- Shell configuration files (`.bashrc`, `.zshrc`)

#### Weakened Linux Sandbox
The `enableWeakerNestedSandbox` option for unprivileged Docker environments **considerably reduces security**. Only use if additional isolation is otherwise enforced.

### 7.3 Escape Hatch Mechanism

Claude Code includes an intentional escape hatch: when a command fails due to sandbox restrictions, Claude can retry it with `dangerouslyDisableSandbox`. These commands go through the normal permission flow.

To disable this escape hatch:
```json
{
  "sandbox": {
    "allowUnsandboxedCommands": false
  }
}
```

### 7.4 Known Incompatibilities

| Tool | Issue | Solution |
|------|-------|----------|
| **Docker** | Incompatible with sandbox | Add to `excludedCommands` |
| **watchman** | Incompatible with sandbox | Use `jest --no-watchman` |
| **CLI tools with network access** | May require allowed domains | Add domains progressively |

---

## Additional Resources

- [Official Sandboxing Documentation](https://code.claude.com/docs/en/sandboxing)
- [Settings Documentation](https://code.claude.com/docs/en/settings)
- [GitHub sandbox-runtime (open source)](https://github.com/anthropic-experimental/sandbox-runtime)

---

*Documentation generated on January 23, 2026*
