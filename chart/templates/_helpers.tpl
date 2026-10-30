{{/* Labels on every resource of the app */}}
{{- define "final-project.labels" -}}
app.kubernetes.io/name: final-project-app
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/* Labels the Service uses to find the app pods */}}
{{- define "final-project.selectorLabels" -}}
app.kubernetes.io/name: final-project-app
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
