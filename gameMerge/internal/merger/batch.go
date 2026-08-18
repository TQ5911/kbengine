package merger

import (
	"strings"
)

func BulkInsertSQL(table string, columns []string) (string, string) {
	quoted := make([]string, len(columns))
	for i, c := range columns {
		quoted[i] = "`" + c + "`"
	}
	parts := make([]string, len(columns))
	for i := range parts {
		parts[i] = "?"
	}
	rowPH := "(" + strings.Join(parts, ", ") + ")"

	var b strings.Builder
	b.Grow(len(table) + 32 + len(rowPH)*2)
	b.WriteString("INSERT INTO `")
	b.WriteString(table)
	b.WriteString("` (")
	b.WriteString(strings.Join(quoted, ", "))
	b.WriteString(") VALUES ")
	return b.String(), rowPH
}

func AppendRowPlaceholders(buf *strings.Builder, rowPH string, count int) {
	for i := 0; i < count; i++ {
		if i > 0 {
			buf.WriteString(", ")
		}
		buf.WriteString(rowPH)
	}
}