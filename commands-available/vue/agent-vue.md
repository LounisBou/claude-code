---
name: agent-vue
description: Create, modify, or analyze Vue.js components with Vue 3 Composition API best practices
user_invocable: true
---

# Vue Command

Launches the vuejs-developer agent to work with Vue.js components.

## Usage

```bash
/vue [task_description]
```

## Examples

```bash
# Create a new component
/vue "create a UserCard component with avatar, name, and email"

# Modify existing component
/vue "add dark mode support to the Navbar component"

# Analyze component
/vue "explain how the ShoppingCart component works"

# Fix component issue
/vue "fix the reactivity issue in ProductList.vue"

# Convert to Composition API
/vue "convert UserProfile.vue from Options API to Composition API"

# General Vue work
/vue
```

## What It Does

1. Creates new Vue components from scratch
2. Modifies existing components (add features, fix bugs, refactor)
3. Analyzes component structure and data flow
4. Converts between Options API and Composition API
5. Integrates with Tailwind CSS, ApexCharts, Shadcn Vue
6. Follows Vue 3 best practices

## Capabilities

### Component Creation
- Vue 3 Composition API with `<script setup>`
- TypeScript support
- Props and emits with proper typing
- Reactive state management
- Computed properties and watchers

### Framework Integration
- Vue Router integration
- Pinia state management
- Tailwind CSS styling
- ApexCharts visualizations
- Shadcn Vue components

### Code Quality
- Proper TypeScript types
- Event naming conventions
- Reactive patterns (ref vs reactive)
- Lifecycle hooks usage
- Performance optimizations

## When to Use

- Creating new Vue components
- Modifying .vue files
- Working with Vue 3 Composition API
- Integrating Vue libraries
- Converting Vue 2 to Vue 3 patterns
- Debugging Vue reactivity issues

---

When this command is invoked, work on the Vue.js task. Check package.json for Vue version, look for tsconfig.json for TypeScript usage, and examine existing .vue files to understand project conventions before making changes.
