<template>
  <div class="project-card">
    <div class="card-header">
      <h3>
        <a :href="githubUrl" target="_blank" rel="noopener noreferrer">
          {{ project.owner_name }}/{{ project.repo_name }}
        </a>
      </h3>
      <div class="meta">
        <span class="owner">by {{ project.user_name || project.owner_name }}</span>
      </div>
    </div>
    <div class="card-body">
      <p class="description">{{ project.description || 'No description provided.' }}</p>
      <div class="readme-preview" v-if="project.full_readme">
        <div class="markdown-content" v-html="renderedMarkdown"></div>
      </div>
    </div>
    <div class="card-footer">
      <small>Updated: {{ formattedDate }}</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'

const props = defineProps<{ project: any }>()

const md = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: true
})

const githubUrl = computed(() => {
  const data = props.project.github_data
  return data?.html_url || `https://github.com/${props.project.owner_name}/${props.project.repo_name}`
})

const formattedDate = computed(() => {
  if (!props.project.repo_updated_at) return 'unknown'
  return new Date(props.project.repo_updated_at).toLocaleDateString()
})

const renderedMarkdown = computed(() => {
  if (!props.project.full_readme) return ''
  const html = md.render(props.project.full_readme)
  // Обернуть таблицы в контейнер для скроллбара
  return html.replace(/<table>/g, '<div class="table-wrapper"><table>')
            .replace(/<\/table>/g, '</table></div>')
})
</script>

<style scoped>
.project-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  overflow: hidden;
  transition: transform 0.1s ease;
}
.project-card:hover {
  transform: translateY(-2px);
}
.card-header {
  padding: 1rem 1rem 0.5rem;
  border-bottom: 1px solid #edf2f7;
}
.card-header h3 {
  margin: 0 0 0.25rem;
  font-size: 1.1rem;
}
.card-header a {
  text-decoration: none;
  color: #2563eb;
}
.meta {
  font-size: 0.8rem;
  color: #64748b;
}
.card-body {
  padding: 1rem;
}
.description {
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  color: #334155;
}
.readme-preview {
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.85rem;
  color: #1e293b;
  max-height: 300px;
  overflow-y: auto;
}

/* Markdown стили */
.markdown-content {
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  margin: 0.75rem 0 0.5rem;
  font-weight: 600;
}

.markdown-content :deep(h1) { font-size: 1.1rem; }
.markdown-content :deep(h2) { font-size: 1rem; }
.markdown-content :deep(h3) { font-size: 0.95rem; }
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) { font-size: 0.9rem; }

.markdown-content :deep(p) {
  margin: 0.5rem 0;
  line-height: 1.5;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.markdown-content :deep(li) {
  margin: 0.25rem 0;
}

.markdown-content :deep(code:not(pre code)) {
  background: #e2e8f0;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.85em;
}

.markdown-content :deep(pre) {
  background: #1e293b;
  color: #e2e8f0;
  padding: 0.75rem;
  border-radius: 6px;
  overflow-x: auto;
  margin: 0.5rem 0;
}

.markdown-content :deep(pre code) {
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid #cbd5e1;
  padding-left: 0.75rem;
  margin: 0.5rem 0;
  color: #64748b;
  font-style: italic;
}

.markdown-content :deep(a) {
  color: #2563eb;
  text-decoration: none;
}

.markdown-content :deep(a:hover) {
  text-decoration: underline;
}

/* Таблицы с горизонтальным скроллбаром */
.table-wrapper {
  overflow-x: auto;
  border-radius: 6px;
  margin: 0.5rem 0;
}

.markdown-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  font-size: 0.85rem;
}

.markdown-content :deep(th) {
  background: #e2e8f0;
  padding: 0.5rem;
  text-align: left;
  font-weight: 600;
  border: 1px solid #cbd5e1;
}

.markdown-content :deep(td) {
  padding: 0.5rem;
  border: 1px solid #cbd5e1;
}

.markdown-content :deep(tr:nth-child(even)) {
  background: #f8fafc;
}

.markdown-content :deep(hr) {
  border: none;
  border-top: 1px solid #cbd5e1;
  margin: 0.75rem 0;
}

.card-footer {
  padding: 0.75rem 1rem;
  background: #f9fafb;
  font-size: 0.7rem;
  color: #6c757d;
  border-top: 1px solid #edf2f7;
}

/* Скроллбар стили */
.readme-preview::-webkit-scrollbar {
  height: 6px;
  width: 6px;
}

.readme-preview::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.readme-preview::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.readme-preview::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.table-wrapper::-webkit-scrollbar {
  height: 6px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: transparent;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.table-wrapper::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
